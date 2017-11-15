"""
The Settings singleton keeps track of application-wide settings
"""

# definition of themes
default_theme = {
    "path_prefix": "default",
    "id": 0,
    "name": "Default",
    "primary": (117, 64, 160),
    "secondary": (61, 189, 73),
    "tertiary": (63, 63, 63),
    "font": (200, 220, 220)
}

themes = [default_theme]

# actual settings
sfx_volume = 100
music_volume = 100
theme = default_theme


# accessors
def set_theme(selected_theme):
    global theme
    theme = selected_theme


def get_themes():
    return themes
