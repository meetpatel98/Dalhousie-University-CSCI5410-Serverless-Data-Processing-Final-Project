import csv
import random

#Single -1, Couple-2, Family-3, Family-4
header = ['days', 'package']

data = []
for i in range(1000):
	days = random.randint(1,15)
	if days == 1:
		p = 1
	elif days >= 2 and days < 7:
		p = 2
	elif days >= 7 and days < 12:
		p = 3
	else:
		p = 4
	data.append({'days': days, 'package': p})



with open('dataset.csv', 'w', newline='') as csvfile:
	writer = csv.DictWriter(csvfile, fieldnames = header) 
	
	writer.writeheader()
	writer.writerows(data)
	
