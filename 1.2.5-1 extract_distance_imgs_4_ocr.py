import os
import hashlib
from PIL import Image
import subprocess
import time
import cv2

# === CONFIG ===
ACCEL_POS = (200, 850, 240, 850, 500)  # (x1, y1, x2, y2)
BRAKE_POS = (2115, 850, 2200, 850, 500)  # (x1, y1, x2, y2)
VIDEO_DEVICE = '/dev/video10'
HOLD_DURATION_MS = 10_000  # 10 seconds (long enough to cover many steps)
TAP_DURATION_MS = 1  # 10 seconds (long enough to cover many steps)


# === Helper funcs ===
def get_frame(cap):
    """Grab single frame from video device"""
    ret, frame = cap.read()
    if not ret:
        raise RuntimeError("Failed to read frame")
    return frame


def resize_img(frame, width=84):
    """Resize frame to given width, preserving aspect ratio (height auto-scaled)"""
    h, w = frame.shape[:2]
    new_w = width
    new_h = int(h * (new_w / w))
    resized = cv2.resize(frame, (new_w, new_h))
    return resized


def ocr_distance(frame):
    """Extract distance from frame via OCR. Return float distance in meters."""
    h, w = frame.shape[:2]

    # ADJUST THESE CROP COORDINATES TO YOUR SCREEN
    x1, x2 = 1800, 2200
    y1, y2 = 20, 60

    # Fix bounds
    x1 = max(0, min(x1, w))
    x2 = max(0, min(x2, w))
    y1 = max(0, min(y1, h))
    y2 = max(0, min(y2, h))

    if x2 <= x1 or y2 <= y1:
        print("OCR: Invalid crop region")
        return 0.0

    roi = frame[y1:y2, x1:x2]

    # Only show if valid
    if roi.size > 0:
        cv2.imshow("OCR Region", roi)
        cv2.waitKey(1)

    # TODO: Add OCR here later
    return 0.0


def save_unique_image(img: Image.Image, folder="assets/extracts"):
    os.makedirs(folder, exist_ok=True)

    # Compute hash of the image
    img_bytes = img.tobytes()
    img_hash = hashlib.md5(img_bytes).hexdigest()
    filepath = os.path.join(folder, f"{img_hash}.png")

    # Save only if not exists
    if not os.path.exists(filepath):
        img.save(filepath)
        return True
    return False


def get_distance_img(frame):
    h, w = frame.shape[:2]
    x1, y1 = 240, 24
    x2, y2 = x1 + 70, y1 + 19

    x1 = max(0, min(x1, w))
    x2 = max(0, min(x2, w))
    y1 = max(0, min(y1, h))
    y2 = max(0, min(y2, h))

    if x2 <= x1 or y2 <= y1:
        return None

    roi = frame[y1:y2, x1:x2]
    if roi.size == 0:
        return None

    # Preprocess for Tesseract: B&W, high contrast
    gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)
    thresh = cv2.bitwise_not(thresh)
    return thresh


# ---------------------------------

# print("[INFO] Starting scrcpy...")
# scrcpy_proc = subprocess.Popen([
#     'scrcpy', f'--v4l2-sink={VIDEO_DEVICE}',
#     '--no-window', '--max-size', '720', '--stay-awake'
# ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
# time.sleep(2)

print(f"[INFO] Opening video device: {VIDEO_DEVICE}")
cap = cv2.VideoCapture(VIDEO_DEVICE)
if not cap.isOpened():
    raise RuntimeError(f"Cannot open {VIDEO_DEVICE}")

print("[INFO] Capture started. Entering main loop...")
frame_count = 0

while True:
    start_iter = time.perf_counter()

    print(f"\n[STEP] Frame {frame_count}: Capturing frame...")
    frame = get_frame(cap)

    print("[STEP] Extracting distance region...")
    distance_img = get_distance_img(frame)
    if distance_img is None:
        print("[WARN] Distance region invalid, skipping.")
        frame_count += 1
        continue

    distance_pil = Image.fromarray(distance_img)
    print("[STEP] Saving unique distance image...")
    did_save = save_unique_image(distance_pil)

    # Display both full frame and distance ROI
    cv2.imshow("Full Frame", frame)
    cv2.imshow("Distance ROI", distance_img)
    cv2.waitKey(1)

    iter_time = time.perf_counter() - start_iter
    status = "saved new!" if did_save else "duplicate (skipped)"
    print(f"[INFO] took: {iter_time * 1000:.1f} ms | {status}")

    frame_count += 1