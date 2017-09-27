# coding: utf-8
#!/usr/bin/env python

from optparse import OptionParser
from ConfigUtils import *
from SFTPFiles import *
#from SocrataStuff import *
#from PandasUtils import *
#from PyLogger import *
#from Queries import *
#from Utils import *
#from JobStatusEmailerComposer import *
#from ProfileDatasets import *
#from WebTasks import *

def parse_opts():
  helpmsgConfigFile = 'Use the -c to add a config yaml file. EX: fieldConfig.yaml'
  parser = OptionParser(usage='usage: %prog [options] ')
  parser.add_option('-c', '--configfile',
                      action='store',
                      dest='configFn',
                      default=None,
                      help=helpmsgConfigFile ,)

  helpmsgConfigDir = 'Use the -d to add directory path for the config files. EX: /home/ubuntu/configs'
  parser.add_option('-d', '--configdir',
                      action='store',
                      dest='configDir',
                      default=None,
                      help=helpmsgConfigDir ,)
  helpmsgjobType = 'Use the -n to specify a job name. EX: profile_fields - can either be profile_datasets or profile_fields'
  parser.add_option('-n', '--jobtype',
                      action='store',
                      dest='jobType',
                      default=None,
                      help=helpmsgjobType ,)
  helpmsgjobType = 'Use the -t to specify if hourly or not. EX: -t 1 means that its a run hourly'
  parser.add_option('-t', '--hourly',
                      action='store',
                      dest='hourly',
                      default=0,
                      help=helpmsgjobType ,)

  (options, args) = parser.parse_args()

  if  options.configFn is None:
    print "ERROR: You must specify a config yaml file!"
    print helpmsgConfigFile
    exit(1)
  elif options.configDir is None:
    print "ERROR: You must specify a directory path for the config files!"
    print helpmsgConfigDir
    exit(1)


  config_inputdir = None
  fieldConfigFile = None
  fieldConfigFile = options.configFn
  config_inputdir = options.configDir
  return fieldConfigFile, config_inputdir


def main():
  fieldConfigFile, config_inputdir = parse_opts()
  cI =  ConfigUtils(config_inputdir,fieldConfigFile  )
  configItems = cI.getConfigs()
  print configItems
  sftp = SFTPUtils(configItems)
  try:
    sftp.getFileList(configItems['files'], configItems['remote_dir'], configItems['download_dir'])
  except Exception, e:
    print "ERROR: Could not download files from the SFTP"
    print str(e)
  sftp.closeSFTPConnection()

if __name__ == "__main__":
    main()
