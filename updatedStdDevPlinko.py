import time
import random
import math

random.seed()

#if these two values mutiplied together is "too big", it will take a long time to run the program
#both values have an effect on the result
balls = int(input("How many balls?"))
#must be 10 layers as the new format forces a predeclared empty dictionary
layer = 10
print("Ideal: 1s    2s    3s")
print("     68%   95%   99.7%\n")
print("Calculating...\n")
time.sleep(1)


#simulate the action of going down the plinko board.
def generate(max):

  #the starting position of the ball
  instance = 0

  #loop through every layer of the board
  for i in range(1, max):

      #randomly determine whether the ball goes to the left or to the right
      x = random.randint(0,1)
      if x == 1:
        instance += 1

  #return the postion of the balls
  
  return instance


#find the mean of the result 
def mean(list):

    total = 0
    count = 0
    for i in range(0, len(list)):
        total += i*list[i]
        count += list[i]

    mean = total/count
    return mean

#find the standard deviation of the result
def standDev(list):

    sum = 0
    m = mean(list)
    count = 0
    for i in range(0, len(list)):
      count += list[i]
      for j in range(0, list[i]):
        sum += (i-m)**2

    sx = math.sqrt(sum/(count-1))

    return sx

#excute the simulation
posList = {0:0, 1:0, 2:0, 3:0, 4:0, 5:0, 6:0, 7:0, 8:0, 9:0}
#force the list to have more than one ball in it at the beginning so standard deviation can be calculated.
r = generate(layer)
posList[r] = posList[r] + 1

#loop through each ball
for i in range(2, balls+1):
  s1 = 0 
  s2 = 0 
  s3 = 0 
  
  #add the ball into the resulting list and calulate the new mean and standard deviation
  r = generate(layer)
  posList[r] = posList[r] + 1
  m = mean(posList)
  sd = standDev(posList)
  
  #loop through all the positions
  for j in range(0, layer):
  
    #calculate the amount of balls within 1 standard deviation of the mean
    if j < (m + sd) and j > (m - sd):
      s1 += posList[j]
      
    #calculate the amount of balls within 2 standard deviation of the mean
    if j < (m + sd*2) and j > (m - sd*2):
      s2 += posList[j]
      
    #calculate the amount of balls within 3 standard deviation of the mean
    if j < (m + sd*3) and j > (m - sd*3):
      s3 += posList[j]
      
      
  #convert them into percentages 
  p1 = (s1/i)*100
  p2 = (s2/i)*100
  p3 = (s3/i)*100

#Using the 68-95-99.7 rule of the normal curve to compare the result to a true normal curve

  print("Actual: {0:.2f}%        ".format(p1),"{0:.2f}%          ".format(p2),"{0:.2f}%   ".format(p3))