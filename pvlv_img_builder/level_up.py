from pvlv_img_builder.configurations.configuration import (
    DEFAULT_BACKGROUND_COLOR, DEFAULT_LEVEL_COLOR, DEFAULT_TEXT_COLOR,
    DIR_DEFAULT_FONT,
)
from PIL import ImageFont
from io import BytesIO
from math import ceil
from pvlv_img_builder.support import DrawSupport
draw_support = DrawSupport()


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


class DrawLevelUpCard(object):

    def __init__(self, data):

        """
        :param data: is a dictionary look the documentation on the top of this file:
        """

        self.data = data

        self.y_resolution = 30
        self.width = 350
        self.height = 0

        self.level = str(self.data.get('level', False))
        if self.level is not False:
            self.height += SPAN_LEVEL_SECTION * self.y_resolution
        self.level_color = self.data.get('level_color', DEFAULT_LEVEL_COLOR)

        self.title = self.data.get('title', False)
        if self.title is not False:
            self.height += SPAN_BOLD_TEXT * self.y_resolution
        self.title_color = self.data.get('title_color', DEFAULT_LEVEL_COLOR)

        # add space for SPAN_TEXT
        self.text = self.data.get('text', False)
        if self.text is not False:
            self.text_lines = self.text.count('\n') + 1
            self.height += SPAN_TEXT * self.text_lines * self.y_resolution
        self.text_color = self.data.get('text_color', DEFAULT_TEXT_COLOR)

        self.height += SPAN_BORDER * self.y_resolution

        self.height = ceil(self.height)
        background_color = self.data.get('background_color', DEFAULT_BACKGROUND_COLOR)
        self.image = draw_support.create_image("RGB", self.width, self.height, background_color)
        self.draw = draw_support.create_draw(self.image)

        self.y_cursor = 0

        self.font_dir = self.data.get('font', DIR_DEFAULT_FONT)
        self.font_level = ImageFont.truetype(self.font_dir, int(self.y_resolution * SPAN_LEVEL))
        self.font_title = ImageFont.truetype(self.font_dir, int(self.y_resolution * SPAN_BOLD_TEXT / 1.3))
        self.font_text = ImageFont.truetype(self.font_dir, int(self.y_resolution * SPAN_TEXT / 2))

    def draw_level_up(self):

        if self.level is not False:
            self.y_cursor += (SPAN_LEVEL_SECTION / 2) * self.y_resolution
            draw_support.draw_text(
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
            draw_support.draw_text(
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
