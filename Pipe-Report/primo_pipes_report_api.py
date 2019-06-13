#!/opt/rh/python27/root/usr/bin/python
# -*- coding: utf-8 -*-
r"""
   Author: Alex Cooper/Bernardo Gomez
   Date: August, 2016
   Purpose: delete oclc holdings
"""
import os
import sys
import re
import socks
import socket
import requests
import xml.etree.ElementTree as elementTree

def analyze_api(tree):
  outcome = 1
  delim = "|"
  start_date = ""
  job_id = ""
  pipe_name = ""
  stage = ""
  end_date = ""
  state = ""
  duration = ""
  no_records = ""
  result = ""
  results = []
  try:
      result_node = tree.find("QueryResult/ResultXml/rowset")
  except:
      sys.stderr.write("could not find rowset" + "\n")
      return "n/a",outcome
  try:
      rows = result_node.findall("Row")
  except:
      sys.stderr.write("could not find rows" + "\n")
      return "n/a",outcome
  for r in rows:
      try:
          start_date = r.find("Column1")
          start_date = start_date.text
      except:
          sys.stderr.write("could not find column1" + "\n")
      try:
          job_id = r.find("Column2")
          job_id = job_id.text
      except:
          sys.stderr.write("could not find column2" + "\n")
      try:
          pipe_name = r.find("Column3")
          pipe_name = pipe_name.text
      except:
          sys.stderr.write("could not find column3" + "\n")
      try:
          stage = r.find("Column4")
          stage = stage.text
      except:
          sys.stderr.write("could not find column4" + "\n")
      try:
          end_date = r.find("Column5")
          end_date = end_date.text
      except:
          sys.stderr.write("could not find column5" + "\n")
      try:
          state = r.find("Column6")
          state = state.text
      except:
          sys.stderr.write("could not find column6" + "\n")
      try:
          duration = r.find("Column7")
          duration = duration.text
      except:
          sys.stderr.write("could not find column7" + "\n")
      try:
          no_records = r.find("Column8")
          no_records = no_records.text
      except:
          sys.stderr.write("could not find column8" + "\n")
      result = str(start_date) + delim + str(job_id) + delim + str(pipe_name) + delim + str(stage) + delim + str(end_date) + delim + str(state) + delim + str(duration) + delim + str(no_records)
      results.append(result)
  return results,outcome

def main():

  if len(sys.argv) < 2:
     sys.stderr.write("system failure. configuration file is missing."+"\n")
     return 1

  try:
     configuration=open(sys.argv[1], 'Ur')
  except:
     sys.stderr.write("couldn't open configuration file "+sys.argv[1]+"\n")
     return 1

  pat=re.compile("(.*?)=(.*)")
  for line in configuration:
    line=line.rstrip("\n")
    m=pat.match(line)
    if m:
       if m.group(1) == "url":
          url=m.group(2)
       if m.group(1) == "path":
          path=m.group(2)
       if m.group(1) == "apikey":
          apikey=m.group(2)
       if m.group(1) == "limit":
          limit=m.group(2)

  configuration.close()

  in_string=""
  outcome=1
  socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, "127.0.0.1", 8080)
  socket.socket = socks.socksocket
  payload={'apikey':apikey,'path':path,'limit':limit}
  try:
     r=requests.get(url,params=payload)
  except:
     sys.stderr.write("api request failed."+"\n")
     return [],outcome
  return_code=r.status_code
  if return_code == 200:
     response=r.content
  else:
     sys.stderr.write("FAILED(1)\n")
     response=r.content
     sys.stderr.write(str(response)+"\n")
     return outcome
  in_string=response
  in_string=in_string.replace("\n","")
  in_string=in_string.replace(" xmlns=\"urn:schemas-microsoft-com:xml-analysis:rowset\"","")
  try:
      tree=elementTree.fromstring(in_string)
  except:
      sys.stderr.write("parse failed(1)."+"\n")
      return outcome
  results,outcome = analyze_api(tree)
  for r in results:
      print r
  return 0

if __name__=="__main__":
  sys.exit(main())
