from tkinter import *
import random
import math
import time
import sys
import os

canStop = True
tests = 60          #misnomer. Every 60, the chi squared graph adds a point
showChi = False
print("Leave blank if you want to run continuously")


#if the user input is an integer, set number of beans to that number, otherwise set beans to 0
#setting beans to 0 is my way of telling the program that I am running in "non-stop" mode
try:
	beans = int(input("How many beans?: "))
	#canStop is True by default
except ValueError:
	beans = 0
	canStop = False


#if the user inputs "N" or "n", then do not show the Chi Squared graph
if (input("Show Chi?(Y/N): ").upper() != "N"):
	#otherwise show the graph...
	showChi = True
	#... and if the input to the "Test Interval" question is an integer, set the number of tests to that number ...
	try:
		tests = int(input("Test Interval?: "))
	except ValueError:
		#... otherwise set the number of tests to 10
		tests = 10


#if user input to the left-bais is an int, set left-bias to that int, otherwise set it to 0.5
#Left-bias is a simple way of saying that "bias"% of the beans bounce left, and (100-bias)% of the beans bounce right
try:
	bias = int(input("Left-Bias Percentage? (0-100): "))/100
except ValueError:
	bias = 0.5


#Fluff. Just so user can see their inputs and computer has time to launch window without stalling
print("Initializing...")
time.sleep(1)
print("Please Wait While We Setup...")



root = Tk() #root is the main Tkinter window

layers = 14 #how many layers are in the triangle of pegs
fps = 60    #just for display, if computers have stutering issues, lower the fps here. fps also dictates calculation cycle time, so program stalls until the wait-time is done
count = 0   #TODO-explain count


_w = 500     #width, in pixels, from the leftmost peg to the rightmost peg
_h = ((_w/(((layers-1)/((layers/2)-1))))*(3**(1/2))) 
topMargin = 50 #space, in pixels, from the top of the window to the top-most peg
bottomMargin = 150 #space, in pixels, form the bottom-most peg to the bottom of the window
leftMargin = (_w/(layers+4)) #make space on left side of peg board, designed to fit the peg board and the graph underneath

#make space to the right of the pegboard...
if showChi:
	#... to fit the chi squared graph ...
	rightMargin = 500 #500px
else:
	#... to have same space as left margin but on the right
	rightMargin = (_w/(layers+4))

w = _w + leftMargin + rightMargin #w is the width of the window
h = _h + topMargin + bottomMargin #h is the height of the window


'''
+------+-----------------------+------+
|      |                       |      |
|      |                       |      |
|      |           o           |      |
|      |          o o          |      |
|      |         o o o         |      |
|      |        o o o o        |      |
|   M  |       o o o o o       | R  M |
| L A  |      o o o o o o      | I  A |
| E R  |     o o o o o o o     | G  R |
| F G  |    o o o o o o o o    | H  G |
| T I  |   o o o o o o o o o   | T  I |
|   N  |  o o o o o o o o o o  |    N |
|      | o o o o o o o o o o o |      |
|      |o o o o o o o o o o o o|      |
|      o o o o o o o o o o o o o      |
|      |                       |      |
|      |                       |      |
+------+-----------------------+------+
leftMargin    +    _w     +     rightMargin    =   w


+-------------------------------------+
|                 TOP                 |  topMargin
|               MARGIN                |
+------------------o------------------+
|                 o o                 |   +
|                o o o                |
|               o o o o               |
|              o o o o o              |
|             o o o o o o             |
|            o o o o o o o            |  _h
|           o o o o o o o o           |
|          o o o o o o o o o          |
|         o o o o o o o o o o         |  
|        o o o o o o o o o o o        |  +
|       o o o o o o o o o o o o       |
+------o o o o o o o o o o o o o------|
|               BOTTOM                |  bottomMargin
|               MARGIN                |
+-------------------------------------+  = h

'''





c = Canvas(root, width=w, height=h) #make a canvas with size width:w, height:h
c.pack() #put Canvas c into the window


#easy way of circumventing the way tkinter draws circles. Give inputs as (center x, center y, radius)
class circle(object):
	def __init__(self, *args, **kwargs):
		self.x, self.y, self.r = args
		self.c = 'black' #change this for default color of circle
		self.id = c.create_oval(self.x-self.r, self.y-self.r, self.x+self.r, self.y+self.r, fill=self.c)


#takes a list of tuples of (index, y-point), and returns a list of tuples of (index "i" of point, y[i], y[i+1])
'''
example: 
>>> ys = [(0, 10), (1, 30), (2, 20), (3, 70), (4, 50), (5, 40), (6, 30), (7, 90), (8, 50), (9, 00), (10, 60)]
>>> lines = makeLine(ys)
>>> print(lines)
[(0, 10, 30), (1, 30, 20), (2, 20, 70), (3, 70, 50), (4, 50, 40), (5, 40, 30), (6, 30, 90), (7, 90, 50), (8, 50, 00), (9, 00, 60)]
'''
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


#way of circumventing tkinter's rectangle method, draws rectangle given (x, y, width, height), with optional argument for color
class rect(object):
	def __init__(self, *args, **kwargs):
		x, y, w, h = args
		self.c = kwargs.get('fill')
		self.id = c.create_rectangle(x, y, x+w, y+h, fill=self.c)


#returns True approximately p% of the time
#generates a random number 0-1, and returns True if the number is less than p
def perc(p):
	return((random.random())<p)


#returns the sum of all the values in the list
def Sum(vals):
	val = 0
	for i in range(len(vals)):
		val += vals[i]
	return val


#Look up Chi Squared test, basically shows how close a generated set of points is to the expected points
def Chi_Squared(observed, expected):
	chi_vals = []
	for i in range(len(observed)):
		chi_vals.append(math.pow(observed[i]-expected[i], 2)/expected[i])
	return Sum(chi_vals)


#maps the input from the range min1-max1 over to the range of min2-max2 by scaling and shifting
#if the number is outside range, then it is also scaled outside range
def Map(Input, min1, max1, min2, max2):
	return ((((Input-min1)/(max1-min1)))*(max2-min2))+min2




class Bean(object):
	def __init__(self):
		self.sums = [0] #start off with one bottom output count
		self.chi = []   #list of points to plot for the Chi Squared graph
		self.chiO = []  #list of observed values (values generated by board)
		self.chiE = []  #list of expected values for each "cup" under the board
		self.fac = []   #list of binomial distributions (n k)
		self.count = 0  #how many beans have been run
		self.Chi = 0    #current Chi Squared value
		self.path = [0] #HINT TO START CHANGE FOR UPDATE: CHANGE HOW THIS WORKS
		self.dmin = 0   #keeps track of smallest chi value
		self.dmax = 1   #keeps track of largest chi value
		self.Count = 0  #DIFFERENT THAN self.count, keeps track of how many chi points to display
		L = layers      #another name for layers, mostly for time saving. Feel free to change all the Ls to layers for ease of reading
		i = 0           #honestly this is just for the while loop, but you can change the while loop to a for loop with an escape condition to end the for loop
		
		self.playing = True  #auto start ball dropping
		
		#this is the while loop I referred to in the "i = 0" comment
		while i <= layers:
			self.sums.append(0)
			i+=1

		#fill the self.fac list with binomial distributions
		#this is because the gaussian curve can be modelled by mapping the binomial distributions to the scale from 0 to the largest bi_dist.
		for i in range(L+1):
			self.fac.append(math.factorial(layers)/(math.factorial(i)*math.factorial(layers-i)))
			'''
			/ n \        n!
			|   |  = --------- = (n _ k)
			\ k /    k! (n-k)!

			pushes (layers _ i) to self.fac
			'''
			self.chiO.append(0) #fill chiO with 0 to start all observed values to 0, since all counts of the "cups" is 0

		M = max(self.fac) #largest bi_dist
		for i in range(len(self.fac)):
			self.chiE.append(self.fac[i]/M) #set expected values to the scaled bi_dist values
	
	#main method for updating
	def go(self): #takes no parameters
		
		L = layers
		_W = _w/(2*L) #I will explain why this is the way it is. 

		########################### Change this to do row by row updating, my comments here will be on what was intended to happen, but it is your job to figure out how to change it. 
		
		if (self.playing):       #If beans are being dropped ...
			self.path = [0]  #... set this bean's path to have its first layer position as 0

		self.spot = 0
		self.pspot = 0
		l = 0

		
		'''
		pegboard can be seen as this triangular pattern, where the number indicates the peg's position in the layer
		                   0
		                 0   1
		               0   1   2
		             0   1   2   3
		           0   1   2   3   4
		         0   1   2   3   4   5
		       0   1   2   3   4   5   6
		     0   1   2   3   4   5   6   7
		   0   1   2   3   4   5   6   7   8

		|_| |_| |_| |_| |_| |_| |_| |_| |_| |_|
		 0   1   2   3   4   5   6   7   8   9

		At each layer, the bean has a position P. 
		In the next layer, the bean can only have one of two positions, P or P+1 (see diagram as to why)
		Therefore, when updating the path, we can either add 0 or 1 to the previous path.
		By the time the bean gets to the last layer, it will need one more update to put it into a specific cup.
		Add 1 to that cup in self.sums


		'''
		
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
		########################### 

	
	#method to display the rectangles
	def get_rects(self):        #I will need to explain the MESS in the create_line functions, unless you can figure it out, but that is highly unlikely.
		_m = max(self.sums)
		
		L = layers
		if self.playing:
			for i in range(L+1):
				self.chiO[i] = self.sums[i]/_m

		_W = _w/(2*L) #I will explain why this is the way it is. 
		m = 0
		S = len(self.sums)
		for m in range(S):
			if (m < S-1):
				if (m < S-2):
					c.create_line(leftMargin+(_W*(2*m)), h-((bottomMargin*4/5)*self.chiO[m]), leftMargin+(_W*(2*(m+1))), h-((bottomMargin*4/5)*self.chiO[m+1]), fill="blue")
					if bias == 0.5: #only show the bell curve if bias is 0.5
						c.create_line(leftMargin+(_W*(2*m)), h-((bottomMargin*4/5)*self.chiE[m]), leftMargin+(_W*(2*(m+1))), h-((bottomMargin*4/5)*self.chiE[m+1]), fill="red")
				c.create_text(leftMargin+(_W*(2*m)), h-(bottomMargin*4/5)-6, text=self.sums[m])
	


	#method to display the chi squared graph with a logarithmic scale
	#This part, honestly just let me teach it to you personally because there is no easy explanation for this part without showing in person what it does
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

		
def restart(event):
	python = sys.executable
	os.execl(python, python, *sys.argv)



		

bean = Bean() #initialize a variable bean as the Bean class


#draws the pegs on the screen
def draw_pegs():

	#Possibly change to a for loop??? I do not remember why I made this a while loop.
	#if you do make it a for loop, make sure to make it start at 1, not 0
	l = 0
	L = layers
	_W = _w/(2*L) #I will explain why this is the way it is. 
	#Hint though if you want a challenge, it has to do with the pegs in the layer above being in the middle of the pegs on the current layer.   
	while l < layers:
		l += 1
		i = 0
		while i < l: #only put as many pegs as the number of the layer
			circle((leftMargin+(_W*(L-(l-1)+(2*i)))), (topMargin+((l-1)*_h/(L-1))), 5)
			i+=1


#really only used because tkinter has no support for in-line multi-line function definitions
def add_bean(event):
	global beans
	bean.playing = True #if the simulation is stopped, make it run
	beans += 1          #add 1 to the total bean count


#Ask Nihal about the "continual run after end" bug, and try to figure out why it happens. 
def toggle_play(event):
	#it seems innocent enough
	if bean.playing:             #if the simulation is running... 
		bean.playing = False #... pause it ...
	else:                        #... otherwise ...
		bean.playing = True  #... make it play
	

#MAIN LOOP
def draw():
	c.delete(ALL)          #Clears canvas of everything that was on layer in last frame

	if showChi:            #if showChi is true... 
		bean.getChi()  #... run bean.getChi
		c.create_text(10, 10, text="Chi Squared: %s" %bean.Chi, anchor="w")

	bean.go()         #UPDATE 
	bean.get_rects()  #displsay the rectangles

	global beans
	global count
	if bean.playing:
		if bean.count == beans-1:             #This whole logic will need to be changed. Otherwise, simulation will stop entirely when the last bean is dropped onto the first peg
			if (canStop):
				bean.playing = False
		bean.count += 1

	
	c.create_text(10, 20, text="Count: %s" %bean.count, anchor="w") #Display number of beans >DROPPED<, not collected



	root.after(int(1000/fps), draw) #after a certain amount of milliseconds, call draw() again, in effect looping the program

draw() #start


root.bind("x", restart)                 #Binds the keyboard key "x" to the restart function. If this still works, great! If it doesn't, the problem isnt here, it's in the restart function.
root.bind("<Button-1>", add_bean)       #Binds the left mouse button to the add_bean function. If there is an error, it will be in add_bean, not here
root.bind("<Button-3>", toggle_play)    #Binds the right mouse button to the toggle_play function. If there is an error (HINT HINT), it will be in toggle_play 

root.mainloop() #This is just necessary for tkinter. dont touch this. If you do end up adding another TK window (please do not, you will drown in a puddle of sadness and self loathing)
