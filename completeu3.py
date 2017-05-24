#Loading packages
import json
import ast
import pandas as pd

#Initializing the count
c = 0 
i =30000000
j = 60000000

#Creating an empty list to store pandas dataframes of product reviews
df_list =[]
# metadata = []

#Reading from json file and coverting them into pandas dataframes
with open('complete.json','r') as jsonfile:
	print('Reading complete JSON file..')
	for line in jsonfile:
		if j != 0:
			j-=1
			continue
		if i ==0:
			break
			
		# if c ==0:
		# 	break
		# print(json.loads(json.dumps(ast.literal_eval(line))))
		# df.append( pd.read_json(json.dumps(ast.literal_eval(line))))
		df_list.append(pd.read_json(line,lines = True))
		# print(df[i])
		i-=1
		c+=1
		if c%1000000 == 0:
			print('records read: ',c)

print(c,' Json Lines read')
print('List of data frames are being created')
#combining all the individual datasets
df_complete = pd.concat(df_list) 

print('Merged the data frames')
print('Performing manupulations')
# #Droping unwanted columns
# df_complete.drop('reviewTime',axis = 1,inplace = True)

#Changing to user readable time format
df_complete['stdReviewTime'] = pd.to_datetime(df_complete['unixReviewTime'],unit = 's')

#Getting date in YearMonthWeek format
df_complete['Year'] = df_complete['stdReviewTime'].apply(lambda x:x.strftime('%m-%Y'))
df_complete['Week'] = df_complete['stdReviewTime'].dt.week

# print(df_complete)
# print(df_complete.dtypes)

#witing to csv
print('Writing to CSV file')
df_complete.to_csv('product_reviews3.csv',sep = '\t', encoding = 'utf-8', index= False)
