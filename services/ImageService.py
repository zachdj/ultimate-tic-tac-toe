"""
The ImageService singleton handles the loading of image assets for scenes
It will retrieve images using logical names (e.g. get_main_menu_bg() )
The actual image returned from a logical call can vary based on the selected theme

Once an image is loaded from a file, it is kept in memory in case it is requested again
"""

import pygame
import os
import services.SettingsService as Settings


_image_library = {}


def build_image_path(filename):
    return "assets/img/%s/%s" % (Settings.theme['path_prefix'], filename)


def get_image(path):
    global _image_library
    image = _image_library.get(path)
    if image == None:
        canonicalized_path = path.replace('/', os.sep).replace('\\', os.sep)
        image = pygame.image.load(canonicalized_path).convert()
        _image_library[path] = image
    return image


def get_main_menu_bg():
    return get_image(build_image_path("mm_bg.jpg"))


def get_text_button_sprites():
    normal = build_image_path("dark_btn.png")
    hover = build_image_path("dark_btn_hover.png")
    pressed = build_image_path("dark_btn_pressed.png")
    return get_image(normal), get_image(hover), get_image(pressed)