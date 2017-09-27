# coding: utf-8
#!/usr/bin/env python


import pysftp
import os

class SFTPUtils:

  def __init__(self, configItems):
    self._username = configItems['username']
    self._password = configItems['password']
    self._hostname = configItems['hostname']
    self._sftp = pysftp.Connection(self._hostname, username=self._username, password=self._password)

  def getFileList(self, fileList, remoteDir=None, localDir=None, preserve_mtime=True):
    for fn in fileList:
      print fn
      item = self.getFile(self._sftp, fn, remoteDir,localDir)

  @staticmethod
  def getFile(sftpConn, fname, remoteDir, localDir, preserve_mtime=True):
    fnameFull = fname
    if(not(remoteDir is None)):
      fnameFull = str(os.path.join(remoteDir, fname))
    if(not (localDir is None)):
      downloadFname = str(os.path.join(localDir, fname))
      sftpConn.get(fnameFull, downloadFname)
    else:
      sftpConn.get(fnameFull, preserve_mtime)

  def closeSFTPConnection(self):
    self._sftp.close()
    return True
