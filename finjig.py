#!/bin/python

from svgfig import *
from math import sqrt

class FinJig(object):
	def __init__(self, body_d = 0, fin_h = 0, fin_w = 0):
		if body_d == 0 or fin_h == 0 or fin_w == 0:
			self.getParams()
		else:
			self.body_d = float(body_d)
			self.body_r = 0.5 * float(self.body_d)
			self.fin_h = float(fin_h)
			self.fin_w = float(fin_w)
	def getParams(self):
		print("All units are in mm")
		self.body_d = float(input("Body diam: "))
		self.fin_h = float(input("Fin height: "))
		self.fin_w = float(input("Fin width: "))
		self.body_r = 0.5 * self.body_d
		
def makeJig(d, h, w):
	jig = FinJig(d, h, w)
	square = (2 * jig.fin_h + jig.body_d) + 20
	center = square/2
	edge = SVG("rect", cx=0, cy=0, width=square, height=square)
	body = SVG("circle", cx=center, cy=center, r=jig.body_r)
	#fin_off = jig.body_d/2 + jig.fin_h/2
	fin_offw = jig.fin_w / 2
	fins = []
	fins.append(SVG("rect", x=-fin_offw, y=jig.body_r, width=jig.fin_w, height=jig.fin_h, transform="rotate(0)"))
	fins.append(SVG("rect", x=-fin_offw, y=jig.body_r, width=jig.fin_w, height=jig.fin_h, transform="rotate(90)"))
	fins.append(SVG("rect", x=-fin_offw, y=jig.body_r, width=jig.fin_w, height=jig.fin_h, transform="rotate(180)"))
	fins.append(SVG("rect", x=-fin_offw, y=jig.body_r, width=jig.fin_w, height=jig.fin_h, transform="rotate(270)"))
	f = SVG("g", fins[0], fins[1], fins[2], fins[3], transform="translate({},{})".format(center,center))
	rocket = SVG("g", body, f, transform="rotate(45,{},{})".format(center,center))
	j = canvas(edge, rocket, height="{}mm".format(square), width="{}mm".format(square), viewBox="0 0 {} {}".format(square, square))
	j.save("jig.svg")
	j.inkview()

if __name__ == '__main__':
	import sys
	args = len(sys.argv)
	if args == 4:
		makeJig(sys.argv[1], sys.argv[2], sys.argv[3])
	elif args == 1:
		makeJig(0,0,0)
	else:
		print("Usage: {} [body_d, fin_h, fin_w]".format(sys.argv[0]))
	sys.exit(1)
