from PIL import Image, ImageDraw
from io import BytesIO
from pvlv_img_builder.configurations.configuration import (
    BACKGROUND_COLOR,
)


class DrawSupport(object):

    def __init__(self, data):

        self.data = data
        self.y_resolution = 30
        self.width = None
        self.height = 0

        self.background_color = self.data.get('background_color', BACKGROUND_COLOR)
        self.image: Image = None
        self.draw: ImageDraw = None

    def build_canvas(self):
        img = Image.open("img.png")
        self.image = Image.new("RGB", (self.width, self.height), self.background_color)
        self.image.paste(img)
        self.draw = ImageDraw.Draw(self.image)

    def get_section(self, section_name, data, span, default_color):
        height = 0
        section_value = str(data.get(section_name))
        if section_value:
            height += span * self.y_resolution
        section_color = data.get('{}_color'.format(section_name), default_color)

        return section_value, height, section_color

    def get_text(self, section_name, data, span, default_color):
        height = 0
        section_lines = 0
        section_value = str(data.get(section_name))
        if section_value:
            section_lines = section_value.count('\n') + 1
            height += span * section_lines * self.y_resolution
        section_color = data.get('{}_color'.format(section_name), default_color)

        return section_value, height, section_lines, section_color

    @staticmethod
    def get_text_dimension(draw_obj, text, font=None):
        """
        :param draw_obj: object where draw
        :param text: string of the name that you want to print
        :param font: font
        :return: the width abd the high of the text if printed
        """
        w, h = draw_obj.textsize(text, font=font)
        return w, h

    @staticmethod
    def draw_text(draw_obj, x, y, text, fill=None, font=None, anchor=None, origin_x=None, origin_y=None):
        """
        :param draw_obj: object where draw
        :param x: value of x entry point
        :param y: value of y entry point
        :param text: string of the name that you want to print
        :param fill: fill
        :param font: font
        :param anchor: value_printed
        :param origin_x: where the text must start in reference of the origin (center, right or left)
        :param origin_y: same of x but up, down and center
        """
        w, h = draw_obj.textsize(text, font=font)

        if origin_y == 'up':
            _y = y - h
        elif origin_y == 'down':
            _y = y + h
        else:
            _y = y - h / 2

        if origin_x == 'right':
            _x = x
        elif origin_x == 'left':
            _x = x - w
        else:
            _x = x - w / 2

        draw_obj.text([_x, _y], text, fill=fill, font=font, anchor=anchor)

    @staticmethod
    def draw_multiline_text_in_center(draw_obj, x, y, text, fill=None, font=None, anchor=None, align=None):
        """
        :param draw_obj: object where draw
        :param x: value of x entry point
        :param y: value of y entry point
        :param text: string of the name that you want to print
        :param fill: fill
        :param font: font
        :param anchor: anchor
        :param align: align
        """
        w, h = draw_obj.textsize(text, font=font)
        draw_obj.multiline_text([(x - w / 2), (y - h / 2)], text, fill=fill, font=font, anchor=anchor, align=align)

    @staticmethod
    def draw_rectangle(draw_obj, x, y, x_2, y_2, fill=None):
        draw_obj.rectangle([(x, y), (x_2, y_2)], fill=fill)

    def get_image(self):
        """
        :return: image converted as byte array
        """
        # convert the image in bytes to send it
        img_bytes = BytesIO()
        img_bytes.name = 'level_up.png'
        self.image.save(img_bytes, format='PNG')
        img_bytes.seek(0)

        return img_bytes

    def save_image(self, file_dir):
        self.image.save(file_dir, format='PNG')
