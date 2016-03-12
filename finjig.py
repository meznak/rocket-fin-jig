#!/usr/bin/env python

from math import sqrt, ceil, floor
import copy
import svgwrite
import svgwrite.shapes as shapes

class FinJig(object):
    def __init__(self, *args):
        for i in args:
            if i == 0:
                self.get_params()
                return
        self.num_fins = int(floor(float(args[0])))
        self.body_d = float(args[1])
        self.body_r = 0.5 * float(self.body_d/2)
        self.fin_h = float(args[2])
        self.fin_w = float(args[3])
        self.num_plates = int(floor(float(args[4])))

    def get_params(self):
        self.num_fins = int(floor(input("Number of fins: ")))
        print("All units are in mm")
        self.body_d = float(input("Body diam: "))
        self.body_r = 0.5 * self.body_d
        self.fin_h = float(input("Fin height: "))
        self.fin_w = float(input("Fin width: "))
        self.num_plates = int(floor(float(raw_input("Number of plates: "))))

        
def make_jig(num_fins=0, diameter=0, height=0, width=0, num_plates=3, out_file="jig.svg"):
    if (num_plates < 1):
        num_plates = 3
    else:
        num_plates = int(num_plates)
        
    jig = FinJig(num_fins, diameter, height, width, num_plates)

    if jig.num_fins < 3 or jig.num_fins > 360:
        print("Number of fins must be between 3 and 360.")
        sys.exit(1)
    else:
        drawing = draw_jig(jig)
        draw_plates(jig, drawing, out_file)

def draw_jig(jig):
    """build a jig drawing"""
    
    # plate properties
    square = (2 * jig.fin_h + jig.body_d) + 20
    center = square / 2
    edge = shapes.Rect(size=(square,square), stroke="blue", stroke_width=1, fill="white")
    
    # body/fin properties
    body = shapes.Circle(center=(center, center), r=jig.body_r, stroke="black", stroke_width=1, fill="white")
    fin_offw = jig.fin_w / 2.0
    fin_offh = jig.fin_h + jig.body_r
    fin_angle = 360 / jig.num_fins
    
    cutout = svgwrite.container.Group()
    xfm = svgwrite.mixins.Transform
    
    cutout.add(edge)
    cutout.add(body)
    
    for i in range(jig.num_fins):
        fin = shapes.Rect(insert=(center - fin_offw, center - fin_offh), size=(jig.fin_w, jig.fin_h), stroke="black", stroke_width=1, fill="white")
        xfm.rotate(fin, angle = i * fin_angle, center=(center, center))
        cutout.add(fin)

    return cutout

def draw_plates(jig, cutout, out_file):

    # lay out plates
    xpos = 0
    ypos = 0
    
    square = (2 * jig.fin_h) + jig.body_d + 20
    center = square / 2

    num_per_row = ceil(sqrt(jig.num_plates))
    plate_width = square * num_per_row
    plate_height  = square * ceil((jig.num_plates / num_per_row))

    out = svgwrite.Drawing(out_file, (plate_width, plate_height))
    xfm = svgwrite.mixins.Transform
    
    for i in range(jig.num_plates):
        cutout_cp = copy.deepcopy(cutout)
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
    if args == 6:
        print 6
        make_jig(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5])
    elif args == 5:
        print 5
        make_jig(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], 3)
    elif args == 1:
        print 1
        make_jig()
    else:
        print("Usage: {} [num_fins, body_diameter, fin_height, fin_width] [num_plates] [out_file]".format(sys.argv[0]))
        sys.exit(1)
    sys.exit(0)
