'''
Created on May 14, 2014

@author: Sakib
'''

class TimePeriod:
    timeZone = ""
    startTime = ""
    endTime = ""
    
    def __init__(self):
        self.timeZone=""



class KeyValue:
    key = ""
    value = ""
    place = ""  # unique string assigned for the location 
    count = 0
    periodList = []   # list of String objects, each item is From@To. FromTime and ToTime is seperated by @

    def __init__(self,key,value,place):
        self.key=key
        self.value=value
        self.place=place
   


class WifiPlace:
    place = "" # unique string assigned for the location 
    count = 0  #frequency
    max_duration = 0 #longest time stayed
    aplist = [] # list of neigboring ap macs
    def __init__(self,place,count,max_duration):
        self.place = place
        self.count = count
        self.max_duration = max_duration
        
 
class Place:
    type = ""  # fixed or moving
    description = ""
    periodList = []  # list of String objects
    
    
class TimeUnit:
    date = ""
    places = [] #list of strings to denote places for every hour of the day; if multiple fixed place can be assinged then moving, if no place is confirmed, then gap
    
    def __init__(self,date):
        self.date = date
        
class DayUnit:
    hour_minute = ""  #hour in 24 hour format followed by ":" and first digit of the minute value
    places = dict()
    
    def __init__(self,hour_minute):
        self.hour_minute=hour_minute
        

# directory="D://Ubicomp Project//Personal Tracker//Ubicomp Data//"
# filename="Nexus 4_4.csv"

# directory="/home/junaed/ubidata/"
# filename="GT-I9100.csv"
# 
# input_wifi = open(directory+"timeline_wifi_"+filename+"_.txt", "r")
# input_cell = open(directory+"timeline_cell_"+filename+"_.txt", "r") 
# 
# match_timeline = dict()
# 
# prevPlace = ""
# curPlace = ""
# 
# cell_count = 0
# wifi_count = 0
# extra_wifi = 0
# extra_cell = 0
# 
# for line in input_wifi:
#     tokens = line.split("----->")
#     ctime = tokens[0][:15]
#     curPlace = tokens[1]
#     if curPlace == prevPlace:
#         match_timeline[ctime] = 0
#     else:
#         match_timeline[ctime] = 1
#         
#     prevPlace = curPlace
#     
# 
# prevPlace = ""
# curPlace = ""
# total_match = 0
# 
# for line in input_cell:
#     tokens = line.split("----->")
#     curPlace = tokens[1]   
#     if curPlace == prevPlace:
#         result = 0
#     else:
#         result = 1
#     
#     prevPlace = curPlace
#     
#     if tokens[0] in match_timeline:
#         val = match_timeline.get(tokens[0])
#         
#         if val == result:
#             total_match += 1
#         else:
#             pass
#         
#         cell_count += 1
#         
#     else:
#         extra_cell += 1
#         pass
# 
# wifi_count = len(match_timeline)
# extra_wifi = wifi_count - cell_count
# 
# 
# print("Total Timeline Statistics")
# print("===========================")
# print("Total Cell Entries: "+str(cell_count))
# print("Total Wifi Entries: "+str(wifi_count))
# print("Total Extra Cell Entries: "+str(extra_cell))
# print("Total Extra Wifi Entries: "+str(extra_wifi))
# print("Total Matched Entries: "+str(total_match))
# print("Match percentage: "+str(total_match/cell_count*100.0))
# 
# input_cell.close()
# input_wifi.close()
# 
# input_wifi = open(directory+"dayline_"+filename+"_.txt", "r")
# input_cell = open(directory+"dayline_cell_"+filename+"_.txt", "r") 
# 
# match_dayline = dict()
# 
# prevPlace = ""
# curPlace = ""
# 
# cell_count = 0
# wifi_count = 0
# 
# for line in input_wifi:
#     tokens = line.split("----->")
#     ctime = tokens[0]
#     curPlace = tokens[1][:9]
#     if curPlace == prevPlace:
#         match_dayline[ctime] = 0
#     else:
#         match_dayline[ctime] = 1
#         
#     prevPlace = curPlace
#     
# 
# prevPlace = ""
# curPlace = ""
# total_match = 0
# 
# for line in input_cell:
#     tokens = line.split("----->")
#     curPlace = tokens[1][:9]   
#     if curPlace == prevPlace:
#         result = 0
#     else:
#         result = 1
#     
#     prevPlace = curPlace
#     
#     if tokens[0] in match_dayline:
#         val = match_dayline.get(tokens[0])
#         
#         if val == result:
#             total_match += 1
#         else:
#             pass
#         
#         cell_count += 1
#         
#     else:
#         pass
# 
# wifi_count = len(match_dayline)
# 
# print()
# print("Total Dayline Statistics")
# print("===========================")
# print("Total Cell Entries: "+str(cell_count))
# print("Total Wifi Entries: "+str(wifi_count))
# print("Total Matched Entries: "+str(total_match))
# print("Match percentage: "+str(total_match/cell_count*100.0))
# 
# input_cell.close()
# input_wifi.close()

