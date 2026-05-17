import random
import os

IMAGE_FOLDER = "media/reactions/"

files = os.listdir(IMAGE_FOLDER)
media_files = [
    f for f in files
    if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.webp'))
]

used_files = set()

def get_random_media_file():
    global used_files

    if len(used_files) == len(media_files):
        used_files.clear()

    remaining_files = [
        f for f in media_files
        if f not in used_files
    ]

    chosen_file = random.choice(remaining_files)

    used_files.add(chosen_file)
    return os.path.join(IMAGE_FOLDER, chosen_file)
