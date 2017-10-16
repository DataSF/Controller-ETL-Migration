print fnFullPath
      headerLn = LargeFileUtils.getFileHeader(fnFullPath, ",")
      start = 0
      dataset_info = {'Socrata Dataset Name': fnConfigObj['dataset_name'], 'SrcRecordsCnt':1000, 'DatasetRecordsCnt':0, 'fourXFour': fnConfigObj['fourXFour'], 'row_id': ''}
      end = 1000
      fileLen = SubProcessUtils.getFileLen(fnFullPath)
      while start < fileLen:
        chunk = LargeFileUtils.readDictListChunk(fnFullPath, start, end, ",",  headerLn)
        #print chunk
        dataset_info = scrud.postDataToSocrata(dataset_info, chunk)
        print dataset_info
        start = start + 1000
        end = end + 1000
        dataset_info['row_id'] = 'blah'
        print dataset_info
