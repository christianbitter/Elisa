import os
import pygame
import json


def load_image(fp, colorkey=None, image_only=False):
    if not fp:
        raise ValueError("load_image - fp not provided")

    fullname = os.path.join(fp)
    try:
        image = pygame.image.load(fullname)
    except pygame.error as message:
        print('Cannot load image:', fp)
        raise SystemExit(message)

    image = image.convert()
    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0,0))
        image.set_colorkey(colorkey, pygame.RLEACCEL)

    if image_only:
        return image
    else:
        return image, image.get_rect()


def load_png(fp, image_only=False):
    """ Load image and return image object"""
    if not fp:
        raise ValueError("load_png - fp not provided")
    if not os.path.exists(fp):
        raise ValueError("load_png - {} does not exist".format(fp))

    fullname = os.path.join(fp)
    try:
        image = pygame.image.load(fullname)
        if image.get_alpha() is None:
            image = image.convert()
        else:
            image = image.convert_alpha()
    except pygame.error as message:
        print('Cannot load image:', fullname)
        raise SystemExit(message)
    if image_only:
        return image
    else:
        return image, image.get_rect()

class PSprite(object):
    def __init__(self, id, w, h, img):
        super(PSprite, self).__init__()
        self._id = id
        self._width = w
        self._height = h
        self._image = img

    @property
    def id(self):
        return self._id

    @property
    def image(self):
        return self._image

    @property
    def width(self):
        return self._width

    @property
    def height(self):
        return self._height


class SpriteMap(object):
    def __init__(self, json_descriptor: str):
        super(SpriteMap, self).__init__()
        self._descriptor = json_descriptor
        self._sprites = {}
        self._id = None
        self._description = None
        self._source = None
        self._image_path = None
        self._width = None
        self._height = None
        self._no_sprites = None
        self._sprites = {}
        self._initialized = False
        self._image = None
        self._sprites = {}
        self._idx2key = []

    @property
    def initialized(self):
        return self._initialized

    def _load_image(self) -> None:
        img_name = os.path.basename(self._image_path)

        if img_name.endswith("png"):
            self._image, r = load_png(self._image_path)
        else:
            colour_key = None
            if self._color_key:
                colour_key = self._colour_key
            self._image, r = load_image(self._image_path, colour_key)

        self._width, self._height = r.width, r.height
        return None

    def initialize(self):
        if not self._initialized:
            with open(self._descriptor, mode='r+') as fp:
                self._sprite_map = json.load(fp)

            if 'id' not in self._sprite_map: raise ValueError("SpriteMap - id missing")
            if 'width' not in self._sprite_map: raise ValueError("SpriteMap - width missing")
            if 'height' not in self._sprite_map: raise ValueError("SpriteMap - height missing")
            if 'image_path' not in self._sprite_map: raise ValueError("SpriteMap - image path missing")
            if 'no_sprites' not in self._sprite_map: raise ValueError("SpriteMap - no_sprites missing")
            self._id = self._sprite_map['id']
            self._width = self._sprite_map['width']
            self._height = self._sprite_map['height']
            self._image_path = self._sprite_map['image_path']
            self._no_sprites = self._sprite_map['no_sprites']
            self._colour_key = self._sprite_map['color_key']

            self._description = self._sprite_map['description']
            self._source = self._sprite_map['source']

            self._load_image()
            # load sprites
            sprites = self._sprite_map['sprites']
            for i, sprite_def in enumerate(sprites):
                id = sprite_def['id']
                x = sprite_def['x']
                y = sprite_def['y']
                w = sprite_def['width']
                h = sprite_def['height']
                sprite_img = self._image.subsurface(x, y, w, h)
                self._sprites[id] = PSprite(id, w, h, sprite_img)
                self._idx2key.append(id)

            if self._no_sprites > 0 and self._no_sprites != len(self._sprites):
                raise ValueError("Number of defined sprites does not match declared sprites")
            self._initialized = True

    def __getitem__(self, item):
        if item is None:
            raise ValueError("SpriteMap.get - key not provided")

        if isinstance(item, int):
            return self._sprites[self._idx2key[item]]
        else:
            if item in self._sprites:
                return self._sprites[item]

        raise ValueError("SpriteMap.get - undefined sprite selected")

    @property
    def no_sprites(self):
        return self._no_sprites