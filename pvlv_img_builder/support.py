import os
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
from pvlv_img_builder.configurations.configuration import (
    DEBUG,
    BACKGROUND_COLOR,
    DIR_DEFAULT_FONT,
)

SPAN_BORDER = 0.3
SPAN_TITLE = 1.8
SPAN_TEXT = 1


class Position(enumerate):
    UP = 'up'
    DOWN = 'down'
    RIGHT = 'right'
    LEFT = 'left'
    CENTER = 'center'


class DrawSupport(object):

    def __init__(self, data):

        self.data = data
        self.y_resolution = 30
        self.width = 350
        self.height = 0

        self.x_cursor = 0
        self.y_cursor = SPAN_BORDER*self.y_resolution

        self.background_color = self.data.get('background_color', BACKGROUND_COLOR)
        self.image: Image
        self.draw: ImageDraw

        # set the absolute path dir for the font.
        dir_path = os.path.dirname(os.path.realpath(__file__))
        self.font_dir = self.data.get('font', dir_path + DIR_DEFAULT_FONT)

        # Standard fonts Global for all the canvas
        self.font_title = ImageFont.truetype(self.font_dir, int(self.y_resolution * SPAN_TEXT / 1.3))
        self.font_text = ImageFont.truetype(self.font_dir, int(self.y_resolution * SPAN_TEXT / 2))

    def build_canvas(self):
        # img = Image.open("img.png")
        self.image = Image.new("RGB", (self.width, self.height), self.background_color)
        # self.image.paste(img)
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

    def get_text_dimension(self, text, font=None):
        """
        :param text: string of the name that you want to print
        :param font: font
        :return: the width abd the high of the text if printed
        """
        w, h = self.draw.textsize(text, font=font)
        return w, h

    # if there is no y it means that the draw is y automated and should follow the y_cursor
    def update_y_cursor(self, span, align=Position.CENTER):

        y_cursor_increment = (span / 2) * self.y_resolution

        if align == Position.UP:
            increment = y_cursor_increment - 2/3*y_cursor_increment
            y = self.y_cursor + increment
        elif align == Position.DOWN:
            increment = y_cursor_increment + 2/3*y_cursor_increment
            y = self.y_cursor + increment
        else:
            y = self.y_cursor + y_cursor_increment

        self.y_cursor += y_cursor_increment * 2

        return y

    def draw_text(self, x, text, y=None, span=1, fill=None, font=None, anchor=None, origin_x=None, origin_y=None):
        """
        :param x: value of x entry point
        :param y: value of y entry point
        :param text: string of the name that you want to print
        :param span: the di dimension of the section
        :param fill: fill
        :param font: font
        :param anchor: value_printed
        :param origin_x: where the text must start in reference of the origin (center, right or left)
        :param origin_y: same of x but up, down and center
        """
        if not text:
            return

        if not y:
            y = self.update_y_cursor(span)

        w, h = self.draw.textsize(text, font=font)

        if origin_y == Position.UP:
            _y = y - h
        elif origin_y == Position.DOWN:
            _y = y + h
        else:
            _y = y - h / 2

        if origin_x == Position.RIGHT:
            _x = x
        elif origin_x == Position.LEFT:
            _x = x - w
        else:
            _x = x - w / 2

        self.draw.text([_x, _y], text, fill=fill, font=font, anchor=anchor)

    def draw_multiline_text_in_center(self, x, text, y=None, span=1, fill=None, font=None, anchor=None, align=None):
        """
        :param x: value of x entry point
        :param y: value of y entry point
        :param text: string of the name that you want to print
        :param span: the di dimension of the section
        :param fill: fill
        :param font: font
        :param anchor: anchor
        :param align: align
        """
        if not text:
            return

        if not y:
            y = self.update_y_cursor(span)

        w, h = self.draw.textsize(text, font=font)
        self.draw.multiline_text([(x - w / 2), (y - h / 2)], text, fill=fill, font=font, anchor=anchor, align=align)

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

    def section_line(self):
        if DEBUG:
            self.draw.line([(0, self.y_cursor), (self.width, self.y_cursor)], width=1)
