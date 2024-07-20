import os
import requests
from PIL import Image
from io import BytesIO
from concurrent.futures import ThreadPoolExecutor, as_completed

from constants import BASE_URL_FOR_IMAGES,HEADERS,PICTURES_FOLDER_NAME
import json


class PictureHandler:
    @classmethod
    def create_pictures_folder(cls)-> None:
        if not os.path.exists(PICTURES_FOLDER_NAME):
            os.makedirs(PICTURES_FOLDER_NAME)
            print(f"Folder '{PICTURES_FOLDER_NAME}' created.")
        else:
            print(f"Folder '{PICTURES_FOLDER_NAME}' already exists.")
    @classmethod
    def get_picture(cls, animal_name_for_url:str) ->str:
        return cls._get_img_src(animal_name_for_url)

    @classmethod
    def download_images_concurrently(cls, animal_names_for_urls:list[str]) ->None:
        with ThreadPoolExecutor(max_workers=20) as executor:
            futures = [executor.submit(cls._download_animal_image_if_needed, name_for_url) for name_for_url in
                       animal_names_for_urls]
            for future in as_completed(futures):
                future.result()

    @classmethod
    def _get_img_src(cls, animal_name_for_url: str) -> str:
        return cls._get_picture_path(animal_name_for_url)

    @classmethod
    def _download_animal_image_if_needed(cls, animal_name_for_url: str) -> None:
        if not cls._picture_exist_in_my_computer(animal_name_for_url):
            try:
                response = requests.get(f'{BASE_URL_FOR_IMAGES}{animal_name_for_url}')
                content = response.content
                response_str = content.decode('utf-8')
                data = json.loads(response_str)
                original_image_url = data['originalimage']['source']
                response_image = requests.get(original_image_url, headers=HEADERS)
                image = Image.open(BytesIO(response_image.content))
                image_path = os.path.join('pictures', f'{animal_name_for_url}.png')
                image.save(image_path, 'PNG')
            except KeyError:
                print(f'{animal_name_for_url} does not have picture ')
    @classmethod
    def _picture_exist_in_my_computer(cls, animal_name_for_url: str):
        picture_full_path = cls._get_picture_path(animal_name_for_url)
        return os.path.isfile(picture_full_path)

    @classmethod
    def _get_picture_path(cls, animal_name_for_url: str):
        current_dir = os.path.dirname(os.path.relpath(__file__))
        pictures_folder = os.path.join(current_dir, 'pictures')
        picture_full_path = os.path.join(pictures_folder, f'{animal_name_for_url}.png')
        return picture_full_path
