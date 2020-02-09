import os
from pvlv_img_builder.configurations.configuration import (
    BACKGROUND_COLOR, LEVEL_COLOR, TEXT_COLOR,
    DIR_DEFAULT_FONT,
)
from PIL import ImageFont, Image, ImageDraw
from io import BytesIO
from math import ceil
from pvlv_img_builder.support import DrawSupport


"""                   
    +-----------------------------------------+  
    |              SPAN_BORDER                | span  |              
    +-----------------------------------------+       |                               
    |                                         | span  |                          
    |              SPAN_LEVEL                 | span  |  SPAN_LEVEL_SECTION                        
    |                                         | span  |                                                  
    +-----------------------------------------+       | 
    |              SPAN_BORDER                | span  | 
    +-----------------------------------------+                            
    |              SPAN_BOLD_TEXT             | span  
    |                                         | span                             
    +-----------------------------------------+            
    |              SPAN_TEXT                  | span                         
    +-----------------------------------------+     
    |              SPAN_BORDER                | span     at the end of all                        
    +-----------------------------------------+        
"""
SPAN_BORDER = 0.3
SPAN_LEVEL = 2
SPAN_BOLD_TEXT = 1
SPAN_TEXT = 1

SPAN_LEVEL_SECTION = SPAN_BORDER + SPAN_LEVEL + SPAN_BORDER


class DrawLevelUpCard(DrawSupport):

    def __init__(self, data):
        super().__init__(data)

        self.width = 350
        """
        :param data: is a dictionary look the documentation on the top of this file:
        """
        self.level, h, self.level_color = self.get_section('level', self.data, SPAN_LEVEL_SECTION, LEVEL_COLOR)
        self.height += h

        self.title, h, self.title_color = self.get_section('title', self.data, SPAN_BOLD_TEXT, LEVEL_COLOR)
        self.height += h

        self.text, h, self.text_lines, self.text_color = self.get_text('text', self.data, SPAN_TEXT, TEXT_COLOR)
        self.height += h

        self.height += SPAN_BORDER * self.y_resolution

        self.height = ceil(self.height)
        self.y_cursor = 0

        self.build_canvas()

        dir_path = os.path.dirname(os.path.realpath(__file__))
        self.font_dir = self.data.get('font', dir_path + DIR_DEFAULT_FONT)  # DIR_DEFAULT_FONT

        self.font_level = ImageFont.truetype(self.font_dir, int(self.y_resolution * SPAN_LEVEL))
        self.font_title = ImageFont.truetype(self.font_dir, int(self.y_resolution * SPAN_BOLD_TEXT / 1.3))
        self.font_text = ImageFont.truetype(self.font_dir, int(self.y_resolution * SPAN_TEXT / 2))

    def draw_level_up(self):

        if self.level is not False:
            self.y_cursor += (SPAN_LEVEL_SECTION / 2) * self.y_resolution
            self.draw_text(
                self.draw,
                self.width / 2,
                self.y_cursor,
                self.level,
                font=self.font_level,
                fill=self.level_color
            )
            self.y_cursor += (SPAN_LEVEL_SECTION / 2) * self.y_resolution

        if self.title is not False:
            self.y_cursor += (SPAN_BOLD_TEXT / 2) * self.y_resolution
            self.draw_text(
                self.draw,
                self.width / 2,
                self.y_cursor,
                self.title,
                font=self.font_title,
                fill=self.title_color
            )
            self.y_cursor += (SPAN_BOLD_TEXT / 2) * self.y_resolution

        if self.text is not False:
            self.y_cursor += (SPAN_TEXT * self.text_lines / 2) * self.y_resolution
            self.draw_multiline_text_in_center(
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
