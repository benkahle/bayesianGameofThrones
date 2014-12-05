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


houselist=['Wildling','None','Night\'s Watch','Lannister','House Lannister','Stark','House Stark','Tully','House Tully', 'Arryn','House Arryn',
			'Tyrell', 'House Tyrell', 'Targaryen','House Targaryen','Martell','House Martell','Baratheon','House Baratheon','Greyjoy','House Greyjoy']

# houselist_short=['Stark','Baratheon','None','Lannister','Tully','Arryn','Targaryen','Greyjoy','Wildling','Night\'s Watch','Tyrell','Martell']
houselist_short1=['Arryn','Stark','Lannister','None']
houselist_short2=['Tyrell','Baratheon','Tully','Night\'s Watch']
houselist_short3=['Martell','Targaryen','Wildling','Greyjoy']
houselist_short=['Arryn','Stark','Lannister','None','Tyrell','Baratheon','Tully','Night\'s Watch','Martell','Targaryen','Wildling','Greyjoy']
def Init_List_Struct():
	list_str=[['dead', ['nobles', ['men'], ['women']], ['smallfolk', ['men'], ['women']]], ['alive', ['nobles', ['men'], ['women']], ['smallfolk', ['men'], ['women']]]]
	return list_str
colordict={'Stark':['SlateGrey','DimGrey','Silver'],'Baratheon':['DarkOrange','Red','Orange'],'None':['MediumTurquoise','Teal','DarkSeaGreen'],
			'Lannister':['Maroon','DarkGoldenRod','Gold'],'Tully':['FireBrick','RoyalBlue','LightSteelBlue'],'Arryn':['LightSkyBlue','LightSlateGrey','MidnightBlue'],
			'Targaryen':['DarkRed','Black','Brown'],'Greyjoy':['DarkSlateGrey','GoldenRod','Khaki'],'Wildling':['Indigo','BlueViolet','Plum'],
			'Night\'s Watch':['Black','LightGrey','Grey'],'Tyrell':['DarkGreen','Yellow','YellowGreen'],'Martell':['PaleGoldenRod','SandyBrown','Tomato']}
No=Init_List_Struct()
Lannister=Init_List_Struct()
Stark=Init_List_Struct()
Tully=Init_List_Struct()
Arryn=Init_List_Struct()
Tyrell=Init_List_Struct() #WTF
Targaryen=Init_List_Struct()
Martell=Init_List_Struct()#WTF2.5559687549462544
Baratheon=Init_List_Struct()
Greyjoy=Init_List_Struct()
Wildling=Init_List_Struct()
NW=Init_List_Struct()

hd={'Wildling':Wildling,'None': No,'Night\'s Watch':NW,'Lannister':Lannister,'House Lannister':Lannister,'Stark':Stark,'House Stark':Stark,
			'Tully':Tully,'House Tully':Tully, 'Arryn':Arryn,'House Arryn':Arryn,'Tyrell':Tyrell, 'House Tyrell':Tyrell, 'Targaryen':Targaryen,
			'House Targaryen':Targaryen,'Martell':Martell,'House Martell':Martell,'Baratheon':Baratheon,'House Baratheon':Baratheon,'Greyjoy':Greyjoy,'House Greyjoy':Greyjoy}

data=[]
with open('char_final.csv', 'r') as dataset:
	reader=csv.reader(dataset)
	for row in reader:
		data.append(row)
data.pop(0)
data.pop(0)
data.pop(0)
data.pop(0)

def house_list(House_Name,info):
	if info [1]==House_Name:
		if info[3]!='': #if they are dead
			if info[8]=='1':#if they are noble
				if info[7]=='1': #if they are male
					hd[House_Name][0][1][1].append(info)
				elif info[7]=='0': #if they are female
					hd[House_Name][0][1][2].append(info)
				else:
					print 'a',info
			elif info[8]=='0': #if they are smallfolk
				if info[7]=='1': #if they are male
					hd[House_Name][0][2][1].append(info)
				elif info[7]=='0': #if they are female
					hd[House_Name][0][2][2].append(info)
				else:
					print 'b',info
			else:
				print 'bb',info
				print info[8]
		elif info[3]=='': #if they are alive
			if info[8]=='1':#if they are noble
				if info[7]=='1': #if they are male
					hd[House_Name][1][1][1].append(info)
				elif info[7]=='0': #if they are female
					hd[House_Name][1][1][2].append(info)
				else:
					print 'c',info
			elif info[8]=='0': #if they are smallfolk
				if info[7]=='1': #if they are male
					hd[House_Name][1][2][1].append(info)
				elif info[7]=='0': #if they are female
					hd[House_Name][1][2][2].append(info)
				else:
					print 'd',info
			else:
				print 'e',info
for info in data:
	for key in houselist:
		house_list(key,info)


def ages(alive,dead):
	got=72
	cok=69
	sos=81
	ffc=45
	dwd=72
	bd={'got':got,'cok':cok,'sos':sos,'ffc':ffc,'dwd':dwd}
	bnd={'got':0,'cok':1,'sos':2,'ffc':3,'dwd':4}
	introductions=[]
	lifetimes=[]

	for pers in dead:
		if pers[9]=='1':
			start='got'
		elif pers[10]=='1':
			start='cok'
		elif pers[11]=='1':
			start='sos'
		elif pers[12]=='1':
			start='ffc'
		elif pers[13]=='1':
			start='dwd'

		if pers[13]=='1':
			end='dwd'
		elif pers[12]=='1':
			end='ffc'
		elif pers[11]=='1':
			end='sos'
		elif pers[10]=='1':
			end='cok'
		elif pers[9]=='1':
			end='got'

		if pers[5]=='':
			birth=bnd[start]
		else:
			birth=(float(pers[5])/bd[start])+bnd[start]
		if pers[4]=='':
			death=bnd[end]+1
		else:
			death=((float(pers[4])+1)/bd[end])+bnd[end]
		life=death-birth

		lifetimes.append(life)


	for pers in alive:
		if pers[9]=='1':
			start='got'
		elif pers[10]=='1':
			start='cok'
		elif pers[11]=='1':
			start='sos'
		elif pers[12]=='1':
			start='ffc'
		elif pers[13]=='1':
			start='dwd'

		if pers[5]=='':
			birth=bnd[start]
		else:
			birth=(float(pers[5])/bd[start])+bnd[start]
		introductions.append(5-birth)
	return introductions,lifetimes

def SurvivalHaz(introductions,lifetimes):
	haz=survival.EstimateHazardFunction(lifetimes, introductions)
	sf=haz.MakeSurvival()

	# thinkplot.plot(sf,color='Grey')
	# plt.xlabel("Age (books)")
	# plt.ylabel("Probability of Surviving")
	# plt.title('Survial Function')
	# thinkplot.show()
	# thinkplot.plot(haz,color='Grey')
	# plt.title('Hazard Function')
	# plt.xlabel("Age (books)")
	# plt.ylabel("Percent of Lives That End")
	# thinkplot.show()
	return sf,haz

class GOT(thinkbayes2.Suite, thinkbayes2.Joint):

	def Likelihood(self, data, hypo):
		age, alive = data
		k, lam = hypo
		if alive:
			prob = 1-exponweib.cdf(age, k, lam)
		else:
			prob = exponweib.pdf(age, k, lam)
		return prob

def Update(k, lam, age, alive):
	joint = thinkbayes2.MakeJoint(k, lam)
	suite = GOT(joint)
	suite.Update((age, alive))
	k, lam = suite.Marginal(0, label=k.label), suite.Marginal(1, label=lam.label)
	return k, lam

def makePMF(k,lam):
	k.label = 'K'
	lam.label = 'Lam'


	print("Updating deaths")
	numDead = len(dead)
	ticks = math.ceil(numDead/100)
	i = 0
	for age in lifetimes:
		# if not i%ticks:
		# 	print('.', end='', flush=True)
		i += 1	
		# age = float(pers[-1])
		k, lam = Update(k, lam, age, False)
	print('Updating alives')
	numAlive = len(alive)
	ticks = math.ceil(numAlive/100)
	i = 0
	for age in introductions:
		# if not i%ticks:
		# 	print('.', end='', flush=True)
		i += 1
		k, lam = Update(k, lam, age, True)
	return k,lam

def WriteFile(k,lam,House):

	intervalk = k.Percentile(5), k.Percentile(95)
	intervallam = lam.Percentile(5), lam.Percentile(95)

	good = raw_input('Good? y/n')

	if good=='y':
		file = open("klam.txt", "a")
		Words=[House,'\n','K\n',str(k),'\n','\n','lam\n',str(lam),'\n','\n','K-90per cred\n',str(intervalk),'\n','\n','Lam-90per cred\n',str(intervallam),'\n','\n',]
		file.writelines(Words)
		file.close()

def cred_params(house):
	file = open('house_all_alivef.txt', 'r')
	i=-1
	cred_param=[['Stark'],['Baratheon'],['None'],['Lannister'],['Tully'],['Arryn'],['Targaryen'],['Greyjoy'],['Wildling'],['Night\'s Watch'],['Tyrell'],['Martell']]
	linelist=[]
	for line in file:
		if line[0] =='(':
			linelist.append(line)
	j=0
	for i in range(len(linelist)):
		if i%2==0:
			kl=float(linelist[i][1:19])	
			kh=float(linelist[i][21:38])

			cred_param[j].append(kl)
			cred_param[j].append(kh)
			j+=1
	j=0
	for i in range(len(linelist)):
		if i%2!=0:
			ll=float(linelist[i][1:19])		
			lh=float(linelist[i][22:38])
			cred_param[j].append(ll)
			cred_param[j].append(lh)
			j+=1
	for i in range(len(cred_param)):
		if cred_param[i][0]==house:
			return cred_param[i][1],cred_param[i][2],cred_param[i][3],cred_param[i][4]

def CredIntPlt(sf,kl,kh,ll,lh,house,mk,ml,Title):
	listcol=colordict[house]
	Dark=listcol[0]
	Mid=listcol[1]
	Light=listcol[2]
	arr=np.linspace(0,7,num=100)
	weibSurv2 = exponweib.cdf(arr, kl, lh)
	weibSurv4 = exponweib.cdf(arr, kh, ll)
	weibSurv1 = exponweib.cdf(arr, mk, ml)
	# p4,=plt.plot(arr, 1-weibSurv2,color=Dark,linewidth=3)
	p1,=plt.plot(arr, 1-weibSurv2,color=Light,linewidth=4)
	# p2,=plt.plot(arr, 1-weibSurv1,color=Mid,linewidth=3,linestyle='--')
	p3,=plt.plot(arr, 1-weibSurv4,color=Light,linewidth=4)
	plt.fill_between(arr,1-weibSurv2,1-weibSurv4, facecolor=Light, alpha=.3)
	# thinkplot.plot(sf,color=Dark)
	plt.xlabel('Age in Books')
	plt.ylabel('Probability of Survival')
	plt.ylim([.0,1]) 
	plt.text(6.3,0.95,'Theon',color='Khaki')
	plt.text(5.3,0.4,'Lord Walder Frey',color='DarkSeaGreen')
	
	# plt.legend([p1,p2,p4],['90 Percent Credible Interval','Best Estimate','Data'])
	plt.title(Title)


def char_lists(house,Gender,Class):
	cur_house=hd[house]
	alive1=cur_house[1][1][1] #Noble Men
	alive2=cur_house[1][1][2] #Noble Women
	alive3=cur_house[1][2][1]  #Small Men
	alive4=cur_house[1][2][2] #Small Women
	alive1.pop(0)
	alive2.pop(0)
	alive3.pop(0)
	alive4.pop(0)

	dead1=cur_house[0][1][1]
	dead2=cur_house[0][1][2]
	dead3=cur_house[0][2][1]
	dead4=cur_house[0][2][2]
	dead1.pop(0)
	dead2.pop(0)
	dead3.pop(0)
	dead4.pop(0)

	if Gender=='M' and Class=='Noble':
		alive=alive1
		dead=dead1
	elif Gender=='M' and Class=='Small':
		alive=alive3
		dead=dead3
	elif Gender=='M' and Class=='All':
		alive=alive1+alive3
		dead=dead1+dead3
	elif Gender=='F' and Class=='Noble':
		alive=alive2
		dead=dead2
	elif Gender=='F' and Class=='Small':
		alive=alive4
		dead=dead4
	elif Gender=='F' and Class=='All':
		alive=alive2+alive4
		dead=dead2+dead4
	elif Gender=='All' and Class=='All':
		dead=dead1+dead2+dead3+dead4
		alive=alive1+alive2+alive3+alive4
	else:
		print ('Check your entries')
	if len(dead)<=5:
		print ('There are less than 5 dead in this category.  Results may not be meaningful')
	return alive,dead


# for house in ['Martell','None']
# 	alive,dead=char_lists(house)
# 	introductions,lifetimes=ages(alive,dead)

# 	sf,haz=SurvivalHaz(introductions,lifetimes)

# 	# kal,kah,lal,lah=cred_params(house)
# # CredIntPlt(sf,kal,kah,lal,lah,house,2.5559687549462544,0.26786495258406434) #NW all
# 	if house=='Martell':
# 		kal,kah,lal,lah=3.4324324324324325, 4.0851351351351353,0.20135135135135135, 0.25810810810810814
# 	if house=='None':
# 		kal,kah,lal,lah=2.5878378378378377, 3.0337837837837838,0.17770270270270272, 0.21554054054054056
# 	CredIntPlt(sf,kal,kah,lal,lah,house,2.3113471123606892,0.44672574344173971) #NW nobles
# plt.show()

def Specific_Character(House,Gender,Class,ksweep,lamsweep,Title=''):
	alive,dead=char_lists(House,Gender,Class)
	print 'alive', len (alive)
	print alive
	print 'dead', len (dead)
	introductions,lifetimes=ages(alive,dead)
	sf,haz=SurvivalHaz(introductions,lifetimes)
	lam= thinkbayes2.MakeUniformPmf(lamsweep[0],lamsweep[1],lamsweep[2])
	k = thinkbayes2.MakeUniformPmf(ksweep[0],ksweep[1],ksweep[2])
	k.label = 'K'
	lam.label = 'Lam'
	print('Updating alives')
	numAlive = len(alive)
	i = 0
	for pers in introductions:
		i += 1
		age = pers
		k, lam = Update(k, lam, age, True)

	print("Updating deaths")
	numDead = len(dead)
	i = 0
	for pers in lifetimes:
		i += 1	
		age = pers
		k, lam = Update(k, lam, age, False)
	# thinkplot.PrePlot(2)
	# thinkplot.Pdfs([k, lam])
	# plt.xlabel('Value')
	# plt.ylabel('Probability')
	# plt.title('Posterior Distributions')
	# print ('If these distributions look chopped off, adjust kweep and lamsweep')
	# thinkplot.Show()
	mk = k.Mean()
	ml = lam.Mean()
	kl,kh = k.Percentile(5), k.Percentile(95)
	ll,lh = lam.Percentile(5), lam.Percentile(95)
	CredIntPlt(sf,kl,kh,ll,lh,House,mk,ml,Title)
	# plt.show()


# arya and sansa
# Cersi
# Val
# Quaithe
# ksweep=[1.5,11,75]
# lsweep=[.0001,1,75]
# Specific_Character('Stark','F','All',ksweep,lsweep)
# ksweep=[.5,7,75]
# lsweep=[.0001,1,75]
# Specific_Character('Lannister','F','All',ksweep,lsweep,)
# ksweep=[.5,4.5,75]
# lsweep=[.0001,1,75]
# Specific_Character('Wildling','F','All',ksweep,lsweep)
# ksweep=[2,6,75]
# lsweep=[.0001,.5,75]
# Specific_Character('None','F','All',ksweep,lsweep,'Some Minor Characters') 
# plt.show()


# dario
# mance
# theon
# Tyrion+ Jamie
# Frey

# ksweep=[1,8,75]
# lsweep=[.0001,.7,75]
# Specific_Character('Targaryen','M','Small',ksweep,lsweep)
# ksweep=[2.5,7.5,75]
# lsweep=[.0001,1,75]
# Specific_Character('Lannister','M','Noble',ksweep,lsweep,)
# ksweep=[.5,3.5,75]
# lsweep=[.0001,1,75]
# Specific_Character('Wildling','M','All',ksweep,lsweep,'Some Characters I Would Like to Live')
ksweep=[1.5,5,75]
lsweep=[.0001,.5,75]
Specific_Character('None','M','Noble',ksweep,lsweep) 
ksweep=[2,9.5,75]
lsweep=[.0001,.5,75]
Specific_Character('Greyjoy','M','Noble',ksweep,lsweep,'Some Characters I Would Like to Die')
plt.show()

# i = 0
# for pers in introductions:
# 	i += 1
# 	age = pers
# 	k, lam = Update(k, lam, age, True)

# print("Updating deaths")
# numDead = len(dead)
# i = 0
# for pers in lifetimes:
# 	i += 1	
# 	age = pers
# 	k, lam = Update(k, lam, age, False)

# thinkplot.PrePlot(2)
# thinkplot.Pdfs([k, lam])
# plt.xlabel('Value')
# plt.ylabel('Probability')
# plt.title('Posterior Distributions')
# thinkplot.Show()
# bestK = k.Mean()
# bestLam = lam.Mean()
# print("K:", bestK, "Lam:", bestLam)


# # k = thinkbayes2.MakeUniformPmf(.5,2.5,75)
# # lam = thinkbayes2.MakeUniformPmf(.000001,2,75)
# # k,lam=makePMF(k,lam)


# # thinkplot.PrePlot(2)
# # thinkplot.Pdfs([k, lam])
# # thinkplot.Show()
# # bestK = k.Mean()
# # bestLam = lam.Mean()
# # print("K:", bestK, "Lam:", bestLam)
# arr=np.linspace(0,7,num=100)
# weibSurv = exponweib.cdf(arr, bestK, bestLam)

# # # weibDeath = exponweib.pdf(arr, bestK, bestLam)
# # p1,=plt.plot(arr, 1-weibSurv, label="Survival Function")
# intervalk = k.Percentile(5), k.Percentile(95)
# intervallam = lam.Percentile(5), lam.Percentile(95)
# print intervalk
# print intervallam

# # (1.3175675675675675, 3.6216216216216219)
# # (0.24675675675675679, 0.66805405405405416)

# # thinkplot.plot(sf)
# # p2,=plt.plot(arr, weibDeath, label="Probability of Death")
# # thinkplot.plot(haz)
# # plt.xlabel('Age (books)')
# # plt.ylabel('Rate of Survival or Death')
# # plt.legend([p1,p2],['Survival Function','Probability of Death'])
# plt.show()

# House='NW All \n'
# WriteFile(k,lam,House)