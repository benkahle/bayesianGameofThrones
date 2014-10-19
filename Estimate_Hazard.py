import csv
import numpy as np
import scipy as sp
from scipy.stats import exponweib
import matplotlib
import matplotlib.pyplot as plt
import pandas
import thinkstats2
import thinkbayes2
import survival
import thinkplot
import random
import math


data=[]
dead=[]
alive=[]
with open('parsed_characters.csv', 'r') as dataset:
	reader=csv.reader(dataset)
	for row in reader:
		data.append(row)
data.pop(0)
data.pop(0)
data.pop(0)
# print (len(data))
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

class GOT(thinkbayes2.Suite, thinkbayes2.Joint):

	def Likelihood(self, data, hypo):
		age, alive = data
		k, lam = hypo
		if alive:
			prob = exponweib.cdf(age, k, lam)
		else:
			prob = exponweib.pdf(age, k, lam)
		# print(prob)
		return prob

def Update(k, lam, age, alive):
	joint = thinkbayes2.MakeJoint(k, lam)
	suite = GOT(joint)
	suite.Update((age, alive))
	k, lam = suite.Marginal(0, label=k.label), suite.Marginal(1, label=lam.label)
	return k, lam

k = thinkbayes2.MakeUniformPmf(0.1,10,20)
lam = thinkbayes2.MakeUniformPmf(0.1,2,20)

k.label = 'K'
lam.label = 'Lam'

print('Updating alives')
numAlive = len(alive)
ticks = math.ceil(numAlive/100)
i = 0
for pers in alive:
	if not i%ticks:
		print('.', end='', flush=True)
	i += 1
	age = float(pers[-1])
	k, lam = Update(k, lam, age, True)

print("Updating deaths")
numDead = len(dead)
ticks = math.ceil(numDead/100)
i = 0
for pers in dead:
	if not i%ticks:
		print('.', end='', flush=True)
	i += 1	
	age = float(pers[-1])
	k, lam = Update(k, lam, age, False)

# k, lam = Update(k, lam, 3, True)

thinkplot.Pmfs([k, lam])
thinkplot.Show()


import sweep_out

probpram=sweep_out.loadlist2()
ivec=[]
jvec=[]
survveci=[0] * 100
deadveci=[0] * 100
survvecj=[0] * 100
deadvecj=[0] * 100
# for entry in probpram:
# 	ivec.append(entry[0])
# 	jvec.append(entry[1])
# 	survvec.append(entry[2])
# 	deadvec.append(entry[3])
for entry in probpram:
	option1=np.linspace(.1,5,100)
	option2=np.linspace(.1,20,100)
	for i in range(100):
		if float(entry[0])==option1[i]:
			survveci[i]=survveci[i]+entry[2]
			deadveci[i]=deadveci[i]+entry[3]
		if float(entry[1])==option2[i]:
			survvecj[i]=survvecj[i]+entry[2]
			deadvecj[i]=deadvecj[i]+entry[3]
plt.plot(option1,survveci)
plt.plot(option1,deadveci)
plt.plot(option2,survvecj)
plt.plot(option2,deadvecj)
# ivec=np.linspace(.1,10,100)
# jvec=np.linspace(.1,10,100)
# plt.plot(ivec,survvec,'x')
# plt.plot(ivec,deadvec,'o')
# plt.plot(jvec,survvec,'*')
# plt.plot(jvec,deadvec,'o')
plt.show()
# paramprob=[]
# survprob=[]
# deadprob=[]
# for i in np.linspace(.1,5,100):
# 	print i
# 	for j in np.linspace(.1,20,100):
# 		survprob=[]
# 		deadprob=[]
# 		for pers in dead:
# 			age=float(pers[-1])
# 			surv=exponweib.cdf(age,i,j)
# 			survprob.append(surv)
# 		for pers in alive:
# 			age=float(pers[-1])
# 			surv=exponweib.pdf(age,i,j)
# 			deadprob.append(surv)
# 		survavg=float(sum(survprob))/len(survprob)		
# 		deadavg=float(sum(deadprob))/len(deadprob)	
# 		paramprob.append([i,j,survavg,deadavg])	
# print paramprob
# i=5
# j=1
# dead=exponweib.pdf(arr,i,j)
# surv=exponweib.cdf(arr,i,j)
# plt.plot(arr,1-surv)
# plt.plot(arr,dead)
# plt.show()

