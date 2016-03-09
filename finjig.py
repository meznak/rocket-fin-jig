#!/usr/bin/env python

from math import sqrt, ceil, floor
import svgwrite
import svgwrite.shapes as shapes

class FinJig(object):
	def __init__(self, *args):
		for i in args:
			if i == 0:
				self.getParams()
				return
		self.numFins = int(floor(float(args[0])))
		self.body_d = float(args[1])
		self.body_r = 0.5 * float(self.body_d/2)
		self.fin_h = float(args[2])
		self.fin_w = float(args[3])
	def getParams(self):
		self.numFins = int(floor(input("Number of fins: ")))
		print("All units are in mm")
		self.body_d = float(input("Body diam: "))
		self.body_r = 0.5 * self.body_d
		self.fin_h = float(input("Fin height: "))
		self.fin_w = float(input("Fin width: "))
		
def makeJig(n=0, d=0, h=0, w=0, out_file="jig.svg"):
	numPlates = int(floor(float(raw_input("Number of plates: "))))
	if (numPlates == "") or (numPlates < 1):
		numPlates = 2
	jig = FinJig(n, d, h, w)
	if jig.numFins < 2 or jig.numFins > 360:
		print("Number of fins must be between 2 and 360.")
		sys.exit(1)


        # plate properties
	square = (2 * jig.fin_h + jig.body_d) + 20
	center = square/2
	edge = shapes.Rect(size=(square,square), stroke="blue", stroke_width=1, fill="white")
                
        # body/fin properties
	body = shapes.Circle(center=(center, center), r=jig.body_r, stroke="black", stroke_width=1, fill="white")
        fin_offw = jig.fin_w / 2
        fin_offh = jig.fin_h
        fin = shapes.Rect(insert=(center - fin_offw, center - fin_offh), size=(jig.fin_w, jig.fin_h), stroke="black", stroke_width=5, fill="white")
	fin_angle = 360 / jig.numFins
	        
        # build a jig drawing
        dwg = svgwrite.Drawing()
        xfm = svgwrite.mixins.Transform

        dwg.add(edge)
        dwg.add(body)

        xfm.translate(fin, center, center)
        xfm.translate(fin, -fin_offw, -fin_offh)
        dwg.add(fin)
	# for i in range(jig.numFins - 1):
        #         xfm.rotate(fin, fin_angle, (center, center))
        #         dwg.add(fin)

                
        # lay out plates
	xpos = 0
	ypos = 0
	numPerRow = ceil(sqrt(numPlates))
	whole_x = (square + 2) * numPerRow
	whole_y = (square + 2) * ceil((numPlates / numPerRow))

        out = svgwrite.Drawing(out_file)

        out.add(dwg)
        # for i in range(1,numPlates+1):

        #         rocket = SVG("g", body, finset, transform="rotate({},{},{})".format(fin_angle/2,center,center))
	# 	plates.append(SVG("g", edge, rocket, transform="translate({},{})".format(xpos, ypos)))
	# 	if i % numPerRow == 0:
	# 		xpos = 0
	# 		ypos += square + 2	
	# 	else:
	# 		xpos += square + 2

                        

        out.save()

if __name__ == '__main__':
	import sys
	args = len(sys.argv)
	if args == 6:
		makeJig(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5])
	elif args == 5:
		makeJig(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
	elif args == 2:
		makeJig(0,0,0,0,sys.argv[1])
	elif args == 1:
		makeJig()
	else:
		print("Usage: {} [numFins, body_d, fin_h, fin_w] [outFile]".format(sys.argv[0]))
		sys.exit(1)
	sys.exit(0)
