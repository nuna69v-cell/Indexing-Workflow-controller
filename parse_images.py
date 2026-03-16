import os
import pytesseract
from PIL import Image


def extract_text_from_images(directory):
    for filename in os.listdir(directory):
        if filename.lower().endswith((".png", ".jpg", ".jpeg")):
            filepath = os.path.join(directory, filename)
            try:
                img = Image.open(filepath)
                text = pytesseract.image_to_string(img)
                print(f"--- Text from {filename} ---")

                # Check for possible API keys
                for line in text.split("\n"):
                    if (
                        "ghp_" in line
                        or "github_pat" in line
                        or "token" in line.lower()
                        or "key" in line.lower()
                    ):
                        print(f"POSSIBLE KEY FOUND in {filename}: {line}")

            except Exception as e:
                print(f"Error processing {filename}: {e}")


extract_text_from_images("/tmp/file_attachments")
