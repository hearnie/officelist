import MySQLdb as mdb
import sys
from operator import itemgetter, attrgetter


class SystemLinks:
    def __init__(self):
	self.conlite = lite.connect('sdd.sqlite')
        
        

    
    def sysID(self, sysname):
        with self.conlite:
            cur = self.conlite.cursor()
            cur.execute("SELECT * FROM mapsolarsystems WHERE solarSystemName = (%s)", (sysname))
            rows = cur.fetchone()
            ID = int(rows["solarSystemID"])
            startsys = (rows["solarSystemName"])
            return(startsys, ID)
            

           
    def sysLinks(self, sysid):
        linkedsystems = []
        with self.conlite:
            cur = self.conlite.cursor()
            cur.execute("SELECT toSolarSystemID , fromSolarSystemID FROM mapsolarsystemjumps WHERE fromSolarSystemID = (%s)", (sysid))
            rows = cur.fetchall()                
            for row in rows:
                linkedsystems.append(row)
                                                                                                      
        return(linkedsystems)

    def gatedist(self,targetparam,maxjumps):
        
    
    
        pending = [] # only contains the sysID
        current = []
        done = [] # includes sysID and number of jumps
        blank = []
        adjacent = []
        jumps = 0
        currentsystem = []
        
        tmp2 = []
        inrange = []
        
        
        # lookup our startsystem
        targetlookup = self.sysID(targetparam)
        targetname =  targetlookup[0]
        targetID =  targetlookup[1]
        
        
        # read office list, put in the format officepairs[[officename , officeID], [....
        tmp1 = []
        officepairs = []
        
        office_list = []
        with open('systems.txt', 'r') as f:
                office_list = f.readlines()
        f.close()

        # lookup system names/IDs and put them in the appropriate format
        for office in office_list:
            tmp1= [self.sysID(office.rstrip())]
            tmp1 = [tmp1[0][0], tmp1[0][1]]
            officepairs.append(tmp1)   
        ## End reading office list
       
        pending.append(targetID)
        while jumps < maxjumps:
            
#            if jumps == (maxjumps - 2): ## condition for extending search if nothing found
#               if len(inrange) == 0:
#                    maxjumps = maxjumps + 1
#                    print "Nothing found, extending search"
            jumps = jumps + 1    
            done.append(current)        #shift everything left
            current = pending        
            pending = blank    
            
            for i in range(len(current)):                    #take each item in current list
        
                adjacent = blank
                adjacent = self.sysLinks(current[i])    #put linked systems in adjacent
                for j in range(len(adjacent)):                #for each item in adjacent
        
                    currentsystem = adjacent[j]['toSolarSystemID']
                    if current.count(currentsystem)    == 0:    #check to see if we looked at it before in this loop
                        if done.count(currentsystem) == 0:    #check to see if we looked at it before ever
                            if pending.count(currentsystem ) == 0:
                                pending.append(currentsystem)    #add it to pending list
                                                            
                                for m in range(len(officepairs)):
                                    if officepairs[m][1] == currentsystem:
                                        if currentsystem == targetID:    #special case if it has an office in startsys
                                            tmp2 = [0 , officepairs[m][0]]
                                            inrange.append(tmp2)
                                        else:                                #the normal operation for this stage
                                            tmp2 = [jumps , officepairs[m][0]]
                                            inrange.append(tmp2)
    
        
        inrange.sort()
        return inrange


class RangeLinks:
    
    def distcalc(self,x0,x1,y0,y1,z0,z1):
        self.dist = float()
        klightyear = float("9460000000000000")
        self.xd = x1 - x0
        self.yd = y1 - y0
        self.zd = z1 - z0
        self.dist = (((self.xd * self.xd) + (self.yd * self.yd) + (self.zd * self.zd)) ** 0.5) / klightyear 
        return self.dist
    
    
    def syscoords(self,sysLookup):
	  
	self.conlite = lite.connect('sdd.sqlite')
        with self.conlite:
            cur = self.conlite.cursor()
            self.cur.execute("SELECT * FROM mapsolarsystems WHERE solarSystemName = (%s)", (sysLookup))
            self.rows = self.cur.fetchone()
            self._x = float(self.rows["x"])
            self._y = float(self.rows["y"])
            self._z = float(self.rows["z"])
            self.sysname = (self.rows["solarSystemName"])
        self.conlite.close()
        return(self.sysname, self._x, self._y, self._z)
    


        




    def lydist(self,sysA,resultcount):
    
        self.beacon = []
        self.beacondist = []
        self.rangelist = []
        self.beacon = []
        with open('systems.txt', 'r') as f:
                self.beacon = f.readlines()
        f.close()
        # lookup system names/IDs and put them in the appropriate format
        for k in range(len(self.beacon)):
            self.beacon[k] = self.beacon[k].rstrip()
 
        ## End reading office list

	# short office list for text file troubleshooting.
        #self.beacon = ['Abath', 'Aedald', 'Aeschee', 'Agoze', 'Aivonen', 'Alachene', 'Aldali', 'Aliette']

            
        self.system = [0,1]
        self._x1 = [0,1]
        self._y1 = [0,1]
        self._z1 = [0,1]
        
        for i in range(len(self.beacon)):
            sysB = self.beacon[i]
            (self.system[0], self._x1[0], self._y1[0], self._z1[0]) = self.syscoords(sysA)
            (self.system[1], self._x1[1], self._y1[1], self._z1[1]) = self.syscoords(sysB)
            self.beacondist.append(self.distcalc(self._x1[0] , self._x1[1] , self._y1[0] , self._y1[1] , self._z1[0] , self._z1[1]))
            self.rangelist.append([self.beacondist[i], self.beacon[i].rstrip('\n')])
        
        
        #sort the list by distance    
        self.rangelist =  sorted(self.rangelist)
        
        # convert the output to 2 decimal places
        for self.i in range(len(self.rangelist)):
           self.rangelist[self.i][0] = "%.2f" % self.rangelist[self.i][0]

	# shorten list to 10 results
	
	if self.rangelist < resultcount:
		resultcount = len(self.rangelist)
	self.output = []
	for self.j in range(0,resultcount):
		self.output.append(self.rangelist[self.j])	
	
           
        return self.output




