# coding: utf-8
#!/usr/bin/env python


import pysftp
import os
from ConfigUtils import *
import base64

class SFTPUtils:

  def __init__(self, configItems):
    self._config_dir =  configItems['config_dir']
    self._sftp_config_file = configItems['sftp_config_file']
    self._sftpConfigs = ConfigUtils.setConfigs(self._config_dir, self._sftp_config_file)
    self._username = None
    self._password = None
    self._hostname = None
    self._sftp = None
    self.setConfigs()

  def setConfigs(self):
    self._username =  self._sftpConfigs['username']
    if ( self._sftpConfigs['password']):
      self._password = base64.b64decode(self._sftpConfigs['password'])
    self._hostname =  self._sftpConfigs['hostname']
    self._sftp = pysftp.Connection(self._hostname, username=self._username, password=self._password)

  def getFileList(self, fileList, remoteDir=None, localDir=None, preserve_mtime=True):
    for fn in fileList:
      item = self.getFile(self._sftp, fn, remoteDir,localDir)

  @staticmethod
  def getFile(sftpConn, fname, remoteDir, localDir, preserve_mtime=True):
    fnameFull = fname
    print fnameFull
    if(not(remoteDir is None)):
      fnameFull = str(os.path.join(remoteDir, fname))
    if(not (localDir is None)):
      downloadFname = str(os.path.join(localDir, fname))
      try:
        sftpConn.get(fnameFull, downloadFname)
        print "Downloaded: " + fname
      except Exception, e:
        print "ERROR: Could not download " + fname
        print str(e)
    else:
      sftpConn.get(fnameFull, preserve_mtime)

  def closeSFTPConnection(self):
    self._sftp.close()
    return True
