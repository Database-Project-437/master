from django.shortcuts import render
from django.http import HttpResponse
import mysql.connector
from operator import itemgetter
import requests

mydb = mysql.connector.connect(
	host="den1.mysql2.gear.host",
	user="dbproject2",
	passwd="Nm2y--Po3wi9",
	database="dbproject2"
	
)


def index(request):
	#these will be replaced with queries 
	
	mycursor = mydb.cursor()
	mycursor.execute("SELECT * FROM location")
	locations_list = mycursor.fetchall()

	mycursor.execute("SELECT * FROM industry")
	industry_list = mycursor.fetchall()
	
	mycursor.execute("SELECT * FROM occupation")
	occupation_list = mycursor.fetchall()
	
	mycursor.execute("SELECT * FROM income_data_result")
	statistic_list = mycursor.fetchall()

#	locations_list = [("France",12343),("New York", 32433),("China", 323432)]
#	industry_list =  [("Technology",234),("Finance", 231),("Fuel", 699)]
#	occupation_list = [("Doctor",87),("Programmer", 34),("Teacher", 23)]
#	statistic_list = [("Annual Salary",1),("Average Salary", 2)]
	
		
	context = {"locations_list":locations_list,"occupation_list":occupation_list,"industry_list":industry_list,"statistic_list": statistic_list}
	
			
	return render(request, 'dbcli/main.html', context)
	
	
def handle_0(request):
	
	bad_input = False; 
	
	if('occupation' not in request.GET):
		bad_input = True
	elif('industry' not in request.GET):
		bad_input = True
	elif('occupation' not in request.GET):
		bad_input = True		
	elif('stat' not in request.GET):
		bad_input = True
	else:
		
			
		location = eval(request.GET['location']);
		industry = eval(request.GET['industry']);
		occupation = eval(request.GET['occupation']);
		stat = eval(request.GET['stat']);
		
	#	call function here
		res = value_extractor(location[0],industry[0],occupation[0],stat[0])
		
		if res == -1:
			res = "No Data Available"
			
	
	if(bad_input):
		location = ("Invalid Request","Not all params filled")
		industry = ("Invalid Request","Not all params filled")
		occupation = ("Invalid Request","Not all params filled")
		stat = ("Invalid Request","Not all params filled")
		res = "Bad params"
		
	
	
	context = {"location":location[1], "industry":industry[1],"occupation":occupation[1],"stat":stat[1],"res":res}
	
	return render(request, 'dbcli/q0.html', context) 
	
def handle_1(request):
	
	bad_input = False; 
	location = [("Invalid Request","Invalid Request")]
	
	if('occupation' not in request.GET):
		bad_input = True
	elif('industry' not in request.GET):
		bad_input = True
	elif('location' not in request.GET):
		bad_input = True
	elif('stat' not in request.GET):
		bad_input = True		
	elif('sorting' not in request.GET):
		bad_input = True
	else:

		location = list(map(eval, request.GET.getlist('location')));
		industry = list(map(eval, request.GET.getlist('industry')));
		occupation = list(map(eval, request.GET.getlist('occupation')));	
		stat = eval(request.GET['stat']);
		
		great_to_least = False
		if(request.GET['sorting'] == "GL"):
			great_to_least = True;
			
		res = db_Parser(location, industry, occupation, stat, (not great_to_least))	
		
	
	if(bad_input):
		location = [("Invalid Request","Not all params filled")]
		industry = [("Invalid Request","Not all params filled")]
		occupation = [("Invalid Request","Not all params filled")]
		stat = [("Invalid Request","Not all params filled")]
		res = []
		
	
	context = {"location":location, "industry":industry,"occupation":occupation,"stat":stat, "res":res}
#	
	return render(request, 'dbcli/q1.html', context) 
	
def handle_2(request):
	
	bad_input = False; 
	
	if('occupation' not in request.GET):
		bad_input = True
	elif('industry' not in request.GET):
		bad_input = True
	elif('location' not in request.GET):
		bad_input = True			
	elif('salary' not in request.GET):
		bad_input = True
	else:
	
		location = eval(request.GET['location']);
		industry = eval(request.GET['industry']);
		occupation = eval(request.GET['occupation']);
		salary = int(request.GET['salary'])

		res = annual_Wage(location[0],industry[0],occupation[0])


	
	if(bad_input):
		location = ("Invalid Request","Not all params filled")
		industry = ("Invalid Request","Not all params filled")
		occupation = ("Invalid Request","Not all params filled")
		salary = ("Invalid Request","Not all params filled")
		res = "Bad params"
	
	context = {"location":location[1], "industry":industry[1],"occupation":occupation[1], "salary":salary, "salary_list":[salary],"sample_data":res}
	
	
	
	
	return render(request, 'dbcli/q2.html', context) 
	
def isState(word):
	for i in word:
		if not i.isalpha():
			return False 
			
	return True 
	
def value_extractor(area_Code, industry_Code, occupation_Code, statistic_Code):
	
	url = "https://api.bls.gov/publicAPI/v2/timeseries/data/OEU"
		
	if(area_Code == "0000000"):
		url+="N"
	elif area_Code[:-5] == "00000":
		url+="S"
	else:
		url+="M"
		
	final_url = url + str(area_Code) + str(industry_Code) + str(occupation_Code) + str(statistic_Code)
	data = requests.get(final_url).json()
	
	print(final_url)
	print(data)
	
	if(data['status']=="REQUEST_NOT_PROCESSED"):
		return -1

	if(data['status']=="REQUEST_FAILED"):
		return -1
		
	if(not len(data['Results']['series'][0]['data']).isdigit()):
		return -1

	if(len(data['Results']['series'][0]['data']) != 0):
		print(data['Results']['series'][0]['data'][0]['value'])
		return float(data['Results']['series'][0]['data'][0]['value'])
	
	return -1 
	
#	return data['Results']['series'][0]['data'][0]['value']


def db_Parser(area_code_List, industry_List, occupation_List,  statistic_code_tuple, lowest_to_highest):

	permutated_List = []
	for i in area_code_List:
		for j in industry_List:
			for k in occupation_List:
				permutated_List.append((i, j, k, value_extractor(i[0], j[0], k[0], statistic_code_tuple[0])))
					
	if lowest_to_highest == True:
		return sorted(permutated_List, key=itemgetter(3))
	else:
		return list(reversed(sorted(permutated_List, key=itemgetter(3))))

	
def annual_Wage(location_Code, occupation_Code, industry_Code):
	annual_Wage_List = []
	for i in range(11, 16):
		annual_Wage_List.append(value_extractor(location_Code, occupation_Code, industry_Code, str(i)))
	return annual_Wage_List
