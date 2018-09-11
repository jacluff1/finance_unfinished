# import libraries
import pandas as pd
import os

def string_2_float_formats(x):
    if "$" in x:
        x   =   x.replace("$","")
        x   =   x.replace(",","")
        x   =   x.replace(" ","")
        return float(x)
    elif "%" in x:
        x   =   x.replace("%","")
        x   =   x.replace(" ","")
        return float(x)/100
    else:
        return x

class DATA:

    #===============================================================================================
    # public methods
    #===============================================================================================

    def GET_DATA(self,**kwargs):
        # take care of default values and kwargs
        file_key        =   'data'
        output          =   True
        if 'file_key' in kwargs: file_key = kwargs['file_key']
        if 'output' in kwargs: output = kwargs['output']
        # search for data collection method
        if hasattr(self,file_key):
            # get data stored in attribute
            data            =   getattr(self,file_key)
            print("retrieved %s from instance" % file_key)
        elif os.path.isfile(self._filename[file_key]):
            # get the modification time of the file
            mtime           =   os.path.getmtime(self._filename[file_key])
            # convert unix timestamp to datetime
            dtime           =   datetime.datetime.fromtimestamp(mtime)
            # convert datetime to pandas datetime
            ptime           =   pd.to_datetime(dtime)
            # get current time
            now             =   pd.to_datetime('today')
            # find the time difference
            diff            =   now - ptime
            # if the number of days since last data retrieval >= 1, collect data, otherwise just load it from the file
            if diff.days >= 1:
                print("%s days since last collected data, collecting data..." % diff.days)
                data            =   self._COLLECT_DATA()
                data            =   self._FORMAT_DATA(data)
                setattr(self,file_key,data)
                self._SAVE_DATA(**kwargs)
            else:
                data            =   self._LOAD_DATA(**kwargs)
                print("%s days since last collected data, loaded data." % diff.days)
        else:
            # collect data from scratch
            print("no data found, collecting data...")
            data            =   self._COLLECT_DATA()
            data            =   self._FORMAT_DATA(data)
            setattr(self,file_key,data)
            self._SAVE_DATA(**kwargs)
        # set data as the attribute in instance
        setattr(self,file_key,data)
        if output: return data

    #===============================================================================================
    # protected methods
    #===============================================================================================

    def _LOAD_DATA(self,**kwargs):
        print("loading data...")
        file_key    =   'data'
        if 'file_key' in kwargs: file_key = kwargs['file_key']
        data        =   pd.read_csv(self._filename[file_key], index_col='Unnamed: 0')
        return data

    def _SAVE_DATA(self,**kwargs):
        print("saving data...")
        file_key    =   'data'
        if 'file_key' in kwargs: file_key = kwargs['file_key']
        data        =   getattr(self,file_key)
        if 'data' in kwargs: data = kwargs['data']
        data.to_csv(self._filename[file_key])

    def _STRING_2_FLOAT_FORMATS(self,data,column_keys):
        for key in column_keys:
            data[key]   =   data.apply(lambda x: string_2_float_formats(x[key]), axis=1)
        return data
