from pvlv_img_builder.configurations.configuration import (
    LEVEL_COLOR,
    TEXT_COLOR,
)
from PIL import ImageFont
from math import ceil
from pvlv_img_builder.support import DrawSupport, Position


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

        self.build_canvas()

        self.font_level = ImageFont.truetype(self.font_dir, int(self.y_resolution * SPAN_LEVEL))
        self.font_title = ImageFont.truetype(self.font_dir, int(self.y_resolution * SPAN_BOLD_TEXT / 1.3))
        self.font_text = ImageFont.truetype(self.font_dir, int(self.y_resolution * SPAN_TEXT / 2))

    def draw_level_up(self):

        self.draw_text(
            self.width / 2,
            self.level,
            span=SPAN_LEVEL_SECTION,
            font=self.font_level,
            fill=self.level_color
        )

        self.draw_text(
            self.width / 2,
            self.title,
            span=SPAN_BOLD_TEXT,
            font=self.font_title,
            fill=self.title_color
        )

        self.draw_multiline_text_in_center(
            self.width / 2,
            self.text,
            span=SPAN_TEXT,
            font=self.font_text,
            fill=self.text_color,
            align=Position.CENTER,
        )
