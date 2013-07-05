import MySQLdb as mdb
import sys
from operator import itemgetter, attrgetter

class SysLinks(object):
  def __init__(self, dbsrv=None,db=None,dbuser=None,dbpw=None):
    dbsrv = dbsrv if dbsrv is not None else 'localhost'
    db = db if db is not None else 'msi'
    dbuser = dbuser if dbuser is not None else 'bongwater'
    dbpw = dbpw if dbpw is not None else 'sdd'

    self.conn = mdb.connect(dbsrv,db,dbuser,dbpw)


  def _execute(self,cursorType,query):
    try:
      if cursorType == 'DictCursor':
        cursor = self.conn.cursor(mdb.cursors.DictCursor)
      result = cursor.execute(query)

      return result
    except Exception, e:
      print e


  def SysID(self,sysname):
    with self.conn:
      rows = self._execute(DictCursor,"SELECT * FROM mapsolarsystems WHERE solarSystemName = (%s)", (sysname)).fetchone()
      system_id = int(rows['solarSystemID'])
      system_name = rows['solarSystemName']
      return (system_name,system_id)
  def SysLinks(self,sysid):
    linked_systems = []
    with self.conn:
      rows = self._execute(DictCursor,"SELECT toSolarSystemID , fromSolarSystemID FROM mapsolarsystemjumps WHERE fromSolarSystemID = (%s)", (sysid)).fetchall()
      for row in rows:
        linked_systems.append(row)

    return linked_systems

  def GateDistance(self,target_system,max_jumps):
    systems = {}

    office_list = {}
    with open('systems.txt','r') as f:
      for line in f:
        stripped = line.strip()
        office_list.setdefault(stripped,self.SysID(stripped))
    f.close()

    systems.setdefault('target_system',self.SysID(target_system))
    systems.setdefault('pending',systems['target_system'][1])

    systems.setdefault('jumps',(0,max_jumps))
    while systems['jumps'][0]<systems['jumps'][1]:
      systems['jumps'][0] += 1
      systems.setdefault('done',[])
      if systems.get('current') is not None:
        systems['done'].append(systems['current'])
      
      systems.setdefault('current',systems['pending'])
      systems['pending'] = []
      
      for system in systems['current']:
        systems.setdefault('adjacent',self.SysLinks(system[1]))
        for adj in systems['adjacent']:
          current_system = adj['toSolarSystemID']
          if systems['current'].get(current_system) is None \
              and systems['done'].get(current_system) is None \
              and systems['pending'].get(current_system) is None:
            systems['pending'].append(current_system)
            for office in office_list:
              if office[1] is current_system:
                systems.setdefault('inrange',[]).append([0,office[0]])
              else:
                systems.setdefault('inrange',[]).append([systems['jumps'][0],office[0]])


    return systems['inrange'].sort()