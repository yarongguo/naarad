#!/usr/bin/env python
# coding=utf-8
"""
© 2014 LinkedIn Corp. All rights reserved.
Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at  http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
"""
"""
Utilities for luminol
"""
import csv
import time

import luminol.exceptions as exceptions

def compute_ema(smoothing_factor, points):
  '''
  Compute exponential moving average of a list of points.
  :param float smoothing_factor: the smoothing factor.
  :param list points: the data points.
  :return list: all ema in a list.
  '''
  ema = list()
  # The initial point has a ema equal to itself.
  if(len(points) > 0):
    ema.append(points[0])
  for i in range(1, len(points)):
    ema.append(smoothing_factor * points[i] + (1 - smoothing_factor) * ema[i - 1])
  return ema

def read_csv(csv_name):
  """
  Read data from a csv file into a dictionary.
  :param str csv_name: path to a csv file.
  :return dict: a dictionary represents the data in file.
  """
  data = {}
  if not isinstance(csv_name, (str, unicode)):
    raise exceptions.InvalidDataFormat('luminol.utils: csv_name has to be a string!')
  with open(csv_name, 'r') as csv_data:
    reader = csv.reader(csv_data, delimiter=',', quotechar='|')
    for row in reader:
      try:
        key = to_epoch(row[0])
        value = float(row[1])
        data[key] = value
      except ValueError:
        pass
  return data

def to_epoch(t_str):
  """
  Covert a timestamp string to an epoch number.
  :param str t_str: a timestamp string.
  :return int: epoch number of the timestamp.
  """
  try:
    t = time.mktime(time.strptime(t_str, "%Y-%m-%d %H:%M:%S.%f"))
  except:
    try:
      t = time.mktime(time.strptime(t_str, "%Y-%m-%d %H:%M:%S"))
    except:
      return float(t_str)
  return t