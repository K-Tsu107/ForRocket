# -*- coding: utf-8 -*-
import platform
import sys
import subprocess as sp
import numpy as np
import os
import datetime
import simplekml
from SubScript.coordinate import *

print "Simulation Start!"
try:
  print "cs2data"
  import cs2data
  print ""
  print "Calcutate"
  if 'Windows' == platform.system():
	 sp.call(['Simulation'])
  else:
  	sp.call(['./Simulation.exe'])
  print ""
  print "Simulation End!"
except:
  print "Error : Can't Calcutate...script exit"

#kmlファイルの出力スイッチ。0で出力オフ、1で出力オン
kml_frag = 1
#出力の機体名
name = u'H-xx'
#射点緯度経度高度[deg,deg,m]
Launch_LLH = np.empty(3)
Launch_LLH[0] = 40.242865
Launch_LLH[1] = 140.010450
Launch_LLH[2] = 5.0


if kml_frag:
  print "kml output..."
else:
  sys.exit()

#座標履歴ファイルの有無
os.chdir("Output_Log")
try:
  file = open('Position_log.csv')
except:
  print "LogFile Not found...script exit"
  sys.exit()


def kml_make(name,Launch_LLH):
  Log = np.loadtxt('Position_log.csv',delimiter=",",skiprows=1)
  array = Log[:,1]
  array_len = len(array)
  print ":"
  Position_ENU = np.zeros((array_len,3))
  Position_ENU[:,0] = np.array(Log[:,0])
  Position_ENU[:,1] = np.array(Log[:,1])
  Position_ENU[:,2] = np.array(Log[:,2])
  
  Position_ecef = np.zeros((array_len,3))
  Position_LLH = np.zeros((array_len,3))
  print ":"
  for i in range(array_len):
    Position_ecef[i,:] = ENU2ECEF(Position_ENU[i,:],Launch_LLH)
    Position_LLH[i,:] = ECEF2LLH(Position_ecef[i,:])
  print ":"
  
  header = 'Latitude,Longitude,Height'
  np.savetxt("Result Log 1.csv",Position_LLH,fmt = '%.5f',delimiter = ',',header = header)
  
  kml = simplekml.Kml(open=1)
  Log_LLH = []
  for i in range(array_len):
    if 0 == i % 10000:
      Log_LLH.append((Position_LLH[i,1],Position_LLH[i,0],Position_LLH[i,2]))
  print ":"
  line = kml.newlinestring(name = name)
  line.style.linestyle.width = 5
  line.style.linestyle.color = simplekml.Color.red
  line.extrude = 1
  line.altitudemode = simplekml.AltitudeMode.absolute
  line.coords = Log_LLH
  line.style.linestyle.colormode = simplekml.ColorMode.random
  kml.save(name + ".kml")



try:
  kml_make(name,Launch_LLH)
  os.chdir("../")
except:
  print "Error : Can't make kml file...script exit"
  os.chdir("../")

print "Script Complete!"
