import os
import io


def get_project_image_cover_data(project_id):
    from PIL import Image

    directory = f"app/images/{project_id}/"

    image_files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f)) and f.lower().endswith(('.png', '.jpg', '.jpeg'))]

    if image_files:
        cover_image_path = os.path.join(directory, image_files[0])

        image = Image.open(cover_image_path)

        img_byte_array = io.BytesIO()
        image.save(img_byte_array, format='PNG')
        img_byte_array.seek(0)

        image_data = img_byte_array.read()

        return image_data