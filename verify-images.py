import os
from PIL import Image

# Directory containing the images
images_folder = 'images'

def find_and_delete_corrupted_images(folder):
    """
    Scans the specified folder for .webp files, checks if they can be opened,
    and deletes those that cannot be loaded properly.
    """
    # Iterate over all files in the specified folder
    for file_name in os.listdir(folder):
        # Check if the file is a .webp file
        if file_name.lower().endswith('.webp'):
            file_path = os.path.join(folder, file_name)
            try:
                # Attempt to open the image file
                with Image.open(file_path) as img:
                    img.verify()  # Verify the image
                    # Optionally, re-open the image to ensure it's valid
                    img = Image.open(file_path)
            except Exception as e:
                print(f"Deleting corrupted image: {file_path} (Error: {e})")
                os.remove(file_path)  # Delete the file if it cannot be opened

if __name__ == "__main__":
    find_and_delete_corrupted_images(images_folder)
