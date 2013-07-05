import MySQLdb as mdb
import sys
from operator import itemgetter, attrgetter


class SYSlinks:
    def __init__(self):
        self.con = mdb.connect('localhost', 'msi', 'bongwater', 'sdd');
        
        

    
    def sysID(self, sysname):
        with self.con:
            self.cur = self.con.cursor(mdb.cursors.DictCursor)
            self.cur.execute("SELECT * FROM mapsolarsystems WHERE solarSystemName = (%s)", (sysname))
            self.rows = self.cur.fetchone()
            self.ID = int(self.rows["solarSystemID"])
            self.startsys = (self.rows["solarSystemName"])
            return(self.startsys, self.ID)
            

           
    def sysLinks(self, sysid):
        self.linkedsystems = []
        with self.con:
            self.cur = self.con.cursor(mdb.cursors.DictCursor)
            self.cur.execute("SELECT toSolarSystemID , fromSolarSystemID FROM mapsolarsystemjumps WHERE fromSolarSystemID = (%s)", (sysid))
            self.rows = self.cur.fetchall()                
            for self.i in range(len(self.rows)):
                self.linkedsystems.append(self.rows[self.i])
                                                                                                      
        return(self.linkedsystems)

    def gatedist(self,targetparam,maxjumps):
        
    
    
        self.pending = [] # only contains the sysID
        self.current = []
        self.done = [] # includes sysID and number of jumps
        self.blank = []
        self.adjacent = []
        self.jumps = 0
        self.currentsystem = []
        
        self.tmp2 = []
        self.inrange = []
        
        
        # lookup our startsystem
        self.targetlookup = self.sysID(targetparam)
        self.targetname =  self.targetlookup[0]
        self.targetID =  self.targetlookup[1]
        
        
        # read office list, put in the format officepairs[[officename , officeID], [....
        self.tmp1 = []
        self.officepairs = []
        
        self.officelist = []
        with open('systems.txt', 'r') as f:
                self.officelist = f.readlines()
        f.close()
        # lookup system names/IDs and put them in the appropriate format
        for self.k in range(len(self.officelist)):
            self.tmp1= [self.sysID(self.officelist[self.k].rstrip())]
            self.tmp1 = [self.tmp1[0][0], self.tmp1[0][1]]
            self.officepairs.append(self.tmp1)   
        ## End reading office list
       
        self.pending.append(self.targetID)
        while self.jumps < maxjumps:
            
#            if self.jumps == (maxjumps - 2): ## condition for extending search if nothing found
#               if len(self.inrange) == 0:
#                    maxjumps = maxjumps + 1
#                    print "Nothing found, extending search"
            self.jumps = self.jumps + 1    
            self.done.append(self.current)        #shift everything left
            self.current = self.pending        
            self.pending = self.blank    
            
            for i in range(len(self.current)):                    #take each item in current list
        
                self.adjacent = self.blank
                self.adjacent = self.sysLinks(self.current[i])    #put linked systems in adjacent
                for j in range(len(self.adjacent)):                #for each item in adjacent
        
                    self.currentsystem = self.adjacent[j]['toSolarSystemID']
                    if self.current.count(self.currentsystem)    == 0:    #check to see if we looked at it before in this loop
                        if self.done.count(self.currentsystem) == 0:    #check to see if we looked at it before ever
                            if self.pending.count(self.currentsystem ) == 0:
                                self.pending.append(self.currentsystem)    #add it to pending list
                                                            
                                for m in range(len(self.officepairs)):
                                    if self.officepairs[m][1] == self.currentsystem:
                                        if self.currentsystem == self.targetID:    #special case if it has an office in startsys
                                            self.tmp2 = [0 , self.officepairs[m][0]]
                                            self.inrange.append(self.tmp2)
                                        else:                                #the normal operation for this stage
                                            self.tmp2 = [self.jumps , self.officepairs[m][0]]
                                            self.inrange.append(self.tmp2)
    
        
        self.inrange.sort()
        return self.inrange


class RANGElinks:
    
    def distcalc(self,x0,x1,y0,y1,z0,z1):
        self.dist = float()
        self.klightyear = float("9460000000000000")
        self.xd = x1 - x0
        self.yd = y1 - y0
        self.zd = z1 - z0
        self.dist = (((self.xd * self.xd) + (self.yd * self.yd) + (self.zd * self.zd)) ** 0.5) / self.klightyear 
        return self.dist
    
    
    def syscoords(self,sysLookup):
	  
        self.con = mdb.connect('localhost', 'msi', 'bongwater', 'sdd');
        with self.con:
            self.cur = self.con.cursor(mdb.cursors.DictCursor)
            self.cur.execute("SELECT * FROM mapsolarsystems WHERE solarSystemName = (%s)", (sysLookup))
            self.rows = self.cur.fetchone()
            self._x = float(self.rows["x"])
            self._y = float(self.rows["y"])
            self._z = float(self.rows["z"])
            self.sysname = (self.rows["solarSystemName"])
        self.con.close()
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
        for self.k in range(len(self.beacon)):
            self.beacon[self.k] = self.beacon[self.k].rstrip()
 
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




