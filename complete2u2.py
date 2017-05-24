import json
import csv
import datetime

json_list = []

c= 0
j= 30000000
i = 30000000

headers = True

with open('complete.json','r') as jsonfile:
	print('Reading Json')
	for line in jsonfile:
		if j != 0:
			j-=1
			continue
		if i == 0:
			break
		i-=1
		json_list.append(json.loads(line))
		c+=1
		
		if c%10000000 == 0:
			print(c)

print('Writing to csv!!')

with open("completeu2.csv", "w",newline = '') as file:
	csv_file = csv.writer(file)
	csv_file.writerow(['reviewerID','asin','reviewerName','helpful','reviewText','summary','overall','reviewTime','reviewDate','mon_year','month','year'])
	for item in json_list:
		# if headers:
		# 	csv_file.writerow(['reviewerID','asin','reviewerName','reviewText','overall','reviewTime'])
		# 	headers = False
		try:
			helpf = item['helpful']
		except:
			helpf = ''
		try:
			summ = item['summary']
		except:
			summ = ''
		try:
			name = item['reviewerName']
		except:
			name = ''
			
		try:
			item['unixReviewTime']
		except:
			pass	
		try:
			date_new = datetime.datetime.fromtimestamp(int(item['unixReviewTime'])).strftime('%Y-%m-%d %H:%M:%S')
			mon_year = datetime.datetime.fromtimestamp(int(item['unixReviewTime'])).strftime('%b %Y')
			year = datetime.datetime.fromtimestamp(int(item['unixReviewTime'])).strftime('%Y')
			mon = datetime.datetime.fromtimestamp(int(item['unixReviewTime'])).strftime('%B')
			date_r = datetime.datetime.fromtimestamp(int(item['unixReviewTime'])).strftime('%m/%d/%Y')
		except:
			date_new = ''
			mon_year = ''
			year = ''
			mon = ''
			date_r = ''
			
		csv_file.writerow([item['reviewerID'],item['asin'],item['reviewerName'],helpf,item['reviewText'],summ,item['overall'],date_new,date_r,mon_year,mon,year])
