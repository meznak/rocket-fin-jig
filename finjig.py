#!/usr/bin/env python

from math import sqrt, ceil, floor
import copy
import svgwrite
import svgwrite.shapes as shapes

class FinJig(object):
    def __init__(self, *args):
        self.cutout = svgwrite.container.Group()

        for i in args:
            if i == 0:
                self.get_params()
                return

        self.body_d = float(args[0])
        self.body_r = self.body_d / 2.0
        self.num_fins = int(floor(float(args[1])))
        self.fin_w = float(args[2])
        self.fin_h = float(args[3])
        self.name = args[4]
        self.num_plates = int(floor(float(args[5])))
        self.out_file = args[6]


    def get_params(self):
        self.num_fins = int(floor(input("Number of fins: ")))
        print("All units are in mm")
        self.body_d = float(input("Body diam: "))
        self.body_r = 0.5 * self.body_d
        self.fin_w = float(input("Fin width: "))
        self.fin_h = float(input("Fin height: "))
        self.name = raw_input("Name: ")
        self.num_plates = int(floor(float(raw_input("Number of plates: "))))
        self.out_file = raw_input("File name (.svg): ")


def make_jig(diameter=0, num_fins=0, width=0, height=0, name="^", num_plates=3, out_file="out.svg"):
    """Assemble fin jig"""
    if (num_plates < 1):
        num_plates = 3
    else:
        num_plates = int(num_plates)

    jig = FinJig(diameter, num_fins, width, height, name, num_plates, out_file)

    if jig.num_fins < 3 or jig.num_fins > 360:
        print("Number of fins must be between 3 and 360.")
        sys.exit(1)
    else:
        draw_jig(jig)
        draw_plates(jig)


def draw_jig(jig):
    """build a jig drawing"""

    stroke_width = 0.5

    # plate properties
    square = (2 * jig.fin_h + jig.body_d) + 20
    center = square / 2
    edge = shapes.Rect(size=(mm(square), mm(square)), stroke="blue", stroke_width=stroke_width, fill="white")
    text = svgwrite.text.Text(jig.name, insert=(mm(5), mm(10)))

    # body/fin properties
    body = shapes.Circle(center=(mm(center), mm(center)), r=mm(jig.body_r), stroke="black", stroke_width=stroke_width, fill="white")
    fin_x_pos = center - jig.fin_w / 2.0
    fin_y_pos = center - jig.fin_h - jig.body_r
    fin_angle = 360.0 / jig.num_fins

    # assemble cutout
    xfm = svgwrite.mixins.Transform

    jig.cutout.add(edge)

    xfm.scale(text, 5)
    jig.cutout.add(text)

    fin = svgwrite.container.Group()

    fillet_scale = 1.5
    fillet_x_pos = fin_x_pos + jig.fin_w * (1 - fillet_scale) / 2
    fillet_y_center = center - jig.body_r + 1
    fillet_y_pos = fillet_y_center - jig.fin_w * fillet_scale / 2

    fillet = shapes.Rect(insert=(mm(fillet_x_pos), mm(fillet_y_pos)), size=(mm(jig.fin_w * fillet_scale), mm(jig.fin_w * fillet_scale)), stroke="black", stroke_width=stroke_width, fill="white")
    xfm.rotate(fillet, angle = 45, center=(mm(center), mm(fillet_y_center)))

    fin.add(fillet)
    fin.add(shapes.Rect(insert=(mm(fin_x_pos), mm(fin_y_pos)), size=(mm(jig.fin_w), mm(jig.fin_h)), stroke="black", stroke_width=stroke_width, fill="white"))

    for i in range(jig.num_fins):
        new_fin = copy.deepcopy(fin)

        xfm.rotate(new_fin, angle = i * fin_angle, center=(mm(center), mm(center)))
        jig.cutout.add(new_fin)

    jig.cutout.add(body)


def draw_plates(jig):
    """Lay out the jig into multiple plates"""

    # lay out plates
    square = (2 * jig.fin_h) + jig.body_d + 20
    center = square / 2

    num_per_row = ceil(sqrt(jig.num_plates))
    plate_width = square * num_per_row
    plate_height  = square * ceil((jig.num_plates / num_per_row))

    out = svgwrite.Drawing(jig.out_file, (mm(plate_width), mm(plate_height)))
    xfm = svgwrite.mixins.Transform

    for i in range(jig.num_plates):
        cutout_cp = copy.deepcopy(jig.cutout)
        x_offset = i % num_per_row * square
        y_offset = floor(i / num_per_row) * square

        xfm.translate(cutout_cp, tx = mm(x_offset), ty = mm(y_offset))
        out.add(cutout_cp)

    out.save()


def mm(val):
    """Scale from px to mm"""
    return val * 3.543307


if __name__ == '__main__':
    import sys
    args = len(sys.argv)
    print args
    if args == 8:
        make_jig(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6], sys.argv[7])
    elif args == 7:
        make_jig(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6])
    elif args == 6:
        make_jig(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5])
    elif args == 1:
        make_jig()
    else:
        print("Usage: {} [body_diameter, num_fins, fin_width, fin_height, name] [num_plates] [out_file]".format(sys.argv[0]))
        sys.exit(1)
    sys.exit(0)
