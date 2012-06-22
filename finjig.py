#!/usr/bin/env python

from math import sqrt, ceil, floor
from svgfig import *

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
		
def makeJig(n=0, d=0, h=0, w=0, outFile="jig.svg"):
	numPlates = int(floor(float(raw_input("Number of plates: "))))
	if (numPlates == "") or (numPlates < 1):
		numPlates = 2
	jig = FinJig(n, d, h, w)
	if jig.numFins < 2 or jig.numFins > 360:
		print("Number of fins must be between 2 and 360.")
		sys.exit(1)
	square = (2 * jig.fin_h + jig.body_d) + 20
	center = square/2
	edge = SVG("rect", cx=0, cy=0, width=square, height=square)
	body = SVG("circle", r=jig.body_r)
	fin_angle = 360 / jig.numFins
	fin_offw = jig.fin_w / 2
	fillet = jig.fin_w * 3
	fillet_x = -jig.fin_w
	fillet_y = jig.body_r - fillet * 0.707
	fins = []
	fillets = []
	for i in range(jig.numFins):
		fins.append(SVG("rect", x=-fin_offw, y=jig.body_r, width=jig.fin_w, height=jig.fin_h, transform="rotate({})".format(i * fin_angle)))
		fillets.append(SVG("rect", x=fillet_x, y=fillet_y, height=fillet, width=fillet, transform="rotate({},{},{}) rotate({},{},{})".format(fin_angle * i, 0, 0, 45, 0, fillet_y + jig.fin_w)))
	finset = SVG("g", *fins)
	filletset = SVG("g", *fillets)
	plates = []
	xpos = 0
	ypos = 0
	numPerRow = ceil(sqrt(numPlates))
	whole_x = (square + 2) * numPerRow
	whole_y = (square + 2) * ceil((numPlates / numPerRow))
	for i in range(1,numPlates+1):
		lugNotch = SVG("rect", x=-0.5, y=jig.body_r, width=1, height=2, transform="rotate({})".format(-fin_angle/2))
		rocket = SVG("g", body, finset, filletset, lugNotch, transform="translate({},{}) rotate({})".format(center,center, fin_angle/2))
		plates.append(SVG("g", edge, rocket, transform="translate({},{})".format(xpos, ypos)))
		if i % numPerRow == 0:
			xpos = 0
			ypos += square + 2	
		else:
			xpos += square + 2
	whole = canvas(*plates, height="{}mm".format(whole_y), width="{}mm".format(whole_x), viewBox="0 0 {} {}".format(whole_x, whole_y))
	whole.save(outFile)
	whole.inkview()

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
