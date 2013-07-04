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
        
        
#        self.officepairs = [['Abath', 30005062], ['Aedald', 30002393], ['Aeschee', 30005008], ['Agoze', 30003787], ['Aivonen', 30045340], ['Alachene', 30003042], ['Aldali', 30002216], ['Aliette', 30002698], ['Anka', 30003071], ['Aralgrund', 30002551], ['Asabona', 30000012], ['Assez', 30005224], ['Aulbres', 30003818], ['Aunenen', 30001398], ['Avair', 30002270], ['Avenod', 30002089], ['Bayuka', 30000039], ['Beke', 30005234],['Bridi', 30005034], ['Dantumi', 30001356], ['Decon', 30002635], ['Egmar', 30002099], ['Esesier', 30003842], ['Faswiba', 30003541], ['Frulegur', 30003467], ['Goinard', 30002725], ['Haine', 30005012], ['Hakonen', 30001448], ['Heydieles', 30004979], ['Horkkisen', 30002741], ['Ibash', 30002984], ['Ingunn', 30002559], ['Istodard', 30002402], ['Kehrara', 30000098], ['Kheram', 30003486], ['Korridi', 30005258], ['Krirald', 30002079], ['Kubinen', 30002767], ['Lisbaetanne', 30005007], ['Mai', 30003499], ['Maila', 30000162], ['Miroona', 30005084], ['Mod', 30004136], ['Nannaras', 30001438], ['Olettiers', 30002686], ['Ordat', 30001685], ['Otanuomi', 30000192], ['Otosela', 30000196], ['Parts', 30004998], ['Raravath', 30003530], ['Sahda', 30003474], ['Sendaya', 30000015], ['Sharza', 30005276], ['Soliara', 30004273], ['Todifrauan', 30002062], ['Toon', 30005212], ['Unertek', 30002413], ['Uuna', 30002759], ['Wiskeber', 30002554]]

        
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


 #   startLookup = sysID(self.startsys)
#    startName =  startLookup[0]
 #   startID =  startLookup[1]
 #   print "start ID" , startID
