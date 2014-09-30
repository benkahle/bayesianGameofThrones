import csv
import numpy as np
import scipy as sp
import matplotlib
import matplotlib.pyplot as plt


data=[]
ddata=[]
with open('parsed_characters.csv', 'rb') as dataset:
	reader=csv.reader(dataset)
	for row in reader:
		data.append(row)
with open('got_dead.csv', 'rb') as dataset:
	reader=csv.reader(dataset)
	for row in reader:
		ddata.append(row)


data.pop(0)
ddata.pop(0)

alive=[0,0,0,0,0]
dead=[0,0,0,0,0]
new_char=[0,0,0,0,0]
tot_dead=0
for i in range(len(data)):
	if data[i][5]=='1':
		alive[0]=alive[0]+1
	if data[i][6]=='1':
		alive[1]=alive[1]+1
	if data[i][7]=='1':
		alive[2]=alive[2]+1
	if data[i][8]=='1':
		alive[3]=alive[3]+1
	if data[i][9]=='1':
		alive[4]=alive[4]+1
	# if data[i][4]!='':
	# 	tot_dead+=1

for i in range(len(data)):
	if data[i][5]=='1':
		new_char[0]=new_char[0]+1
	elif data[i][6]=='1':
		new_char[1]=new_char[1]+1
	elif data[i][7]=='1':
		new_char[2]=new_char[2]+1
	elif data[i][8]=='1':
		new_char[3]=new_char[3]+1
	elif data[i][9]=='1':
		new_char[4]=new_char[4]+1


for i in range(len(ddata)):
	if ddata[i][5]=='1':
		dead[0]=dead[0]+1
	if ddata[i][5]=='2':
		dead[1]=dead[1]+1
	if ddata[i][5]=='3':
		dead[2]=dead[2]+1
	if ddata[i][5]=='4':
		dead[3]=dead[3]+1
	if ddata[i][5]=='5':
		dead[4]=dead[4]+1

ratio=[0,0,0,0,0]
tot_char=0
book_lengths=[864,1040,1216,1104,1152]
deaths_p_page=[0,0,0,0,0]

for i in range(5):
	tot_dead=dead[i]+tot_dead
	tot_char=new_char[i]+tot_char

	ratio[i]=float(dead[i])/float(alive[i])
	deaths_p_page[i]=1./(float(dead[i])/float(book_lengths[i]))


n=[0,1,2,3,4]
m,b=np.polyfit(n,new_char,1)

fit=[0,0,0,0,0,0,0]
for i in range(7):
	fit[i]=(float(i)*m)+b
print fit
# print ratio
# print dead
# print tot_dead
# print alive
# print new_char
# print tot_char




N = 5
ind = np.arange(N)    # the x locations for the groups
width = 0.35       # the width of the bars: can also be len(x) sequence


f1=plt.figure()
p1 = plt.bar(ind, alive,   width, color='DarkTurquoise')
p2 = plt.bar(ind, dead, width, color='Tomato')
plt.ylabel('Characters')
plt.title('Book')
plt.xticks(ind+width/2., ('GoT', 'CoK', 'SoS', 'FfC', 'DwD') )
plt.legend( (p1[0], p2[0]), ('Total', 'Dead') )


f2=plt.figure()
p3=plt.plot(new_char,'o',markersize=10,markerfacecolor='SpringGreen', markeredgecolor='White', color='SpringGreen')
p3b=plt.plot(range(7),fit, color='greenyellow')
p3c=plt.plot([5,6],[fit[5],fit[6]],'o',markersize=10,markerfacecolor='White', markeredgecolor='Chartreuse')
ind2 = np.arange(7)
plt.xticks((ind2+width/2.)-.18, ('GoT', 'CoK', 'SoS', 'FfC', 'DwD', 'WoW', 'SoS') )
plt.xlim(-1,7)
plt.xlabel('Books')
plt.ylabel('New Characters')

plt.show()

f3=plt.figure()
p4=plt.plot(ratio,'o',markersize=10,markerfacecolor='crimson', markeredgecolor='white', color='crimson')
plt.xticks((ind+width/2.)-.18, ('GoT', 'CoK', 'SoS', 'FfC', 'DwD') )
plt.xlim(-1,5)
plt.xlabel('Books')
plt.ylabel('Probability of Death')


f4=plt.figure()
p5=plt.plot(deaths_p_page,'o',markersize=10,markerfacecolor='DarkSlateBlue', markeredgecolor='white')
plt.xticks((ind+width/2.)-.18, ('GoT', 'CoK', 'SoS', 'FfC', 'DwD'))
plt.xlim(-1,5)
plt.xlabel('Books')
plt.ylabel('Pages Between Deaths')

# plt.show()


