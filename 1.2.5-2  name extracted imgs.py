import glob
import os
import cv2

# After data collection, run this to label images
def label_extracted_images():
    extracts_dir = "assets/extracts"
    labeled_dir = "assets/labeled"
    os.makedirs(labeled_dir, exist_ok=True)

    image_paths = sorted(glob.glob(os.path.join(extracts_dir, "*.png")))
    if not image_paths:
        print("[INFO] No images found in assets/extracts")
        return

    label_counts = {}

    for img_path in image_paths:
        img = cv2.imread(img_path)
        if img is None:
            continue

        # Make image very large (4x scale)
        scale = 10
        large_img = cv2.resize(img, (img.shape[1] * scale, img.shape[0] * scale), interpolation=cv2.INTER_NEAREST)
        window_name = "Label Image - Type digits (1-5), press ENTER"
        cv2.namedWindow(window_name, cv2.WINDOW_AUTOSIZE)
        cv2.imshow(window_name, large_img)

        print(f"\n[INFO] Labeling: {os.path.basename(img_path)}")
        print("Type 1-5 digits (0-9) using NUMBER KEYS, then press ENTER.")
        print("Press 'q' to quit, 's' to skip.")

        digits = ""
        while True:
            key = cv2.waitKey(0) & 0xFF
            if key == ord('q'):
                cv2.destroyAllWindows()
                print("[INFO] Quitting labeling.")
                return
            elif key == ord('s'):
                print("[INFO] Skipped.")
                break
            elif key == 13:  # Enter key
                if digits == "":
                    print("No digits entered. Try again.")
                    continue
                if not digits.isdigit() or not (1 <= len(digits) <= 5):
                    print("Invalid: enter 1-5 digits only.")
                    digits = ""
                    continue
                label = digits + "m"
                count = label_counts.get(label, 0)
                label_counts[label] = count + 1
                new_name = f"{label}-{count:02d}.png"
                new_path = os.path.join(labeled_dir, new_name)
                cv2.imwrite(new_path, img)
                os.remove(img_path)
                print(f"[INFO] Saved as: {new_name}")
                break
            elif ord('0') <= key <= ord('9'):
                if len(digits) < 5:
                    digits += chr(key)
                    print(f"Digits so far: {digits}")
                else:
                    print("Max 5 digits allowed.")
            elif key == 8 or key == 127:  # Backspace
                digits = digits[:-1]
                print(f"Digits so far: {digits}")
            else:
                print("Press digits (0-9), Enter, 's' or 'q'.")

    cv2.destroyAllWindows()
    print("[INFO] Labeling complete. Labeled images in 'assets/labeled'.")



# Call this after your data collection loop
label_extracted_images()