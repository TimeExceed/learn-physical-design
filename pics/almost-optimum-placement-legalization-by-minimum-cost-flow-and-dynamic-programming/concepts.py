from fathom import Point, ORIGIN, centroid
import fathom.tikz as tikz
import fathom.colors as colors
import fathom.line_styles as line_styles
import fathom.locations as locations
import fathom.corner_styles as corners
import fathom.geometry as geo
from itertools import *

def draw_zones(canvas, die, blockades):
    row_height = 1
    die = (die.vertices()[3], die.vertices()[1])
    blockades = [(x[3], x[1]) for x in (y.vertices() for y in blockades)]
    blockades.sort(key=lambda x:x[0].x)
    zones = []
    lower_y = 0
    while lower_y + row_height <= die[1].y:
        left_x = 0
        for b in blockades:
            if b[0].y <= lower_y < b[1].y:
                zone = geo.Rectangle(
                    lower_left=Point(left_x, lower_y),
                    upper_right=Point(b[0].x, lower_y + row_height),
                )
                zones.append(zone)
                canvas.new_line(
                    src=Point(left_x, lower_y),
                    dst=Point(b[0].x, lower_y),
                )
                left_x = b[1].x
        if left_x < die[1].x:
            zone = geo.Rectangle(
                lower_left=Point(left_x, lower_y),
                upper_right=Point(die[1].x, lower_y + row_height),
            )
            zones.append(zone)
            canvas.new_line(
                src=Point(left_x, lower_y),
                dst=Point(die[1].x, lower_y),
            )
        lower_y += row_height
    return zones

def draw_columns(canvas, die, blockades):
    col_width = 1
    die = (die.vertices()[3], die.vertices()[1])
    blockades = [(x[3], x[1]) for x in (y.vertices() for y in blockades)]
    blockades.sort(key=lambda x:x[0].y)
    x = col_width
    while x < die[1].x:
        lower_y = 0
        for b in blockades:
            if b[0].x <= x <= b[1].x:
                canvas.new_line(
                    src=Point(x, lower_y),
                    dst=Point(x, b[0].y),
                    line_style=line_styles.DASHED,
                )
                lower_y = b[1].y
        if lower_y < die[1].y:
            canvas.new_line(
                src=Point(x, lower_y),
                dst=Point(x, die[1].y),
                line_style=line_styles.DASHED,
            )
        x += col_width

if __name__ == '__main__':
    canvas = tikz.Canvas()

    die = canvas.new_rectangle(
        lower_left=ORIGIN,
        upper_right=Point(10, 10)
    ).get_skeleton()

    blockades = [
        canvas.new_rectangle(
            lower_left=Point(2, 3),
            upper_right=Point(3, 8),
            brush_color=colors.LIGHT_GRAY,
        ).get_skeleton(),
        canvas.new_rectangle(
            lower_left=Point(6, 6),
            upper_right=Point(8, 9),
            brush_color=colors.LIGHT_GRAY,
        ).get_skeleton(),
    ]

    zones = draw_zones(canvas, die, blockades)
    draw_columns(canvas, die, blockades)

    the_zone = [(x[3], x[1]) for x in (y.vertices() for y in zones)]
    the_zone = [x for x in the_zone if x[0].y < 6.5 < x[1].y and x[0].x < 4 < x[1].x][0]
    canvas.new_rectangle(
        lower_left=the_zone[0],
        upper_right=the_zone[1],
        pen_color=colors.BLUE,
    )
    zone_text = canvas.new_rectangle(
        center=Point(4.5, 5.5),
        width=1,
        height=0.5,
        pen_color=colors.INVISIBLE,
    ).get_skeleton()
    canvas.new_text(
        text='zone',
        anchor=zone_text.center(),
        pen_color=colors.BLUE,
    )
    canvas.new_line(
        src=zone_text,
        dst=the_zone[0],
        pen_color=colors.BLUE,
    )
    canvas.new_line(
        src=zone_text,
        dst=Point(the_zone[1].x, the_zone[0].y),
        pen_color=colors.BLUE,
    )
    region_text = canvas.new_rectangle(
        center=Point(4.5, 7.5),
        width=1,
        height=0.5,
        pen_color=colors.INVISIBLE,
    ).get_skeleton()
    canvas.new_text(
        text='region',
        anchor=region_text.center(),
        pen_color=colors.BLUE,
    )
    y = (the_zone[0].y + the_zone[1].y) / 2
    for x in islice(count(the_zone[0].x + 0.5, 1), 3):
        canvas.new_arrow(
            src=region_text,
            dst=Point(x,y),
            pen_color=colors.BLUE,
        )

    blk_text = canvas.new_rectangle(
        center=Point(12, 4),
        width=2,
        height=0.8,
        pen_color=colors.INVISIBLE,
    ).get_skeleton()
    canvas.new_text(
        text='blockades',
        anchor=blk_text.center(),
    )
    for b in blockades:
        canvas.new_arrow(
            src=blk_text,
            dst=b,
        )

    print(canvas.draw())
