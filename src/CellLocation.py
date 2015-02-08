#! /usr/bin/python3.4

'''
Created on May 20, 2014

@author: junaed
'''
import copy
import collections
import sys
from DataAnalysis import KeyValue, DayUnit
import gc


def appendZeros(a):
    number = str(a)
    if a<10:
        number = "00"+number
    elif a<100:
        number = "0"+number
    return number

def clockStyle(a,b):
    if a<10:
        return "0"+str(a)+":"+str(b)
    else:
        return str(a)+":"+str(b)
    
    
def incrementDate(date):
    parts = date.split('-')
    year = int(parts[0])
    month = int(parts[1])
    day = int(parts[2])
    
    if day == 31:
        if month == 12:
            year += 1
            month = 1
            day = 1
        else:
            month += 1
            day = 1
    elif day == 30:
        if month in [4,6,9,11]:
            month += 1
            day = 1
        else:
            day += 1
    elif day == 29 and month == 2:
        month += 1
        day = 1
    elif day == 28 and month == 2:
        if (year % 4) == 0:
            day = 29
        else:
            month += 1
            day = 1
    else:
        day += 1 
    
    nextdate = ""
    nextdate += str(year) + "-"
    if month < 10:
        nextdate += "0"
    nextdate += str(month) + "-"
    if day < 10:
        nextdate += "0"
    nextdate += str(day)
    
    return nextdate

# directory="D://Ubicomp Project//Personal Tracker//Ubicomp Data//"
# filename="GT-I9100.csv"

directory="/home/junaed/ubidata/"
filename="GT-I9100.csv"

timeDelim = "---->"
inputfile = open(directory+filename, "r")
content=[]
out=[]
isGSM = True
dayline = dict()

#initialize dayline
hourCounter = 0
while hourCounter < 24:
    minuteCounter = 0
    while minuteCounter < 6:
        hour_min = str(hourCounter)+":"+str(minuteCounter)
        if hourCounter < 10:
            hour_min = "0"+hour_min
        
        du = DayUnit(hour_min)
        du.places = dict()
        dayline[hour_min]=du
        minuteCounter += 1
    
    hourCounter += 1
    
tc = 0;
ti = 0;

for line in inputfile:
    if "celllocation" in line:
        a = line.split(';')
        if len(a) < 5:
            continue
        tc = tc+1
        ctime = a[2]
        if ctime != "(invalid date)" and ctime != None:
            b = a[3].split('|')
            if "phone" in line:
                idx = 2
            else:
                idx = 1

            if "lac" in b[idx]:

                map_d = {"lac":a[4].strip()}
                content.append(copy.copy(out))
                del out[:]
                pass

            elif "basestationid" in b[idx]:
                isGSM = False
                out.append(ctime)
                map_d = {"basestationid":a[4].strip()}
                content.append(copy.copy(out))
#                 out.append(map_d)
                del out[:]
                
            else:
                pass
                #print("Should not be printed")
        else:
            ti += 1
    elif "shutdown" in line:
        a = line.split(';')
        ctime = a[2]
        if ctime != "(invalid date)" and ctime != None:
            out.append(ctime)
            if isGSM:
                map_d = {"lac":"shutdown"}
                out.append(map_d)
            else:
                map_d =  {"basestationid":"shutdown"}
                out.append(map_d)
            content.append(copy.copy(out))
            del out[:]



inputfile.close()

for item in content:
    


# sys.exit()

lastlac=""
startTime=""
endTime=""
placeCounter = 1
allContent = dict()

for item in content:
    if isGSM == True and len(item)>=2:
#         print(item)
        lac = item[1].get("lac")
        if lac == "shutdown":
#             print("shut")
            if lastlac != "" and startTime != "" and endTime != "":
                time = startTime[:16]+timeDelim+endTime[:16]
#                 print(time)
                key = lastlac
                if key in allContent:
                    td = allContent.get(key)
                    td.periodList.append(time)
                    pass
                else:
                    k = "celllocation_gsm"
                    td = KeyValue(k,lastlac,"Place:"+appendZeros(placeCounter))
                    placeCounter += 1
                    td.periodList = [time]
                    allContent[key] = td
                lastlac=""
                startTime=""
                endTime=""
            pass
        else:            
            if lastlac == "":
                startTime = item[0]
                endTime = item[0]
                lastlac = lac
            elif lastlac == lac:
                endTime = item[0]
            elif lastlac != lac:
                #end of a stay
                time = startTime[:16]+timeDelim+endTime[:16]
#                 print(time)
                key = lastlac
                if key in allContent:
                    td = allContent.get(key)
                    td.periodList.append(time)
                    pass
                else:
                    k = "celllocation_gsm"
                    td = KeyValue(k,lastlac,"Place:"+appendZeros(placeCounter))
                    placeCounter += 1
                    td.periodList = [time]
                    allContent[key] = td
                lastlac = lac
                startTime = item[0]
                endTime = item[0]
    elif isGSM == False:
        #cdma
        lac = item[1].get("basestationid")
        if "shutdown" == lac:
            if lastlac != "" and startTime != "" and endTime != "":
                time = startTime[:16]+timeDelim+endTime[:16]
#                 print(time)
                key = lastlac
                if key in allContent:
                    td = allContent.get(key)
                    td.periodList.append(time)
                    pass
                else:
                    k = "celllocation_cdma"
                    td = KeyValue(k,lastlac,"Place:"+appendZeros(placeCounter))
                    placeCounter += 1
                    td.periodList = [time]
                    allContent[key] = td
                lastlac=""
                startTime=""
                endTime=""
            pass
        else:
            
            if lastlac == "":
                startTime = item[0]
                endTime = item[0]
                lastlac = lac
            elif lastlac == lac:
                endTime = item[0]
            elif lastlac != lac:
                #end of a stay
                time = startTime[:16]+timeDelim+endTime[:16]
                key = lastlac
                if key in allContent:
                    td = allContent.get(key)
                    td.periodList.append(time)
                    pass
                else:
                    k = "celllocation_cdma"
                    td = KeyValue(k,lastlac,"Place:"+appendZeros(placeCounter))
                    placeCounter += 1
                    td.periodList = [time]
                    allContent[key] = td
                lastlac = lac
                startTime = item[0]
                endTime = item[0]
            pass
        
#handle the last one
if startTime == endTime:
    if isGSM == True:
        time =  startTime[:16]+timeDelim+endTime[:16]
#         print(time)
        key = lastlac
        if key in allContent:
            td = allContent.get(key)
            td.periodList.append(time)
            pass
        else:
            td = KeyValue("celllocation_gsm",lastlac, "Place:"+appendZeros(placeCounter))
            placeCounter +=1
            td.periodList = [time]
            allContent[key] = td
    else:
        #cdma
        time =  startTime[:16]+timeDelim+endTime[:16]
        key = lastlac
        if key in allContent:
            td = allContent.get(key)
            td.periodList.append(time)
            pass
        else:
            td = KeyValue("celllocation_cdma",lastlac, "Place:"+appendZeros(placeCounter))
            placeCounter+=1
            td.periodList = [time]
            allContent[key] = td
        pass        


# for key in allContent.keys():
#     v = allContent.get(key)
#     print(v),
#     print("--->")
#     for period in v.periodList:
#         print(period),
#     print()
    

# outputfile = open(directory+"keyvalue_cell_"+filename+"_.txt", "w")
# outputfile2 = open(directory+"dayline_cell_"+filename+"_.txt", "w")
# outputfile3 = open(directory+"timeline_cell_"+filename+"_.txt", "w")
# 
# timeline = dict()
# 
# for key in allContent.keys():
#     v = allContent.get(key)
# #    outputfile.write(v.key+"\n")
# #    outputfile.write(v.value+"\n")
#     outputfile.write(v.place+"\n")
#     outputfile.write("\n".join(v.periodList))
#     outputfile.write("\n")
#     
#     curPlace = v.place
#     
# 
#     
#     for period in v.periodList:
#         times = period.split(timeDelim)
#         date1 = times[0][:10]
#         date2 = times[1][:10]
#         startTime = times[0][11:15]
#         endTime = times[1][11:15]
#         startTime_parts = startTime.split(':')
#         endTime_parts = endTime.split(':')
#         hour1 = int(startTime_parts[0])
#         minute1 = int(startTime_parts[1])
#         hour2 = int(endTime_parts[0])
#         minute2 = int(endTime_parts[1])
#         int(endTime_parts[0])
#         
#                 
#         #creating timeline
#         
#         dateTimeList = []
#             
#         
#         #creating dayline
#         daytimeList = []
#         m = minute1
#         while m<6:
#             daytimeList.append(clockStyle(hour1, m))
#             dateTimeList.append(date1+"T"+clockStyle(hour1, m))
#             m += 1
#         
#         
#         if date1 == date2:    
#             h = hour1 + 1
#             while h < hour2:
#                 m = 0
#                 while m < 6:
#                     daytimeList.append(clockStyle(h, m))
#                     dateTimeList.append(date1+"T"+clockStyle(h, m))
#                     m += 1
#                 h += 1
#         else:            
#             h = hour1 + 1
#             while h < 24:
#                 m = 0
#                 while m < 6:
#                     daytimeList.append(clockStyle(h, m))
#                     dateTimeList.append(date1+"T"+clockStyle(h, m))
#                     m += 1
#                 h += 1
#             
#             d = incrementDate(date1)
#             
#             while d!= date2:
#                 h = 0
#                 while h < 24:
#                     m = 0
#                     while m < 6:
#                         daytimeList.append(clockStyle(h, m))   
#                         dateTimeList.append(d+"T"+clockStyle(h, m))
#                         m += 1
#                     h += 1
#                 d = incrementDate(d) 
#             
#             h = 0
#             while h < hour2:
#                 m = 0
#                 while m < 6:
#                     daytimeList.append(clockStyle(h, m))
#                     dateTimeList.append(date2+"T"+clockStyle(h, m))
#                     m += 1
#                 h += 1
#                      
#         m = 0
#         while m <= minute2:
#             daytimeList.append(clockStyle(hour2, m))
#             dateTimeList.append(date2+"T"+clockStyle(hour2, m))
#             m += 1
#             
#         
#         for daytime in daytimeList:
#             curDayUnit = dayline[daytime]
#             if curPlace in curDayUnit.places:
#                 curDayUnit.places[curPlace] += 1
#             else:
#                 curDayUnit.places[curPlace] = 1
#                 
#         for datetime in dateTimeList:
#             timeline[datetime] = curPlace 
# 
# 
# timeline = collections.OrderedDict(sorted(timeline.items()))
# for k,v in timeline.items():
#     outputfile3.write(k+"----->"+v+"\n")
# 
# 
# dayline = collections.OrderedDict(sorted(dayline.items()))
# for key in dayline.keys():
#     du = dayline.get(key)
#     outputfile2.write(du.hour_minute+"----->")
#     max_place = ""
#     max_count = 0
#     for k,v in du.places.items():
#         if v>max_count:
#             max_count = v
#             max_place = k
#     outputfile2.write(max_place+":"+str(max_count)+"\n")
# 
# 
# outputfile.close()
# outputfile2.close()
# outputfile3.close()
# 
# del out[:]
# del dateTimeList[:]
# del daytimeList[:]
# del content[:]
# dayline.clear()
# daytime.clear()
# allContent.clear()
# gc.collect()

