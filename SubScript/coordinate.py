# -*- coding: utf-8 -*-
import math
import numpy as np

def deg2rad(array):
  array_len = len(array)
  
  for i in range(array_len):
    array[i] = math.radians(array[i])
  
  return array

def rad2deg(array):
  array_len = len(array)
  
  for i in range(array_len):
    array[i] = math.degrees(array[i])
  
  return array

def ENU2ECEF(Position_ENU,Launch_LLH):
  Position_ecef = np.zeros(3)
  Launch_ecef = np.zeros(3)
  Launch_ecef = LLH2ECEF(Launch_LLH)
  
  matrix = np.array([[-math.sin(math.radians(Launch_LLH[1])),-math.sin(math.radians(Launch_LLH[0])) * math.cos(math.radians(Launch_LLH[1])),math.cos(math.radians(Launch_LLH[0])) * math.cos(math.radians(Launch_LLH[1]))],
    [math.cos(math.radians(Launch_LLH[1])),-math.sin(math.radians(Launch_LLH[0])) * math.sin(math.radians(Launch_LLH[1])),math.cos(math.radians(Launch_LLH[0])) * math.sin(math.radians(Launch_LLH[1]))],
    [0.0,math.cos(math.radians(Launch_LLH[0])),math.sin(math.radians(Launch_LLH[0]))]])
    
  Position_ecef = matrix.dot(Position_ENU) + Launch_ecef
  
  return Position_ecef


def ECEF2LLH(Position_ecef):
  #ECEF座標から緯度経度高度に変換
  #Longitude-Latitude-Height
  #Position_ecef : [x,y,z]
  Position_LLH = np.zeros(3)
  
  #WGS84 Constant
  a = 6378137.0
  f = 1.0 / 298.257223563
  b = a * (1.0 - f)
  e_sq = 2.0 * f - (f * f)
  e2_sq = (e_sq * a * a) / (b * b)
  
  p = np.sqrt(np.power(Position_ecef[0],2) + np.power(Position_ecef[1],2))
  theta = math.atan2(Position_ecef[2] * a,p * b)
  
  Position_LLH[0] = math.degrees(math.atan2(Position_ecef[2] + e2_sq * b * np.power(math.sin(theta),3),p - e_sq * a * np.power(math.cos(theta),3)))
  Position_LLH[1] = math.degrees(math.atan2(Position_ecef[1],Position_ecef[0]))
  N = a / np.sqrt(1.0 - e_sq * np.power(math.sin(math.radians(Position_LLH[0])),2))
  Position_LLH[2] = (p / math.cos(math.radians(Position_LLH[0]))) - N
  
  return Position_LLH

def LLH2ECEF(Position_LLH):
  #Position_LLH : [longitude,latitude,height] = [deg,deg,m]
  #
  Position_ecef = np.zeros(3)
  
  #WGS84 Constant
  a = 6378137.0
  f = 1.0 / 298.257223563
  e_sq = 2.0 * f - (f * f)
  
  N = a / np.sqrt(1.0 - e_sq * np.power(math.sin(math.radians(Position_LLH[0])),2))
  
  Position_ecef[0] = (N + Position_LLH[2]) * math.cos(math.radians(Position_LLH[0])) * math.cos(math.radians(Position_LLH[1]))
  Position_ecef[1] = (N + Position_LLH[2]) * math.cos(math.radians(Position_LLH[0])) * math.sin(math.radians(Position_LLH[1]))
  Position_ecef[2] = (N * (1.0 - e_sq) + Position_LLH[2]) * math.sin(math.radians(Position_LLH[0]))
  
  return Position_ecef

