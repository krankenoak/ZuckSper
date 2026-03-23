import random
import os

IMAGE_FOLDER = "gifs/"
files = os.listdir(IMAGE_FOLDER)
media_files = [f for f in files if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.webp'))]    

def get_random_media_file():
    if not media_files:
        return None 

    chosen_file = random.choice(media_files)
    return os.path.join(IMAGE_FOLDER, chosen_file)
