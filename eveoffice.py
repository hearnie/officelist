
import sys
from operator import itemgetter, attrgetter
import sqlite3 as lite


class SystemLinks:
    def __init__(self):
#        self.con = mdb.connect('localhost', 'msi', 'bongwater', 'sdd');
	self.conlite = lite.connect('sdd.sqlite')
        
        

    
    def sysID(self, sysname):
        with self.conlite:
            cur = self.conlite.cursor()
            cur.execute("SELECT * FROM mapsolarsystems WHERE solarSystemName=? COLLATE NOCASE", (sysname,))
            rows = cur.fetchone()
            ID = int(rows[2]) # column number in table, it goes regionID, constID, systemID, systemname, x, y, z, ...
            startsys = (rows[3])
            return(startsys, ID)

           
    def sysLinks(self, sysid):
        linkedsystems = []
        with self.conlite:
            cur = self.conlite.cursor()
            cur.execute("SELECT toSolarSystemID , fromSolarSystemID FROM mapsolarsystemjumps WHERE fromSolarSystemID=? COLLATE NOCASE", (sysid,))
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


	   # read officepairs variable from database
        cur2 = self.conlite.cursor()
        cur2.execute("SELECT * FROM OfficeList")
        dbcontents = cur2.fetchall()
        tmp3 = []
        officepairs = []
        for i in dbcontents:
            tmp3 = [i[1], i[0]]
            officepairs.append(tmp3)
       
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
        
                    currentsystem = adjacent[j][0] # edited from name of column for sqlite
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
            self.cur = self.conlite.cursor()
            self.cur.execute("SELECT * FROM mapsolarsystems WHERE solarSystemName=? COLLATE NOCASE", (sysLookup,))
            self.rows = self.cur.fetchone()
            self._x = float(self.rows[4])
            self._y = float(self.rows[5])
            self._z = float(self.rows[6])
            self.sysname = (self.rows[3])
        self.conlite.close()
        return(self.sysname, self._x, self._y, self._z)
    


        




    def lydist(self,sysA,resultcount):
    
        self.beacon = []
        self.beacondist = []
        self.rangelist = []
        self.beacon = []
        
        self.conlite2 = lite.connect('sdd.sqlite')
        self.cur2 = self.conlite2.cursor()
        self.cur2.execute("SELECT solarSystemName FROM OfficeList")
        self.dbcontents = self.cur2.fetchall()
        self.j = 0
        for i in self.dbcontents:
            self.beacon.append(i[0])
            self.j += 1




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




