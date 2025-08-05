from PIL import Image
import os

# Folder where your images are
folder = "static"

for filename in os.listdir(folder):
    if filename.lower().endswith(".jpg"):
        filepath = os.path.join(folder, filename)
        img = Image.open(filepath).convert("RGBA")

        # Create white background
        bg = Image.new("RGB", img.size, (255, 255, 255))
        bg.paste(img, mask=img.split()[3])  # Use alpha channel as mask

        # Save new JPG
        new_filename = filename.replace(".jpg", ".jpeg")
        new_filepath = os.path.join(folder, new_filename)
        bg.save(new_filepath, "JPEG")

        print(f"Converted {filename} → {new_filename}")
