#!/bin/python

from svgfig import *
from math import sqrt

class FinJig(object):
	def __init__(self, body_d = 0, fin_h = 0, fin_w = 0):
		self.body_d = body_d
		self.fin_h = fin_h
		self.fin_w = fin_w
		if self.body_d == 0 or self.fin_h == 0 or self.fin_w == 0:
			self.getParams()
	def getParams(self):
		self.body_d = float(input("Body diam: "))
		self.fin_h = float(input("Fin height: "))
		self.fin_w = float(input("Fin width: "))
		
def makeJig(d, h, w):
	jig = FinJig(d, h, w)
	square = (2 * jig.fin_h + jig.body_d) * 1.5
	center = square/2
	edge = SVG("rect", cx=0, cy=0, width=square, height=square)
	body = SVG("circle", cx=center, cy=center, r=jig.body_d/2)
	#fin_off = jig.body_d/2 + jig.fin_h/2
	fin_off = jig.body_d/2 + jig.fin_h
	fins = []
	fins.append(SVG("rect", x=fin_off, y=fin_off, width=jig.fin_w, height=jig.fin_h, transform="rotate(45)"))
	fins.append(SVG("rect", x=fin_off, y=fin_off, width=jig.fin_w, height=jig.fin_h, transform="rotate(-45)"))
	fins.append(SVG("rect", x=fin_off, y=fin_off, width=jig.fin_w, height=jig.fin_h, transform="rotate(45)"))
	fins.append(SVG("rect", x=fin_off, y=fin_off, width=jig.fin_w, height=jig.fin_h, transform="rotate(-45)"))
	f = SVG("g", fins[0], fins[1], fins[2], fins[3])
	rocket = SVG("g", body, f)
	j = canvas(edge, rocket, height=square, width=square, viewBox="0 0 {} {}".format(square, square))
	j.save("jig.svg")

if __name__ == '__main__':
	import sys
	args = len(sys.argv)
	if args == 4:
		makeJig(float(sys.argv[1]), float(sys.argv[2]), float(sys.argv[3]))
	elif args == 1:
		makeJig(0,0,0)
	else:
		print("Usage: %s [body_d, fin_h]", sys.argv[0])
	sys.exit(1)
