import csv
import numpy as np
import scipy as sp
from scipy.stats import exponweib
import matplotlib
import matplotlib.pyplot as plt
import pandas
import thinkstats2
import survival
import thinkplot
import random


data=[]
dead=[]
alive=[]
with open('parsed_characters.csv', 'rb') as dataset:
	reader=csv.reader(dataset)
	for row in reader:
		data.append(row)
data.pop(0)
data.pop(0)
data.pop(0)
print (len(data))
for info in data:

	if info[2]!='':
		dead.append(info)
	else:
		alive.append(info)

lifetimes=[]
introductions=[]
for pers in dead:
	life=0
	rand=random.randint(1,9)
	rand=rand/10.0
	rand=0
	if (int(pers[8])+int(pers[9])+int(pers[10])+int(pers[11])+int(pers[12]))==1:
		lifetimes.append(1-rand)
		pers.append('lifetime')
		pers.append(1)

	else:
		start=0
		end=0

		if pers[7+1]=='1':
			start=0
		elif pers[7+2]=='1':
			start=1
		elif pers[7+3]=='1':
			start=2
		elif pers[7+4]=='1':
			start=3

		if pers[13-1]=='1':
			end=4
		elif pers[13-2]=='1':
			end=3
		elif pers[13-3]=='1':
			end=2
		elif pers[13-4]=='1':

			end=1
		life=end-start+1
		# print pers
		# print start, end 
		# print life, rand, life-rand
		lifetimes.append(life-rand)
		pers.append('lifetimes')
		pers.append(life)

for pers in alive:
		start=0
		rand=random.randint(1,9)
		rand=rand/10.0
		rand=0
		if pers[7+1]=='1':
			start=0+rand
		elif pers[7+2]=='1':
			start=1+rand
		elif pers[7+3]=='1':
			start=2+rand
		elif pers[7+4]=='1':
			start=3+rand
		elif pers[7+5]=='1':
			start=4+rand

		start=5-start
		introductions.append(start)
		pers.append('age')
		pers.append(start)
alive.pop(0)
# print alive
# print dead
# print introductions
# print min(introductions), max(introductions)
# print lifetimes
# print min(lifetimes), max(lifetimes)
ones=0
twos=0
threes=0
fours=0
fives=0


for num in lifetimes:
	if num==1:
		ones+=1
	if num==2:
		twos+=1
	if num==3:
		threes+=1
	if num==4:
		fours+=1
	if num==5:
		fives+=1


# print 'lifetime in books'
# print 'ones', ones
# print 'twos', twos
# print 'threes', threes
# print 'fours', fours
# print 'fives', fives


ones=0
twos=0
threes=0
fours=0
fives=0


for num in introductions:
	if num==1:
		ones+=1
	if num==2:
		twos+=1
	if num==3:
		threes+=1
	if num==4:
		fours+=1
	if num==5:
		fives+=1

# print ''
# print 'Lifetime (alive)'
# print 'one', ones
# print 'two', twos
# print 'three', threes
# print 'four', fours
# print 'five', fives
# print 'total', ones+twos+threes+fours+fives

# lifetimes=[1,2,3,4,5]
# introductions=[5]

haz=survival.EstimateHazardFunction(lifetimes, introductions)
sf=haz.MakeSurvival()

# thinkplot.plot(sf)
# thinkplot.show()
# thinkplot.plot(haz)
# thinkplot.show()

arr=np.linspace(1,7,num=100)

paramprob=[]
survprob=[]
deadprob=[]
for i in np.linspace(.1,10,100):
	print i
	for j in np.linspace(.1,10,100):
		for pers in dead:
			age=float(pers[-1])
			surv=exponweib.cdf(age,i,j)
			survprob.append(surv)
		for pers in alive:
			age=float(pers[-1])
			surv=exponweib.pdf(age,i,j)
			deadprob.append(surv)
		survavg=float(sum(survprob))/len(survprob)		
		deadavg=float(sum(deadprob))/len(deadprob)	
		paramprob.append([i,j,survavg,deadavg])	
print paramprob
