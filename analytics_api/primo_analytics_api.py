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
     print response
  else:
     sys.stderr.write("FAILED(1)\n")
     response=r.content
     sys.stderr.write(str(response)+"\n")
     return 1
  in_string=response
  in_string=in_string.replace("\n","")
  in_string=in_string.replace(" xmlns=\"urn:schemas-microsoft-com:xml-analysis:rowset\"","")
  try:
      tree=elementTree.fromstring(in_string)
  except:
      sys.stderr.write("parse failed(1)."+"\n")
      return outcome
if __name__=="__main__":
  sys.exit(main())
