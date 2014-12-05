import csv
import numpy as np
from scipy.stats import exponweib
import matplotlib
import matplotlib.pyplot as plt
import thinkstats2
import thinkbayes2
import survival
import thinkplot

# The allegiances in our data set were not consistant, sometimes we used House Name and sometimes just Name.  This list covers all posibilites 
houselist=['Wildling','None','Night\'s Watch','Lannister','House Lannister','Stark','House Stark','Tully','House Tully', 'Arryn','House Arryn',
			'Tyrell', 'House Tyrell', 'Targaryen','House Targaryen','Martell','House Martell','Baratheon','House Baratheon','Greyjoy','House Greyjoy']

#Used for plotting in house colors
colordict={'Stark':['DimGrey','SlateGrey','Silver'],'Baratheon':['DarkOrange','Red','NavajoWhite'],'None':['Teal','MediumTurquoise','DarkSeaGreen'],
			'Lannister':['DarkRed','DarkGoldenRod','Gold'],'Tully':['FireBrick','RoyalBlue','LightSteelBlue'],'Arryn':['MidnightBlue','LightSkyBlue','LightSlateGrey'],
			'Targaryen':['Black','Maroon','Brown'],'Greyjoy':['DarkSlateGrey','GoldenRod','Khaki'],'Wildling':['Indigo','BlueViolet','Plum'],
			'Night\'s Watch':['Black','Grey','LightGrey'],'Tyrell':['DarkGreen','YellowGreen','Yellow'],'Martell':['Tomato','SandyBrown','PaleGoldenRod',]}


def Init_List_Struct():
"""This nested list is how we store characters by attribute.  This function creates the list with labels."""

	list_str=[['dead', ['nobles', ['men'], ['women']], ['smallfolk', ['men'], ['women']]], ['alive', ['nobles', ['men'], ['women']], ['smallfolk', ['men'], ['women']]]]
	return list_str

def house_list(hd,House_Name,info):
"""This function takes in the house variables, a target house, and the character data.  
If the character is in the target house, they are sorted by gender, class, and dead/alive status"""
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

def PrepData():
"""This function reads the csv file and sorts the data into house lists"""

	No=Init_List_Struct()
	Lannister=Init_List_Struct()
	Stark=Init_List_Struct()
	Tully=Init_List_Struct()
	Arryn=Init_List_Struct()
	Tyrell=Init_List_Struct() 
	Targaryen=Init_List_Struct()
	Martell=Init_List_Struct()
	Baratheon=Init_List_Struct()
	Greyjoy=Init_List_Struct()
	Wildling=Init_List_Struct()
	NW=Init_List_Struct()

	hd={'Wildling':Wildling,'None': No,'Night\'s Watch':NW,'Lannister':Lannister,'House Lannister':Lannister,'Stark':Stark,'House Stark':Stark,
			'Tully':Tully,'House Tully':Tully, 'Arryn':Arryn,'House Arryn':Arryn,'Tyrell':Tyrell, 'House Tyrell':Tyrell, 'Targaryen':Targaryen,
			'House Targaryen':Targaryen,'Martell':Martell,'House Martell':Martell,'Baratheon':Baratheon,'House Baratheon':Baratheon,'Greyjoy':Greyjoy,
			'House Greyjoy':Greyjoy}

	data=[]
	with open('char_final.csv', 'r') as dataset:
		reader=csv.reader(dataset)
		for row in reader:
			data.append(row)
	#The first four rows were headers we don't need anymore
	data.pop(0)
	data.pop(0)
	data.pop(0)
	data.pop(0)

	for info in data: #For each character
		for key in houselist: #For each house they could possibly be in
			house_list(hd,key,info) #Sort them accordingly
	return hd 

def ages(alive,dead):
"""For a set of characters, divided into list of alive and dead, this function returns a list of 
all the ages of the alive characters and the lifespans of the dead characters"""
	#Number of chapters in each of the books
	got=72
	cok=69
	sos=81
	ffc=45
	dwd=72
	bd={'got':got,'cok':cok,'sos':sos,'ffc':ffc,'dwd':dwd}
	bnd={'got':0,'cok':1,'sos':2,'ffc':3,'dwd':4}
	introductions=[]
	lifetimes=[]

	for pers in dead: #Find out when the dead person was introduced
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

		if pers[13]=='1': #... and when the died
			end='dwd'
		elif pers[12]=='1':
			end='ffc'
		elif pers[11]=='1':
			end='sos'
		elif pers[10]=='1':
			end='cok'
		elif pers[9]=='1':
			end='got'

		if pers[5]=='':	#If we could not find an intro
			birth=bnd[start] #Assume begining of book
		else:
			birth=(float(pers[5])/bd[start])+bnd[start]
		if pers[4]=='': #If we could not find a death
			death=bnd[end]+1 #Assume the end
		else:
			death=((float(pers[4])+1)/bd[end])+bnd[end]
		life=death-birth
		lifetimes.append(life)

	for pers in alive: #Same process for when an alive person was introduced
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
		introductions.append(5-birth) #Their age at the end of the 4th book 
	return introductions,lifetimes

def SurvivalHaz(introductions,lifetimes,plot=False):
"""Given lists of ages and lifespans, this function calculates the 
	Hazard and Survial curves.  If plot is set True, it will plot them."""
	haz=survival.EstimateHazardFunction(lifetimes, introductions)
	sf=haz.MakeSurvival()
	if plot:
		thinkplot.plot(sf,color='Grey')
		plt.xlabel("Age (books)")
		plt.ylabel("Probability of Surviving")
		plt.title('Survial Function')
		thinkplot.show()
		thinkplot.plot(haz,color='Grey')
		plt.title('Hazard Function')
		plt.xlabel("Age (books)")
		plt.ylabel("Percent of Lives That End")
		thinkplot.show()
	return sf,haz

class GOT(thinkbayes2.Suite, thinkbayes2.Joint):

	def Likelihood(self, data, hypo):
	"""Determines how well a given k and lam predict the life/death of a character """
		age, alive = data
		k, lam = hypo
		if alive:
			prob = 1-exponweib.cdf(age, k, lam)
		else:
			prob = exponweib.pdf(age, k, lam)
		return prob

def Update(k, lam, age, alive):
"""Preforms the Baysian Update and returns the PMFS of k and lam"""
	joint = thinkbayes2.MakeJoint(k, lam)
	suite = GOT(joint)
	suite.Update((age, alive))
	k, lam = suite.Marginal(0, label=k.label), suite.Marginal(1, label=lam.label)
	return k, lam

def MakeDistr(introductions, lifetimes,k,lam):
"""Iterates through all the characters for a given k and lambda.  It then updates
	the k and lambda distributions """
	k.label = 'K'
	lam.label = 'Lam'
	print("Updating deaths")
	for age in lifetimes:
		k, lam = Update(k, lam, age, False)
	print('Updating alives')
	for age in introductions:
		k, lam = Update(k, lam, age, True)
	return k,lam

def WriteFile(k,lam,House):
"""Stores the distributions and percentiles of k and lambda"""

	intervalk = k.Percentile(5), k.Percentile(95)
	intervallam = lam.Percentile(5), lam.Percentile(95)

	file = open("klam.txt", "a")
	Words=[House,'\n','K\n',str(k),'\n','\n','lam\n',str(lam),'\n','\n','K-90per cred\n',str(intervalk),'\n','\n','Lam-90per cred\n',str(intervallam),'\n','\n',]
	file.writelines(Words)
	file.close()

def cred_params(house):
""" Reads a file written by WriteFile and returns the 90 percent credible k and lambda values for that house"""
	file = open('house_all_alivef.txt', 'r')
	i=-1
	#List to add data to
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
"""Given 90 credible values of k and lambda, the mean values of k and lambda, 
	the survival function, the house color scheme to use, and the plot title, this 
	function plots the 90 percent credible interval, the best line, and the data 
	we have"""

	listcol=colordict[house]
	Dark=listcol[0]
	Mid=listcol[1]
	Light=listcol[2]
	arr=np.linspace(0,7,num=100)
	weibSurv2 = exponweib.cdf(arr, kl, lh) #Lower bound
	weibSurv4 = exponweib.cdf(arr, kh, ll) #Upper bound
	weibSurv1 = exponweib.cdf(arr, mk, ml) #Best line
	p4,=plt.plot(arr, 1-weibSurv2,color=Dark,linewidth=3)
	p1,=plt.plot(arr, 1-weibSurv2,color=Light,linewidth=4)
	p2,=plt.plot(arr, 1-weibSurv1,color=Mid,linewidth=3,linestyle='--')
	p3,=plt.plot(arr, 1-weibSurv4,color=Light,linewidth=4)
	plt.fill_between(arr,1-weibSurv2,1-weibSurv4, facecolor=Light, alpha=.3)
	thinkplot.plot(sf,color=Dark)
	plt.xlabel('Age in Books')
	plt.ylabel('Probability of Survival')
	plt.ylim([0,1]) 
	
	plt.legend([p1,p2,p4],['90 Percent Credible Interval','Best Estimate','Data'])
	plt.title(Title)

def char_lists(hd,house,Gender,Class):
""" Takes the house you want to work within, as well as the gender and class of the 
characters you want to select for, and returns a list of the dead ones and a list of
dead ones. The class is 'Noble' or 'Small' or 'All' , and the gender is 'M', 'F' or 'All'."""
	cur_house=hd[house]
	alive1=cur_house[1][1][1] #Noble Men
	alive2=cur_house[1][1][2] #Noble Women
	alive3=cur_house[1][2][1] #Small Men
	alive4=cur_house[1][2][2] #Small Women
	#We want to get rid of the lables for each group
	alive1.pop(0)
	alive2.pop(0)
	alive3.pop(0)
	alive4.pop(0)

	dead1=cur_house[0][1][1] #Noble Men
	dead2=cur_house[0][1][2] #Noble Women
	dead3=cur_house[0][2][1] #Small Men
	dead4=cur_house[0][2][2] #Small Women
	#We want to get rid of the lables for each group
	dead1.pop(0)
	dead2.pop(0)
	dead3.pop(0)
	dead4.pop(0)

	#Figure out which segements we want
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
		print ('There are 5 or less dead in this category.  Results may not be meaningful')
	return alive,dead

def Specific_Character(House,Gender,Class,ksweep,lamsweep,Title=''):
"""Knits many function together to produce a prediction for a given house, gender and class
The house can be any key in hd, class can be 'Noble' or 'Small' or 'All' , and the gender can 
be 'M' or 'F' or 'All'.  This also needs to make a linspace for k and lambda, so ksweep and 
lsweep are lists of the form [lower limit, upper limit, number of points].  You can also 
choose what to title your graph."""
	hd=PrepData() #Get the data
	alive,dead=char_lists(hd,House,Gender,Class) #Sort by alive/dead for given attributes
	introductions,lifetimes=ages(alive,dead) #Get ages and lifespans
	sf,haz=SurvivalHaz(introductions,lifetimes) #Use kaplan-meyer
	lam= thinkbayes2.MakeUniformPmf(lamsweep[0],lamsweep[1],lamsweep[2]) #Our uniform priors
	k = thinkbayes2.MakeUniformPmf(ksweep[0],ksweep[1],ksweep[2])
	k, lam=MakeDistr(introductions, lifetimes,k,lam) #Get our posterior

	thinkplot.PrePlot(2)
	thinkplot.Pdfs([k, lam])
	plt.xlabel('Value')
	plt.ylabel('Probability')
	plt.title('Posterior Distributions')
	print ('If these distributions look chopped off, adjust kweep and lsweep')
	thinkplot.Show()

	mk = k.Mean()
	ml = lam.Mean()
	kl,kh = k.Percentile(5), k.Percentile(95)
	ll,lh = lam.Percentile(5), lam.Percentile(95)
	CredIntPlt(sf,kl,kh,ll,lh,House,mk,ml,Title)
	plt.show()


ksweep=[2.5,7,10] #These will end up as uniform priors
lsweep=[.001,1,10]
Specific_Character('Martell','M','Noble',ksweep,lsweep,'Some Characters I Would Like to Die')
