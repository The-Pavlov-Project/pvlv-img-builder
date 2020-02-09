from pvlv_img_builder.configurations.configuration import (
    BACKGROUND_COLOR, TEXT_COLOR,
    DIR_DEFAULT_FONT,
    DEFAULT_BACKGROUND_BAR_COLOR, DEFAULT_BAR_COLOR,
)
from PIL import ImageFont
from io import BytesIO
from math import ceil
from pvlv_img_builder.utils.formatting import remap_range
from pvlv_img_builder.support import DrawSupport
draw_support = DrawSupport()


"""                   
    +-----------------------------------------+  
    |              SPAN_BORDER                | span  |              
    +-----------------------------------------+       |                               
    |              SPAN_TITLE                 | span  |  SPAN_TITLE_SECTION                         
    |                                         | span  |                                                                    
    +-----------------------------------------+       | 
    |              SPAN_BORDER                | span  |                         
    +-----------------------------------------+            
    |                                         | span  |                         
    |              SPAN_RANK                  |       |    
    |                                         | span  |  SPAN_RANK_SECTION                     
    +-----------------------------------------+       |
    |              SPAN_SEPARATOR             | span  |    
    +-----------------------------------------+  
    |              SPAN_TEXT                  | span                         
    +-----------------------------------------+  
    |              SPAN_BORDER                | span     at the end of all                        
    +-----------------------------------------+        

"""

SPAN_USERNAME = 1.6
SPAN_DATA = 1
SPAN_BAR = 0.8

SPAN_BORDER = 0.3
SPAN_TITLE = 1.6
SPAN_RANK = 0.8
SPAN_SEPARATOR = 0.8

SPAN_TEXT = 1

SPAN_TITLE_SECTION = SPAN_BORDER + SPAN_TITLE + SPAN_BORDER
SPAN_RANK_SECTION = SPAN_RANK + SPAN_SEPARATOR

"""
        +-+------+--------------------+---------------------+-+----------+-+            
        | |      |                    |                     | |          | |                      
   +--> | | RANK |      USERNAME      |    XP_BAR           | | LEVEL    | |      
   |    | |      |                    |                     | |          | |                   
   |    +-+------+--------------------+---------------------+-+----------+-+
OFFSET

"""
DIM_OFFSET = 0.5
DIM_RANK = 1.5
DIM_USERNAME = 8
DIM_XP_BAR = 6
DIM_LEVEL = 4


class DrawRanking(object):

    def __init__(self, data):

        """
        :param data: is a dictionary look the documentation on the top of this file:
        """

        self.data = data

        self.y_resolution = 30
        self.x_resolution = 30
        self.width = (DIM_OFFSET+DIM_RANK+DIM_USERNAME+DIM_XP_BAR+DIM_OFFSET+DIM_LEVEL+DIM_OFFSET)*self.x_resolution
        self.height = 0

        self.title = str(self.data.get('title', False))
        if self.title is not False:
            # reserve the space
            self.height += SPAN_TITLE_SECTION * self.y_resolution
            # get values
            self.title_color = self.data.get('title_color', TEXT_COLOR)

        self.rank_sections = []
        sections = self.data.get('rank', False)
        if sections is not False:
            # extract the sections and put them into an array
            for key in sections.keys():
                self.rank_sections.append(sections.get(key))
            # reserve the space
            self.height += SPAN_RANK_SECTION * self.y_resolution * len(self.rank_sections)

        # add space for SPAN_TEXT
        self.text = self.data.get('text', False)
        if self.text is not False:
            # the line of text will be added based on the line terminator
            self.text_lines = self.text.count('\n') + 1
            # reserve the space
            self.height += SPAN_TEXT * self.text_lines * self.y_resolution
            self.text_color = self.data.get('text_color', TEXT_COLOR)

        # last border in the end
        # reserve the space
        self.height += SPAN_BORDER * self.y_resolution

        # prepare the canvas
        # ceil the value to from float to decimal value, cause the img creation need int
        self.height = ceil(self.height)
        self.width = ceil(self.width)
        background_color = self.data.get('background_color', BACKGROUND_COLOR)
        self.image = draw_support.create_image("RGB", self.width, self.height, background_color)
        self.draw = draw_support.create_draw(self.image)

        self.y_cursor = 0

        # prepare dynamic fonts dimensions
        self.font_dir = self.data.get('font', DIR_DEFAULT_FONT)

        self.font_username = ImageFont.truetype(self.font_dir, int(self.y_resolution * SPAN_USERNAME / 1.4))
        self.font_data_value = ImageFont.truetype(self.font_dir, int(self.y_resolution * SPAN_DATA / 1.2))
        self.font_data_label = ImageFont.truetype(self.font_dir, int(self.y_resolution * SPAN_DATA / 2.2))
        self.font_xp_inside = ImageFont.truetype(self.font_dir, int(self.y_resolution * SPAN_BAR / 1.6))
        self.font_xp_values = ImageFont.truetype(self.font_dir, int(self.y_resolution * SPAN_BORDER * 1.6))
        self.font_text = ImageFont.truetype(self.font_dir, int(self.y_resolution * SPAN_TEXT / 2))

    def draw_xp_bar(self, y, x_start, x_end, current_xp, total_xp_level, bar_background_color, bar_color):
        """
        draw shadow frame of the xp bar
        draw the real xp bar
        draw the xp values
        """
        bar_dim_pixels = SPAN_RANK*self.y_resolution

        x_1 = x_start
        x_max = x_end
        x_2 = remap_range(current_xp, 0, total_xp_level, x_1, x_max)

        y_1 = y - bar_dim_pixels
        y_2 = y

        draw_support.draw_rectangle(self.draw, x_1, y_1, x_max, y_2, fill=bar_background_color)
        draw_support.draw_rectangle(self.draw, x_1, y_1, x_2, y_2, fill=bar_color)

        text_xp_inside = ' {} XP'.format(current_xp)
        w, h = draw_support.get_text_dimension(self.draw, text_xp_inside, font=self.font_xp_inside)
        if (x_2 - x_1) > w:
            _origin_x = 'left'
            _fill = bar_background_color
        else:
            _origin_x = 'right'
            _fill = bar_color

        draw_support.draw_text(
            self.draw,
            x_2,
            self.y_cursor - bar_dim_pixels/2,
            text_xp_inside,
            font=self.font_xp_inside,
            fill=_fill,
            origin_x=_origin_x,
        )

        _y_cursor_temp = self.y_cursor + SPAN_BORDER/1.9*self.y_resolution

        draw_support.draw_text(
            self.draw,
            x_max,
            y + self.y_resolution/4,
            '{} / {} XP'.format(current_xp, total_xp_level),
            font=self.font_xp_values,
            fill=self.text_color,
            origin_x='left',
        )

    def draw_rank_section(self, data):

        username = data.get('username', 'Anonymous')
        highlights = data.get('highlights', False)
        rank = data.get('rank', False)
        rank_label = data.get('rank_label', False)
        rank_color = data.get('rank_color', TEXT_COLOR)
        level = data.get('level', False)
        level_label = data.get('level_label', False)
        level_color = data.get('level_color', TEXT_COLOR)
        bar_value = data.get('value', False)
        bar_max = data.get('max', False)
        bar_color = data.get('color', DEFAULT_BAR_COLOR)
        bar_background_color = data.get('background_color', DEFAULT_BACKGROUND_BAR_COLOR)

        x_cursor = self.x_resolution*DIM_OFFSET

        if rank is not False:
            draw_support.draw_text(
                self.draw,
                x_cursor,
                self.y_cursor,
                ' #{}'.format(rank),
                font=self.font_data_value,
                fill=rank_color,
                origin_x='right',
                origin_y='up'
            )
        x_cursor += DIM_RANK * self.x_resolution

        if username is not False:
            draw_support.draw_text(
                self.draw,
                x_cursor,
                self.y_cursor,
                username,
                font=self.font_data_value,
                fill=rank_color,
                origin_x='right',
                origin_y='up'
            )
        x_cursor += DIM_USERNAME * self.x_resolution

        if bar_value is not False:
            self.draw_xp_bar(
                self.y_cursor,
                x_cursor,
                x_cursor + DIM_XP_BAR * self.x_resolution,
                current_xp=bar_value,
                total_xp_level=bar_max,
                bar_color=bar_color,
                bar_background_color=bar_background_color

            )
        x_cursor += DIM_XP_BAR * self.x_resolution
        x_cursor += self.x_resolution * DIM_OFFSET

        if level is not False:
            draw_support.draw_text(
                self.draw,
                x_cursor,
                self.y_cursor,
                '{}'.format(level_label),
                font=self.font_data_label,
                fill=level_color,
                origin_x='right',
                origin_y='up'
            )
            w, h = draw_support.get_text_dimension(self.draw, str(level_label), font=self.font_data_label)
            draw_support.draw_text(
                self.draw,
                x_cursor + w,
                self.y_cursor,
                ' {}'.format(level),
                font=self.font_data_value,
                fill=level_color,
                origin_x='right',
                origin_y='up'

            )

    def draw_ranking(self):

        if self.title is not False:
            self.y_cursor += (SPAN_TITLE_SECTION / 2) * self.y_resolution
            draw_support.draw_text(
                self.draw,
                self.width / 2,
                self.y_cursor,
                self.title,
                font=self.font_username,
                fill=self.title_color
            )
            self.y_cursor += (SPAN_TITLE_SECTION / 2) * self.y_resolution

        if self.rank_sections is not []:
            for el in self.rank_sections:
                self.y_cursor += SPAN_RANK * self.y_resolution
                self.draw_rank_section(el)
                self.y_cursor += SPAN_SEPARATOR * self.y_resolution

        if self.text is not False:
            self.y_cursor += (SPAN_TEXT * self.text_lines / 2) * self.y_resolution
            draw_support.draw_multiline_text_in_center(
                self.draw,
                self.width / 2,
                self.y_cursor,
                self.text,
                font=self.font_text,
                fill=self.text_color,
                align='center'
            )
            self.y_cursor += (SPAN_TEXT * self.text_lines / 2) * self.y_resolution

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