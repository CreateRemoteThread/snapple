#!/usr/bin/python

import sys
import os
import random
import string
import socket
import base64

snap_js_src = "dmFyIHN5c3RlbSA9IHJlcXVpcmUoJ3N5c3RlbScpOwp2YXIgcGFnZSA9IHJlcXVpcmUoJ3dlYnBhZ2UnKS5jcmVhdGUoKTsKcGFnZS5zZXR0aW5ncy51c2VyQWdlbnQgPSAnTW96aWxsYS81LjAgKFgxMTsgTGludXggeDg2XzY0KSBBcHBsZVdlYktpdC81MzcuMzYgKEtIVE1MLCBsaWtlIEdlY2tvKSBDaHJvbWUvMjguMC4xNTAwLjcxIFNhZmFyaS81MzcuMzYnOwpwYWdlLnZpZXdwb3J0U2l6ZSA9IHsgd2lkdGg6IDEwMjQsIGhlaWdodDogNzY4IH07CnBhZ2UuY2xpcFJlY3QgPSB7IHRvcDogMCwgbGVmdDogMCwgd2lkdGg6IDEwMjQsIGhlaWdodDogNzY4IH07CnBhZ2Uub3BlbihzeXN0ZW0uYXJnc1sxXSwgZnVuY3Rpb24oKSB7CiAgcGFnZS5yZW5kZXIoc3lzdGVtLmFyZ3NbMl0pOwogcGhhbnRvbS5leGl0KCk7Cn0pOwoK"

# requires: PhantomJS
#           convert (ImageMagick)

PHANTOMJS = "/home/charlemagne/software/phantomjs-2.1.1-linux-x86_64/bin/phantomjs --ignore-ssl-errors=yes"

class snapAll:
  def __init__(self,urls):
    dirname = "snapple-" + ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(6))
    os.mkdir(dirname)
    os.mkdir(dirname + "/images_80")
    os.mkdir(dirname + "/images_443")
    self.screencapsDb = {} 
    for _url in urls: 
      url = _url.rstrip()
      if url in self.screencapsDb.keys():
        print " [!] skipping %s" % url
        continue
      pngName = url.replace(".","_") + ".png"
      screencap_80 = "none"
      screencap_443 = "none"
      minicap_80 = "none"
      minicap_443 = "none"
      if self._testConnection(url,80):
        command = "%s snap.js http://%s %s/%s" % (PHANTOMJS,url,dirname + "/images_80",pngName)
        print " [>] %s" % command
        os.system(command)
        command = "convert %s/%s -resize 320x280 %s/mini-%s" % (dirname + "/images_80",pngName,dirname + "/images_80",pngName)
        print " [>] %s" % command
        os.system(command)
        screencap_80 = "images_80/%s" % pngName
        minicap_80 = "images_80/mini-%s" % pngName
      if self._testConnection(url,443):
        command = "%s snap.js https://%s %s/%s" % (PHANTOMJS,url,dirname + "/images_443" ,pngName)
        print " [>] %s" % command
        os.system(command)
        command = "convert %s/%s -resize 320x280 %s/mini-%s" % (dirname + "/images_443",pngName,dirname + "/images_443",pngName)
        print " [>] %s" % command
        os.system(command)
        screencap_443 = "images_443/%s" % pngName
        minicap_443 = "images_443/mini-%s" % pngName
      self.screencapsDb[url] = (screencap_80,screencap_443,minicap_80,minicap_443)
    self._printHtml(dirname)

  def _printHtml(self,dirname):
    print " [>] printing %s/index.html" % dirname
    f = open(dirname + "/index.html","w")
    f.write("<html>\n")
    f.write("<head><title>%s</title></head>\n" % dirname)
    f.write("<table border=\"1\">\n")
    f.write("<tr><td>site</td><td>port 80</td><td>port 443</td></tr>\n")
    for key in self.screencapsDb.keys():
      f.write("<tr>\n")
      (screencap_80,screencap_443,minicap_80,minicap_443) = self.screencapsDb[key]
      f.write("<td>%s</td>\n" % key)
      if minicap_80 == "none":
        f.write("<td>none</td>\n")
      else:
        f.write("<td><a href=\"%s\"><img src=\"%s\"></a></td>\n" % (screencap_80,minicap_80))
      if minicap_443 == "none":
        f.write("<td>none</td>\n")
      else:
        f.write("<td><a href=\"%s\"><img src=\"%s\"></a></td>\n" % (screencap_443,minicap_443))
      f.write("</tr>\n")
    f.write("</table>\n")
    f.write("</html>\n")
    f.close()

  def _testConnection(self,url,port):
    sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    # print url
    try:
      result = sock.connect_ex( (url,port) )
    except:
      print " [!] exception trying to test %s:%d" % (url,port)
      sock.close()
      return False
    if result == 0:
      sock.close()
      return True
    else:
      sock.close()
      return False

if __name__ == "__main__":
  if os.path.exists("snap.js") is False:
    print " [+] creating snap.js"
    f = open("snap.js","w")
    f.write(base64.b64decode(snap_js_src))
    f.close()
  if len(sys.argv) != 2:
    print " [+] usage: ./snapple.py [list]"
    sys.exit(0)
  f = open(sys.argv[1])
  data = f.readlines()
  f.close()
  n = snapAll(data)
  os.system("~/slackmsg/ping.py recon complete")
