import json
import pandas as pd
import ast

c = 1
# metadata = []
with open('metadata.json','r') as jsonfile:
	print('Reading meta JSON file..')
	for line in jsonfile:
		if c==0:
			break
		df = json.loads(json.dumps(ast.literal_eval(line)))
		df1 =  json.dumps(ast.literal_eval(line))
		print(type(df))
		print(type(df1))
		print(type(line))
		pdf = pd.read_json(df1)
		print(pdf)
		c-=1


		