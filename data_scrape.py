#!/usr/bin/python3
import sys
import re

# python script to parse data from text file and output a sql file 


out = open("location.sql", "w")

query = "INSERT INTO location (code, location_name) VALUES ("


lines = [line.rstrip('\n') for line in open('/home/accts/jgt37/cs437/location.txt')]

for line in lines:
	code = line[3 : 10].strip()
	loc = line[13 : ].strip()
	newQuery = query + '\'' + code + '\', \'' + loc + '\');\n'
	out.write(newQuery)

out.close()



out = open("industry.sql", "w")

query = "INSERT INTO industry (code, industry_name) VALUES ("

lines = [line.rstrip('\n') for line in open('/home/accts/jgt37/cs437/industry.txt')]

for line in lines:
	#tokens = list(re.finditer("  *[0-9]*  *", line))
	code = line[0 : 6].strip()
	ind = line.rstrip("\t 0123456789")[7 : len(line.rstrip("\t 0123456789")) - 4].strip()
	newQuery = query + '\'' + code + '\', \'' + ind + '\');\n'
	out.write(newQuery)

out.close()


out = open("occupation.sql", "w")

query = "INSERT INTO occupation (code, occupation_name) VALUES ("

lines = [line.rstrip('\n') for line in open('/home/accts/jgt37/cs437/occupation.txt')]

for line in lines:
	#tokens = list(re.finditer("  *[0-9]*  *", line))
	code = line[0 : 6].strip()
	occ = line.rstrip("\t 0123456789")[7 : len(line.rstrip("\t 0123456789")) - 4].strip()
	newQuery = query + '\'' + code + '\', \'' + occ + '\');\n'
	out.write(newQuery)

out.close()


out = open("income_data_result.sql", "w")

query = "INSERT INTO income_data_result (code, income_data_result) VALUES ("


lines = [line.rstrip('\n') for line in open('/home/accts/jgt37/cs437/return_value.txt')]

for line in lines:
	#tokens = list(re.finditer("  *[0-9]*  *", line))
	code = line[0 : 2].strip()
	loc = line[3 : ].strip()
	newQuery = query + '\'' + code + '\', \'' + loc + '\');\n'
	out.write(newQuery)

out.close()