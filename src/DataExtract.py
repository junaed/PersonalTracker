'''
Created on May 14, 2014

@author: junaed
'''
import collections
from DataAnalysis import WifiPlace, DayUnit

         
        
def calculateMatch(a,b):
    matchCount = 0
    #print("len(a):"+str(len(a)))
    #print("len(b):"+str(len(b)))
    for a_a in a:
        for b_b in b:
            if a_a == b_b:
                matchCount += 1
    
    return matchCount/len(a)
   
def merge(a,b):
    c = []
    for c_c in a:
        c.append(c_c)
    for b_b in b:
        found = False
        for a_a in a:
            if b_b == a_a:
                found = True
            else:
                pass
        
        if found == False:      
            c.append(b_b)
            
    return c   

def appendZeros(a):
    number = str(a)
    if a<10:
        number = "00"+number
    elif a<100:
        number = "0"+number
    return number

directory="D://Ubicomp Project//Personal Tracker//Ubicomp Data//"
#directory = ""
filename="Nexus 4.csv"
try:
    inputfile = open(directory+filename, "r")
except IOError as e:
    print("I/O error({0}): {1}".format(e.errno, e.strerror))
    
th_match = 0.1
timeDelim = "-------->"   
placeCounter = 1 

wificount=0
wifiPlaces = dict()
timeline = dict()

outputfile = open(directory+"timeline_wifi_"+filename+"_.txt", "w")
outputfile2 = open(directory+"frequency_"+filename+"_.txt", "w")
outputfile3 = open(directory+"dayline_"+filename+"_.txt", "w")

continuity = 1
prevPlace = ""

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



for line in inputfile:
    if "wifi" in line:
        
        a = line.split(';')
        
        ctime = a[2]
        if ctime != "(invalid date)":
            if "scancomplete" in a[3]:
                #indicates a new wifi AP scan
                wificount= int(a[4])
                newWifiPlace = WifiPlace("",0,0)
                newWifiPlace.aplist = []
                # print("newWifiPlace:"+str(len(newWifiPlace.aplist)))                
                pass
            elif "scan" in a[3]:
                if wificount > 0:
                    b = a[3].split('|')
                    
                    if "ssid" in b[3]:
                        newWifiPlace.aplist.append(b[2])
                        pass
                    elif "level" in b[3]:
                        pass
                    elif "frequency" in b[3]:
                        wificount-=1
                        pass
                    elif "capabilities" in b[3]:
                        pass
                    else:
                        print("might be error")
                        pass
                else:
                    #checking list matches
                    curPlace = "" 
                    if len(wifiPlaces) == 0:
                        
                        newWifiPlace.place = "Place:"+appendZeros(placeCounter)
                        curPlace = newWifiPlace.place
                        placeCounter += 1
                        wifiPlaces[newWifiPlace.place] = newWifiPlace
                    else:
                        noMatch = True
                        for key in wifiPlaces.keys():
                            w = wifiPlaces.get(key)
                            match = calculateMatch(w.aplist, newWifiPlace.aplist)
                        #    print(match)
                        #    if match == 1.0:
                            if match > 0:
                                curPlace = w.place
                                w.aplist = merge(w.aplist, newWifiPlace.aplist)
                       #         if len(w.aplist) >= len(newWifiPlace.aplist):
                       #             pass
                       #         else:
                       #             w.aplist = newWifiPlace.aplist
                                noMatch = False
                                break
                        #   elif match > 0:
                        #        curPlace = w.place
                        #        noMatch = False
                        #        break
                             
                            else:
                                pass
                        
                        if noMatch == True:
                            newWifiPlace.place = "Place:"+appendZeros(placeCounter)
                            curPlace = newWifiPlace.place
                            placeCounter += 1
                            wifiPlaces[newWifiPlace.place] = newWifiPlace
                    
                    
                    #adding to the timeline
                    #timeline[ctime[:16]] = curPlace
                    #print("Time:"+ctime[:16]+"----->"+curPlace)
                    outputfile.write(ctime[:16]+"----->"+curPlace+"\n")
                    wifiPlaces[curPlace].count += 1
                    if curPlace == prevPlace:
                        continuity += 1
                    else:
                        continuity = 1
                        prevPlace = curPlace
                        
                    if wifiPlaces[curPlace].max_duration < continuity:
                            wifiPlaces[curPlace].max_duration = continuity
                            
                    #adding to the dayline
                    daytime = ctime[11:15]
                    curDayUnit = dayline[daytime]
                    if curPlace in curDayUnit.places:
                        curDayUnit.places[curPlace] += 1
                    else:
                        curDayUnit.places[curPlace] = 1
                        
                    
                    
                     
inputfile.close()


#outputfile2 = open(directory+"keyvalue_"+filename+"_.txt", "w")

            
#timeline = collections.OrderedDict(sorted(timeline.items()))
'''
for k,v in timeline.items():
    outputfile.write("Time:"+k+"----->")
    outputfile.write(v+"\n")
'''    
wifiPlaces = collections.OrderedDict(sorted(wifiPlaces.items()))
for key in wifiPlaces.keys():
    v = wifiPlaces.get(key)
    outputfile2.write(v.place+" ----> "+str(v.count)+"|"+ str(v.max_duration)+"\n")

dayline = collections.OrderedDict(sorted(dayline.items()))
for key in dayline.keys():
    du = dayline.get(key)
    outputfile3.write(du.hour_minute+"----->")
    max_place = ""
    max_count = 0
    for k,v in du.places.items():
        if v>max_count:
            max_count = v
            max_place = k
    outputfile3.write(max_place+":"+str(max_count)+"\n")        

outputfile.close()
outputfile2.close()
outputfile3.close()



    
  
        
        

