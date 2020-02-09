from PIL import ImageFont
from pvlv_img_builder.draw_support import DrawSupport
from pvlv_img_builder.utils.positions import Position
from pvlv_img_builder.utils.formatting import remap_range
from pvlv_img_builder.configurations.configuration import (
    BAR_A_COLOR,
    BAR_B_COLOR,
    BAR_XP_INSIDE_A_COLOR,
    BAR_XP_INSIDE_B_COLOR,
)


"""
    +-----------------------------------------+ 
    |              SPAN_VOID                  | span                           
    +--+-----------------------------------+--+         
    |  |           SPAN_BAR                |  | span  
    +--+-----------------------------------+--+
    |              SPAN_XP_DATA               | span                         
    +-----------------------------------------+  
"""

SPAN_VOID = 0.5
SPAN_BAR = 1
SPAN_DATA = 0.5


class LevelUtils(DrawSupport):
    def __init__(self, data):
        super().__init__(data)

        # get values
        self.bar_section = data.get('bar')

        self.bar_value = self.bar_section.get('value')
        self.bar_max = self.bar_section.get('max')
        self.bar_color = self.bar_section.get('bar_color', BAR_A_COLOR)
        self.bar_background_color = self.bar_section.get('bar_background_color', BAR_B_COLOR)
        self.inside_xp_dark_color = self.bar_section.get('inside_xp_dark_color', BAR_XP_INSIDE_A_COLOR)
        self.inside_xp_light_color = self.bar_section.get('inside_xp_light_color', BAR_XP_INSIDE_B_COLOR)

        self.font_xp_bar_text = ImageFont.truetype(self.font_dir, int(self.y_resolution * SPAN_BAR / 1.6))
        self.font_xp_data = ImageFont.truetype(self.font_dir, int(self.y_resolution * SPAN_DATA / 1.2))

    def draw_xp_bar(self, xy_box, current_xp, total_xp_level):
        """
        draw shadow frame of the xp bar
        draw the real xp bar
        draw the xp values
        """
        # recalculate the y_resolution based on the span allocated for the xp bar
        coords_1 = xy_box[0]
        coords_2 = xy_box[1]

        x_1 = coords_1[0]  # start of xp bar (get x from coords)
        x_max = coords_2[0]  # end of xp bar (get x from coords)
        x_2 = remap_range(current_xp, 0, total_xp_level, x_1, x_max)  # xp bar by points

        # recalculate the y_resolution and y center based on the span allocated for the xp bar
        y_resolution = (coords_2[1] - coords_1[1]) / (SPAN_VOID + SPAN_BAR + SPAN_DATA)

        y_1 = coords_1[1] + SPAN_VOID * y_resolution
        y_2 = y_1 + SPAN_BAR * y_resolution

        self.draw.rectangle([(x_1, y_1), (x_max, y_2)], fill=self.bar_background_color)
        self.draw.rectangle([(x_1, y_1), (x_2, y_2)], fill=self.bar_color)

        xp_bar_text = ' {} XP '.format(current_xp)
        w, h = self.get_text_dimension(xp_bar_text, font=self.font_xp_bar_text)

        """
        Check if the text in longer than the bar.
        If yes move the text on the other side of the bar.
        """
        if (x_2 - x_1) > w:
            _origin_x = Position.LEFT
            _fill = self.inside_xp_dark_color
        else:
            _origin_x = Position.RIGHT
            _fill = self.inside_xp_light_color

        self.draw_text(
            x_2,
            xp_bar_text,
            y=y_1 + (y_2 - y_1)/2,
            font=self.font_xp_bar_text,
            fill=_fill,
            origin_x=_origin_x,
        )

        y = y_2 + SPAN_DATA / 2 * y_resolution

        self.draw_text(
            x_max,
            '{} / {} XP'.format(current_xp, total_xp_level),
            y=y,
            font=self.font_xp_data,
            fill=self.inside_xp_light_color,
            origin_x='left',
        )

