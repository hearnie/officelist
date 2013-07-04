import MySQLdb as mdb
import sys
import eveoffice
from operator import itemgetter, attrgetter


## open the text file systems.txt and put it into 

target = raw_input("\nTarget system: ")

jumpradius = 8
routeObj = eveoffice.SYSlinks()
rangelist = routeObj.gatedist(target,jumpradius)


tableoffset = 0
tableoffsetstring = " "
for l in range(len(rangelist)):
	tableoffset = 12 - len(rangelist[l][1])
	tableoffsetstr = tableoffset * " "
	print rangelist[l][1] , tableoffsetstr,   "- " , rangelist[l][0] , " jumps"
	