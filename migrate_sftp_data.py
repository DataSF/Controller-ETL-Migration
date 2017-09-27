# coding: utf-8
#!/usr/bin/env python

from optparse import OptionParser
from ConfigUtils import *
from SFTPFiles import *
from SocrataStuff import *
from PyLogger import *
from Utils import *
from JobStatusEmailerComposer import *

def parse_opts():
  helpmsgConfigFile = '''Use the -c to add a config yaml file. EX: fieldConfig.yaml.
                         Full Example of command: python migrate_sftp_data.py -c job_configs.yaml -d configs/'''
  parser = OptionParser(usage='usage: %prog [options] ')
  parser.add_option('-c', '--configfile',
                      action='store',
                      dest='configFn',
                      default=None,
                      help=helpmsgConfigFile ,)

  helpmsgConfigDir = '''Use the -d to add directory path for the config files. EX: /home/ubuntu/configs
                        Full Example of command: python migrate_sftp_data.py -c job_configs.yaml -d configs/ '''
  parser.add_option('-d', '--configdir',
                      action='store',
                      dest='configDir',
                      default=None,
                      help=helpmsgConfigDir ,)


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
  cI =  ConfigUtils(config_inputdir,fieldConfigFile)
  configItems = cI.getConfigs()
  lg = pyLogger(configItems)
  logger = lg.setConfig()
  logger.info("****************JOB START******************")
  sc = SocrataClient(config_inputdir, configItems, logger)
  client = sc.connectToSocrata()
  clientItems = sc.connectToSocrataConfigItems()
  scrud = SocrataCRUD(client, clientItems, configItems, logger)
  sQobj = SocrataQueries(clientItems, configItems, logger)
  fileList = configItems['files'].keys()
  sftp = SFTPUtils(configItems)
  jobResults = []
  try:
    print "**** Downloading Files From the SFTP **********"
    sftp.getFileList(fileList, configItems['remote_dir'], configItems['download_dir'])
  except Exception, e:
    print "ERROR: Could not download files from the SFTP"
    print str(e)
  sftp.closeSFTPConnection()
  for fn in fileList:
    fnFullPath = configItems['download_dir']+fn
    fnConfigObj = configItems['files'][fn]
    if FileUtils.fileExists(fnFullPath):
      dictList = FileUtils.read_csv_into_dictlist(fnFullPath)
      dataset_info = {'Socrata Dataset Name': fnConfigObj['dataset_name'], 'SrcRecordsCnt':len(dictList), 'DatasetRecordsCnt':0, 'fourXFour': fnConfigObj['fourXFour'], 'row_id': ''}
      dataset_info = scrud.postDataToSocrata(dataset_info, dictList)
      jobResults.append(dataset_info)
      print dataset_info
    else:
      dataset_info = {'Socrata Dataset Name': fnConfigObj['dataset_name'], 'SrcRecordsCnt':0, 'DatasetRecordsCnt':-1, 'fourXFour': fnConfigObj['fourXFour'], 'row_id': ''}
      jobResults.append(dataset_info)
  dsse = JobStatusEmailerComposer(configItems, logger)
  dsse.sendJobStatusEmail(jobResults)



if __name__ == "__main__":
    main()
