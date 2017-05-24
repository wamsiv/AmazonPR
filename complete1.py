import json
# import csv

# json_list = []

c= 0
# headers = True

with open('complete.json','r') as jsonfile:
	print('Reading Json')
	for line in jsonfile:

		# # if c == 10:
		# # 	break
		# json_list.append(json.loads(line))
		c+=1
		
		# if c%100000 == 0:
			# print(c)

print('Total: ',c)
# print('Writing to csv!!')

# with open("complete.csv", "w",newline = '') as file:
#     csv_file = csv.writer(file)
#     for item in json_list:
#     	if headers:
#     		csv_file.writerow(item.keys())
#     		headers = False
#     	csv_file.writerow(item.values())

