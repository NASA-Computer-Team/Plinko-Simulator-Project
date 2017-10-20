from tkinter import *
import random
import math
import time

canStop = True
tests = 60
showChi = False
print("Leave blank if you want to run continuously")

try:
	beans = int(input("How many beans?: "))
except ValueError:
	beans = 0
	canStop = False
#if canStop:
if (input("Show Chi?(Y/N): ").upper() != "N"):
	showChi = True
	try:
		tests = int(input("Test Interval?: "))
	except ValueError:
		tests = 10
try:
	bias = int(input("Left-Bias Percentage? (0-100): "))/100
except ValueError:
	bias = 0.5


print("Initializing...")
time.sleep(1)
print("Please Wait While We Setup...")

#showChi = canStop

root = Tk()

layers = 14
fps = 60
count = 0


_w = 500
_h = ((_w/(((layers-1)/((layers/2)-1))))*(3**(1/2)))
topMargin = 50
bottomMargin = 150
leftMargin = (_w/(layers+4))
if showChi:
	rightMargin = 500
else:
	rightMargin = (_w/(layers+4))
w = _w + leftMargin + rightMargin
h = _h + topMargin + bottomMargin







c = Canvas(root, width=w, height=h)
c.pack()


class circle(object):
	def __init__(self, *args, **kwargs):
		self.x, self.y, self.r = args
		self.c = 'black'
		self.id = c.create_oval(self.x-self.r, self.y-self.r, self.x+self.r, self.y+self.r, fill=self.c)
def makeLine(pts):
	isFirst = True
	y0 = 0
	for (i, y) in pts:
		if isFirst:
			i = 0
			y0 = y
			isFirst = False
		else:
			yield i, y0, y
			y0 = y
class rect(object):
	def __init__(self, *args, **kwargs):
		x, y, w, h = args
		self.c = kwargs.get('fill')
		self.id = c.create_rectangle(x, y, x+w, y+h, fill=self.c)
def perc(p):

	return((random.random())<p)
def Sum(vals):
	val = 0
	for i in range(len(vals)):
		val += vals[i]
	return val
def Chi_Squared(observed, expected):
	chi_vals = []
	for i in range(len(observed)):
		chi_vals.append(math.pow(observed[i]-expected[i], 2)/expected[i])
	return Sum(chi_vals)
def Map(Input, min1, max1, min2, max2):
	return ((((Input-min1)/(max1-min1)))*(max2-min2))+min2



class Bean(object):
	def __init__(self):
		self.sums = [0]
		self.chi = []
		self.chiO = []
		self.chiE = []
		self.fac = []
		self.count = 0
		self.Chi = 0
		self.path = [0]
		self.dmin = 0
		self.dmax = 1
		self.Count = 0
		L = layers
		i = 0
		self.playing = True
		while i <= layers:
			self.sums.append(0)
			i+=1
		for i in range(L+1):
			self.fac.append(math.factorial(layers)/(math.factorial(i)*math.factorial(layers-i)))
			self.chiO.append(0)
		M = max(self.fac)
		for i in range(len(self.fac)):
			self.chiE.append(self.fac[i]/M)

	def go(self):
		if (self.playing):
			self.path = [0]

		self.spot = 0
		self.pspot = 0
		l = 0
		L = layers
		_W = _w/(2*L)
		while l <= layers:
			self.path.append(int(perc(bias)))
			self.spot += self.path[l]
			l+=1
			i = 0
			if (l <= layers):
				while i < l:
					circle((leftMargin+(_W*(L-(l-1)+(2*i)))), (topMargin+((l-1)*_h/(L-1))), 5)
					i+=1
				if l>1:
					c.create_line(leftMargin+(_W*(L-(l-2)+(2*self.pspot))), topMargin+((l-2)*_h/(L-1)), leftMargin+(_W*(L-(l-1)+(2*self.spot))), topMargin+((l-1)*_h/(L-1)))
			self.pspot = self.spot
			if (l==layers+1):
				if self.playing:
					self.sums[self.spot] += 1


	def get_rects(self):
		_m = max(self.sums)
		
		L = layers
		if self.playing:
			for i in range(L+1):
				self.chiO[i] = self.sums[i]/_m

		_W = _w/(2*L)
		m = 0
		S = len(self.sums)
		for m in range(S):
			if (m < S-1):
				if (m < S-2):
					c.create_line(leftMargin+(_W*(2*m)), h-((bottomMargin*4/5)*self.chiO[m]), leftMargin+(_W*(2*(m+1))), h-((bottomMargin*4/5)*self.chiO[m+1]), fill="blue")
					if bias == 0.5:
						c.create_line(leftMargin+(_W*(2*m)), h-((bottomMargin*4/5)*self.chiE[m]), leftMargin+(_W*(2*(m+1))), h-((bottomMargin*4/5)*self.chiE[m+1]), fill="red")
				c.create_text(leftMargin+(_W*(2*m)), h-(bottomMargin*4/5)-6, text=self.sums[m])
	
	def getChi(self):
		Chi = Chi_Squared(self.chiO, self.chiE)
		Chi = int(Chi*1000)
		self.Chi = Chi/1000

		if self.Chi > self.dmax:
			self.dmax = self.Chi
		elif self.Chi < self.dmin:
			self.dmin = self.Chi

		if self.playing:
			if ((self.count%tests) == 0):
				self.chi.append((self.Count, Map(-math.log(self.Chi, 10), 0, 2, topMargin, h-(bottomMargin*4/5))))
				self.Count += 1

		#Map(self.count/tests, 0, beans/tests, _w+leftMargin+30, w-30)
		for (i, y0, y1) in makeLine(self.chi):
			if canStop:
				if i < (beans/tests):
					c.create_line(Map(i, 0, beans/tests, _w+leftMargin+30, w-30), y0, Map(i+1, 0, beans/tests, _w+leftMargin+30, w-30), y1, fill='blue')
			else:
				if i < (bean.count/tests):
					c.create_line(Map(i, 0, bean.count/tests, _w+leftMargin+30, w-30), y0, Map(i+1, 0, bean.count/tests, _w+leftMargin+30, w-30), y1, fill='blue')
		


		c.create_line(_w+leftMargin+30, topMargin, _w+leftMargin+30, h-(bottomMargin*4/5)+20)
		c.create_line(_w+leftMargin+10, h-(bottomMargin*4/5), w-30, h-(bottomMargin*4/5))
		c.create_text(_w+leftMargin+23, topMargin, text="10", anchor="e")
		c.create_text(_w+leftMargin+28, topMargin-5, text="0", anchor="e")
		c.create_line(_w+leftMargin+30, topMargin, _w+leftMargin+35, topMargin)

		c.create_text(_w+leftMargin+23, (topMargin+h-(bottomMargin*4/5))/2, text="10", anchor="e")
		c.create_text(_w+leftMargin+28, ((topMargin+h-(bottomMargin*4/5))/2)-7, text="-1", anchor="e")
		c.create_line(_w+leftMargin+30, ((topMargin+h-(bottomMargin*4/5))/2), _w+leftMargin+35, ((topMargin+h-(bottomMargin*4/5))/2))

		c.create_text(_w+leftMargin+23,  h-(bottomMargin*4/5), text="10", anchor="se")
		c.create_text(_w+leftMargin+28,  h-(bottomMargin*4/5)-17, text="-2", anchor="e")
		c.create_line(_w+leftMargin+30, h-(bottomMargin*4/5)-5, _w+leftMargin+35, h-(bottomMargin*4/5)-5)


		c.create_text((_w+leftMargin+10+w-30)/2, h-(bottomMargin*4/5)+5, text="Chi-Squared Test of Galton Box Measurements", anchor="n")
		if canStop:
			c.create_text(w-30, h-(bottomMargin*4/5)+5, text=beans, anchor="ne")
		else:
			c.create_text(w-30, h-(bottomMargin*4/5)+5, text=bean.count, anchor="ne")

		




		

bean = Bean()

def draw_pegs():
	l = 0
	L = layers
	_W = _w/(2*L)
	while l < layers:
		l += 1
		i = 0
		while i < l:
			circle((leftMargin+(_W*(L-(l-1)+(2*i)))), (topMargin+((l-1)*_h/(L-1))), 5)
			i+=1

def add_bean(event):
	global beans
	bean.playing = True
	beans += 1

def toggle_play(event):
	if bean.playing:
		bean.playing = False
	else:
		bean.playing = True

def draw():
	c.delete(ALL)

	if showChi:
		bean.getChi()
		c.create_text(10, 10, text="Chi Squared: %s" %bean.Chi, anchor="w")
	bean.go()
	bean.get_rects()

	global beans
	global count
	if bean.playing:
		if bean.count == beans-1: 
			if (canStop):
				bean.playing = False
		bean.count += 1

	
	c.create_text(10, 20, text="Count: %s" %bean.count, anchor="w")




	root.after(int(1000/fps), draw)
draw()

root.bind("<Button-1>", add_bean)
root.bind("<Button-3>", toggle_play)

root.mainloop()
