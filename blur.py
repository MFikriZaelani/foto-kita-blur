#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Peace Sign Blur + Sound

- Detects a peace sign (index + middle finger up, ring & pinky down)
  using MediaPipe Hand Landmarker.
- When the gesture is seen:
    * The camera frame is blurred.
    * The sound effect (sound-foto-kita-blur.mp3) starts playing.
    * Text "foto kita blur" is displayed on the screen.
- When the gesture disappears:
    * The blur is removed.
    * The sound stops.
- Press ESC or 'q' to quit.
"""

import os
import subprocess
import time
from pathlib import Path
from time import monotonic

import cv2
import mediapipe as mp
import numpy as np

# ----------------------------------------------------------------------
# Paths & constants
# ----------------------------------------------------------------------
BASE_DIR = Path(__file__).parent
MODEL_PATH = BASE_DIR / "models" / "hand_landmarker.task"
SOUND_PATH = BASE_DIR / "assets" / "sound-foto-kita-blur.mp3"

# ----------------------------------------------------------------------
# MediaPipe helpers
# ----------------------------------------------------------------------
BaseOptions = mp.tasks.BaseOptions
HandLandmarker = mp.tasks.vision.HandLandmarker
HandLandmarkerOptions = mp.tasks.vision.HandLandmarkerOptions
VisionRunningMode = mp.tasks.vision.RunningMode


def finger_up(tip: int, pip: int, landmarks) -> bool:
    """True if fingertip is above the pip joint (smaller y)."""
    return landmarks[tip].y < landmarks[pip].y


def is_peace(landmarks) -> bool:
    """Peace sign = index & middle up, ring & pinky down."""
    return (
        finger_up(8, 6, landmarks)  # index tip > pip
        and finger_up(12, 10, landmarks)  # middle tip > pip
        and not finger_up(16, 14, landmarks)  # ring down
        and not finger_up(20, 18, landmarks)  # pinky down
    )


def create_landmarker():
    if not MODEL_PATH.exists():
        raise FileNotFoundError(f"Missing MediaPipe model: {MODEL_PATH}")

    options = HandLandmarkerOptions(
        base_options=BaseOptions(model_asset_path=str(MODEL_PATH)),
        running_mode=VisionRunningMode.VIDEO,
        num_hands=1,
        min_hand_detection_confidence=0.1,
        min_hand_presence_confidence=0.1,
        min_tracking_confidence=0.1,
    )
    return HandLandmarker.create_from_options(options)


# ----------------------------------------------------------------------
# Audio helper – ffplay subprocess
# ----------------------------------------------------------------------
def start_sound() -> subprocess.Popen | None:
    """Launch ffplay to play the MP3 silently (looped); return the Popen object."""
    if not SOUND_PATH.is_file():
        print(f"[WARN] Sound file not found: {SOUND_PATH}", flush=True)
        return None
    try:
        # -loop 0 → repeat indefinitely until we kill the process
        return subprocess.Popen(
            ["ffplay", "-nodisp", "-loop", "0", str(SOUND_PATH)],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
    except Exception as e:
        print(f"[ERROR] Failed to start ffplay: {e}", flush=True)
        return None


def stop_sound(proc: subprocess.Popen | None):
    """Terminate the ffplay subprocess gracefully."""
    if proc is None:
        return
    # Only attempt to terminate if the process is still alive
    if proc.poll() is None:  # None means still running
        proc.terminate()
        try:
            proc.wait(timeout=2)
        except subprocess.TimeoutExpired:
            proc.kill()
    # If it already exited, we simply drop the reference


# Emoji handling (no longer needed - removed)


# ----------------------------------------------------------------------
# Hand landmark drawing
# ----------------------------------------------------------------------
# Connections between hand landmarks (MediaPipe hand skeleton)
HAND_CONNECTIONS = [
    (0, 1), (1, 2), (2, 3), (3, 4),           # Thumb
    (0, 5), (5, 6), (6, 7), (7, 8),           # Index
    (0, 9), (9, 10), (10, 11), (11, 12),      # Middle
    (0, 13), (13, 14), (14, 15), (15, 16),    # Ring
    (0, 17), (17, 18), (18, 19), (19, 20),    # Pinky
]


def draw_hand_landmarks(frame: np.ndarray, hand_landmarks, frame_width: int, frame_height: int):
    """Draw hand skeleton on frame."""
    if not hand_landmarks:
        return

    # Draw connections (lines)
    for connection in HAND_CONNECTIONS:
        start_idx, end_idx = connection
        if start_idx >= len(hand_landmarks) or end_idx >= len(hand_landmarks):
            continue

        start = hand_landmarks[start_idx]
        end = hand_landmarks[end_idx]

        x1 = int(start.x * frame_width)
        y1 = int(start.y * frame_height)
        x2 = int(end.x * frame_width)
        y2 = int(end.y * frame_height)

        cv2.line(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

    # Draw landmarks (circles)
    for landmark in hand_landmarks:
        x = int(landmark.x * frame_width)
        y = int(landmark.y * frame_height)
        cv2.circle(frame, (x, y), 5, (0, 0, 255), -1)


# ----------------------------------------------------------------------
# Main loop
# ----------------------------------------------------------------------
def main():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        raise RuntimeError("Could not open camera 0")

    # Optional: lower resolution to reduce CPU load
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    start_time = monotonic()
    last_timestamp_ms = -1
    sound_proc = None
    sound_playing = False

    # Create landmarker once
    landmarker = create_landmarker()

    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                print("[WARN] Frame not received – exiting loop", flush=True)
                break

            # Mirror the image (selfie view)
            frame = cv2.flip(frame, 1)
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            timestamp_ms = int((monotonic() - start_time) * 1000)
            if timestamp_ms <= last_timestamp_ms:
                timestamp_ms = last_timestamp_ms + 1
            last_timestamp_ms = timestamp_ms

            # Hand detection
            mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb)
            hand_result = landmarker.detect_for_video(mp_image, timestamp_ms)

            num_hands = len(hand_result.hand_landmarks)
            if num_hands > 0:
                print(f"[DEBUG] Detected {num_hands} hand(s)", flush=True)

            peace_detected = any(
                is_peace(hand_landmarks)
                for hand_landmarks in hand_result.hand_landmarks
            )

            # Draw hand landmarks on frame
            for hand_landmarks in hand_result.hand_landmarks:
                draw_hand_landmarks(frame, hand_landmarks, frame.shape[1], frame.shape[0])

            # ------------------------------------------------------------------
            # Visual feedback: blur + sound + text
            # ------------------------------------------------------------------
            if peace_detected:
                print("[DEBUG] Peace detected!", flush=True)
                frame = cv2.GaussianBlur(frame, (61, 61), 0)

                # Start sound if not already playing
                if not sound_playing:
                    print("[DEBUG] Starting sound...", flush=True)
                    sound_proc = start_sound()
                    if sound_proc is not None:
                        sound_playing = True

                # Add text "foto kita blur" to the frame
                text = "foto kita blur"
                font = cv2.FONT_HERSHEY_SIMPLEX
                font_scale = 1.5
                color = (0, 255, 255)  # Yellow in BGR
                thickness = 3
                text_size = cv2.getTextSize(text, font, font_scale, thickness)[0]
                x = (frame.shape[1] - text_size[0]) // 2
                y = (frame.shape[0] + text_size[1]) // 2
                cv2.putText(frame, text, (x, y), font, font_scale, color, thickness)
            else:
                # Stop sound if it was playing
                if sound_playing:
                    print("[DEBUG] Stopping sound...", flush=True)
                    stop_sound(sound_proc)
                    sound_proc = None
                    sound_playing = False

            # Show the frame
            cv2.imshow("Peace Blur", frame)

            # ------------------------------------------------------------------
            # Exit handling
            # ------------------------------------------------------------------
            key = cv2.waitKey(1) & 0xFF
            if key == 27 or key == ord("q"):  # ESC or 'q'
                print("[INFO] Exit requested by user", flush=True)
                break
            # Small sleep to cap loop (~200 fps max)
            time.sleep(0.005)

    finally:
        # Clean‑up everything
        if sound_playing and sound_proc:
            stop_sound(sound_proc)
        cap.release()
        cv2.destroyAllWindows()
        print("[INFO] Resources released – goodbye!", flush=True)


if __name__ == "__main__":
    main()
