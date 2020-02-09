from pvlv_img_builder.configurations.configuration import (
    TEXT_COLOR,
    TITLE_COLOR,
    DEFAULT_BACKGROUND_BAR_COLOR,
    DEFAULT_BAR_COLOR,
    DEFAULT_XP_INSIDE_DARK_COLOR,
    DEFAULT_XP_INSIDE_LIGHT_COLOR,
)
from PIL import ImageFont
from math import ceil
from pvlv_img_builder.utils.formatting import remap_range
from pvlv_img_builder.support import DrawSupport, Position
from pvlv_img_builder.support import (
    SPAN_BORDER,
    SPAN_TITLE,
    SPAN_TEXT,
)

"""                   
    +-----------------------------------------+  
    |              SPAN_BORDER(border)        | span             
    +-----------------------------------------+                                 
    |              SPAN_TITLE(title)          | span     
    |                                         | span 
    +-----------------------------------------+ 
    |              SPAN_DATA                  | span  
    |                                         | span                               
    +--+-----------------------------------+--+   
    |  |                                   |  | span        
    |  |           SPAN_XP_BAR             |  | span
    |  |                                   |  | span           
    +--+-----------------------------------+--+
    |              SPAN_TEXT(text)            | span                         
    +-----------------------------------------+  
    |              SPAN_BORDER(border)        | span     at the end of all                        
    +-----------------------------------------+        
"""

SPAN_DATA = 1
SPAN_XP_BAR = 2


class DrawLevelCard(DrawSupport):

    def __init__(self, data):
        """
        :param data: is a dictionary look the documentation on the top of this file:
        """
        super().__init__(data)

        self.x_border_offset = 25

        self.height += SPAN_BORDER * self.y_resolution  # first border at the top

        self.username, h, self.username_color = self.get_section('username', self.data, SPAN_TITLE, TITLE_COLOR)
        self.height += h

        self.data_section = self.data.get('data')
        if self.data_section:
            # reserve the space
            self.height += SPAN_DATA * self.y_resolution
            # get values
            self.rank = self.data_section.get('rank')
            self.rank_label = self.data_section.get('rank_label')
            self.rank_color = self.data_section.get('rank_color', TEXT_COLOR)
            self.level = self.data_section.get('level')
            self.level_label = self.data_section.get('level_label')
            self.level_color = self.data_section.get('level_color', TEXT_COLOR)

        # add space for SPAN_BAR
        self.bar_section = self.data.get('bar')
        if self.bar_section:
            # reserve the space
            self.height += SPAN_XP_BAR * self.y_resolution
            # get values
            self.bar_value = self.bar_section.get('value')
            self.bar_max = self.bar_section.get('max')
            self.bar_color = self.bar_section.get('bar_color', DEFAULT_BAR_COLOR)
            self.bar_background_color = self.bar_section.get('bar_background_color', DEFAULT_BACKGROUND_BAR_COLOR)
            self.inside_xp_dark_color = self.bar_section.get('inside_xp_dark_color', DEFAULT_XP_INSIDE_DARK_COLOR)
            self.inside_xp_light_color = self.bar_section.get('inside_xp_light_color', DEFAULT_XP_INSIDE_LIGHT_COLOR)

        self.text, h, self.text_lines, self.text_color = self.get_text('text', self.data, SPAN_TEXT, TEXT_COLOR)
        self.height += h

        self.height += SPAN_BORDER * self.y_resolution  # last border at the end
        self.height = ceil(self.height)

        self.build_canvas()

        self.font_username = ImageFont.truetype(self.font_dir, int(self.y_resolution * SPAN_TITLE / 1.8))
        self.font_data_value = ImageFont.truetype(self.font_dir, int(self.y_resolution * SPAN_DATA / 1.6))
        self.font_data_label = ImageFont.truetype(self.font_dir, int(self.y_resolution * SPAN_DATA / 2.2))
        self.font_xp_inside = ImageFont.truetype(self.font_dir, int(self.y_resolution * SPAN_XP_BAR / 1.6))
        self.font_xp_values = ImageFont.truetype(self.font_dir, int(self.y_resolution * SPAN_XP_VALUES / 1.2))
        self.font_text = ImageFont.truetype(self.font_dir, int(self.y_resolution * SPAN_TEXT / 2))

    def __draw_xp_bar(self, y, current_xp, total_xp_level):
        """
        draw shadow frame of the xp bar
        draw the real xp bar
        draw the xp values
        """
        x_1 = self.x_border_offset
        x_max = self.width - self.x_border_offset
        x_2 = remap_range(current_xp, 0, total_xp_level, x_1, x_max)

        y_1 = y - SPAN_BAR*self.y_resolution/2
        y_2 = y + SPAN_BAR*self.y_resolution/2

        self.draw.rectangle([(x_1, y_1), (x_max, y_2)], fill=self.bar_background_color)
        self.draw.rectangle([(x_1, y_1), (x_2, y_2)], fill=self.bar_color)

        text_xp_inside = ' {} XP'.format(current_xp)
        w, h = self.get_text_dimension(text_xp_inside, font=self.font_xp_inside)
        if (x_2 - x_1) > w:
            _origin_x = Position.LEFT
            _fill = self.inside_xp_dark_color
        else:
            _origin_x = Position.RIGHT
            _fill = self.inside_xp_light_color

        self.draw_text(
            x_2,
            text_xp_inside,
            y=y,
            font=self.font_xp_inside,
            fill=_fill,
            origin_x=_origin_x,
        )

        _y_cursor = y + (SPAN_BAR/2 + SPAN_XP_VALUES/2)*self.y_resolution

        self.draw_text(
            self.width - self.x_border_offset,
            '{} / {} XP'.format(current_xp, total_xp_level),
            y=_y_cursor,
            font=self.font_xp_values,
            fill=self.text_color,
            origin_x='left',
        )

    def __draw_data_section(self, y):

        self.draw_text(
            self.x_border_offset,
            self.rank_label,
            y=y,
            font=self.font_data_label,
            fill=self.rank_color,
            origin_x=Position.RIGHT,
            origin_y=Position.UP
        )
        w, h = self.get_text_dimension(str(self.rank_label), font=self.font_data_label)
        self.draw_text(
            self.x_border_offset + w,
            ' #{}'.format(self.rank),
            y=y,
            font=self.font_data_value,
            fill=self.rank_color,
            origin_x=Position.RIGHT,
            origin_y=Position.UP
        )

        self.draw_text(
            self.width - self.x_border_offset,
            str(self.level),
            y=y,
            font=self.font_data_value,
            fill=self.level_color,
            origin_x=Position.LEFT,
            origin_y=Position.UP
        )
        w, h = self.get_text_dimension(str(self.level), font=self.font_data_value)
        self.draw_text(
            self.width - (self.x_border_offset + w),
            '{} '.format(self.level_label),
            y=y,
            font=self.font_data_label,
            fill=self.level_color,
            origin_x=Position.LEFT,
            origin_y=Position.UP,
        )

    def draw_level_card(self):

        self.section_line()

        self.draw_text(
            self.width / 2,
            self.username,
            span=SPAN_TITLE,
            font=self.font_username,
            fill=self.level_color,
            anchor=Position.CENTER,
        )

        self.section_line()

        if self.data_section is not False:
            y = self.update_y_cursor(SPAN_DATA, align=Position.DOWN)
            self.__draw_data_section(y)

        self.section_line()

        if self.bar_section is not False:
            y = self.update_y_cursor(SPAN_BAR)
            self.__draw_xp_bar(y, current_xp=self.bar_value, total_xp_level=self.bar_max)

        self.section_line()

        self.draw_multiline_text_in_center(
            self.width / 2,
            self.text,
            span=SPAN_TEXT,
            font=self.font_text,
            fill=self.text_color,
            align='center'
        )

        self.section_line()
