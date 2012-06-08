#!/bin/python

from svgfig import *
from math import sqrt

class FinJig(object):
	def __init__(self, *args):
		for i in args:
			if i == 0:
				self.getParams()
				return
		self.numFins = int(args[0])
		self.body_d = float(args[1])
		self.body_r = 0.5 * float(self.body_d/2)
		self.fin_h = float(args[2])
		self.fin_w = float(args[3])
	def getParams(self):
		print("All units are in mm")
		self.numFins = int(input("Number of fins: "))
		self.body_d = float(input("Body diam: "))
		self.body_r = 0.5 * self.body_d
		self.fin_h = float(input("Fin height: "))
		self.fin_w = float(input("Fin width: "))
		
def makeJig(n=0, d=0, h=0, w=0, outFile="jig.svg"):
	numPlates = int(input("Number of plates: "))
	jig = FinJig(n, d, h, w)
	square = (2 * jig.fin_h + jig.body_d) + 20
	center = square/2
	wholeSize = square * 2
	edge = SVG("rect", cx=0, cy=0, width=square, height=square)
	body = SVG("circle", cx=center, cy=center, r=jig.body_r)
	fin_angle = 360 / jig.numFins
	fin_offw = jig.fin_w / 2
	fins = []
	for i in range(jig.numFins):
		fins.append(SVG("rect", x=-fin_offw, y=jig.body_r, width=jig.fin_w, height=jig.fin_h, transform="rotate({})".format(i * fin_angle)))
	finset = SVG("g", *fins, transform="translate({},{})".format(center,center))
	plates = []
	for i in range(numPlates):
		rocket = SVG("g", body, finset, transform="rotate({},{},{})".format(fin_angle/2,center,center))
		plates.append(SVG("g", edge, rocket))
	whole = canvas(*plates, height="{}mm".format(wholeSize), width="{}mm".format(wholeSize), viewBox="0 0 {} {}".format(wholeSize, wholeSize))
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
