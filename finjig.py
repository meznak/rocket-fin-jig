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
        self.body_r = 0.5 * float(self.body_d/2)
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
    
    # plate properties
    square = (2 * jig.fin_h + jig.body_d) + 20
    center = square / 2
    edge = shapes.Rect(size=(square,square), stroke="blue", stroke_width=1, fill="white")
    marker = svgwrite.text.Text(jig.name, insert=(5,10))

    # body/fin properties
    body = shapes.Circle(center=(center, center), r=jig.body_r, stroke="black", stroke_width=1, fill="white")
    fin_offw = jig.fin_w / 2.0
    fin_offh = jig.fin_h + jig.body_r
    fin_angle = 360 / jig.num_fins
    
    # assemble cutout
    xfm = svgwrite.mixins.Transform

    jig.cutout.add(edge)
    jig.cutout.add(marker)
    jig.cutout.add(body)
    
    for i in range(jig.num_fins):
        fin = shapes.Rect(insert=(center - fin_offw, center - fin_offh), size=(jig.fin_w, jig.fin_h), stroke="black", stroke_width=1, fill="white")
        xfm.rotate(fin, angle = i * fin_angle, center=(center, center))
        jig.cutout.add(fin)

def draw_plates(jig):

    # lay out plates
    xpos = 0
    ypos = 0
    
    square = (2 * jig.fin_h) + jig.body_d + 20
    center = square / 2

    num_per_row = ceil(sqrt(jig.num_plates))
    plate_width = square * num_per_row
    plate_height  = square * ceil((jig.num_plates / num_per_row))

    out = svgwrite.Drawing(jig.out_file, (plate_width, plate_height))
    xfm = svgwrite.mixins.Transform
    
    for i in range(jig.num_plates):
        cutout_cp = copy.deepcopy(jig.cutout)
        x_offset = i % num_per_row * square
        y_offset = floor(i / num_per_row) * square
            
        xfm.translate(cutout_cp, tx = x_offset, ty = y_offset)
        out.add(cutout_cp)

        
        # if i % numPerRow == 0:
        #     xpos = 0
        #     ypos += square + 2    
        # else:
        #     xpos += square + 2

    out.save()

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
