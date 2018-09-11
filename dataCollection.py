# import libraries
from browser import BROWSER
from data import DATA
import pandas as pd
import numpy as np

# update using parent classes
# class MASSAGE_ENVY:
#
#     def __init__(self):
#         print("\nInitializing MASSAGE_ENVY...")
#         # setting up default values
#         update                  =   True
#         if 'update' in kwargs: update = kwargs['update']
#         # get login info [pd.Series]
#         print("getting login info...")
#         self.__login            =   pd.read_csv("config/credentials.csv", index_col='name', dtype='O').loc['Envy']
#         # set filenames [dict]
#         print("collecting filenames...")
#         filename                =   {}
#         filename['raw_data']    =   "data/envy_raw_data.csv"
#         filename['data']        =   "data/envy_data.csv"
#         self.__filename         =   filename
#         # collect xpaths [dict]
#         print("collecting xpaths...")
#         xpath                   =   {}
#         xpath['checkLinks']     =   "//table[@id='check-history-table']//a[@class='link com-link']"
#         self.__xpath            =   xpath
#         # collect urls [dict]
#         print("collecting urls")
#         url                     =   {}
#         self.__url              =   url
#         # add time information
#         self.__startYear        =   2016
#         self.__currentYear      =   pd.to_datetime('today').year
#         self.__years            =   self.__GET_YEAR_LIST()
#         self.__fmt              =   '%M/%d/%Y'
#         self.__startDate        =   '10/01/2016'
#         # make sure data is present and up to date
#         if update:
#             print("checking for data/updates...")
#             self.UPDATE()
#         else:
#             self.raw_data       =   self.GET_RAW_DATA()
#             self.data           =   self.GET_DATA()
#             self.PLOT_DATA(plot=False)
#         print("finished creating MASSAGE_ENVY.")
#
#     def GET_RAW_DATA(self):
#         try:
#             return self.raw_data.copy()
#         except:
#             self.__LOAD_RAW_DATA()
#             return self.raw_data.copy()
#
#     def GET_DATA(self):
#         try:
#             return self.data
#         except:
#             try:
#                 self.__LOAD_DATA()
#             except:
#                 self.__FORMAT_RAW_DATA()
#             return self.data
#
#     def UPDATE(self):
#         try:
#             data                =   self.GET_RAW_DATA()
#         except:
#             data                =   pd.DataFrame()
#         years               =   self.__GET_YEAR_LIST()
#         for year in years:
#             print("\nstarting year %s" % year)
#             driver              =   self.__OPEN_BROWSER()
#             self.__LOGIN(driver)
#             success             =   self.__SELECT_YEAR(driver,year)
#             if not success: continue
#             links               =   driver.find_elements_by_xpath(self.__xpath['checkLinks'])
#             nChecks             =   len(links)
#             if nChecks == data[data.year==int(year)].shape[0]:
#                 driver.close()
#                 print("all checks are already included in data for year %s" % year)
#                 continue
#             for index,link in enumerate(links):
#                 date        =   link.get_attribute("outerText")
#                 if date in data.date.values:
#                     print("check %s is already included in data" % date)
#                     continue
#                 row         =   self.__GET_RAW_DATA_BY_YEAR_AND_INDEX(year,index)
#                 if row['success']:
#                     data        =   data.append(row['row'], ignore_index=True)
#             driver.close()
#         self.raw_data       =   data
#         self.__SAVE_RAW_DATA()
#         self.__FORMAT_RAW_DATA()
#         self.PLOT_DATA(plot=False)
#
#     def PLOT_DATA(self,*trim,**kwargs):
#         # set up default keyword arguments
#         values      =   dict(cashTips=True, cardTips=True, servComm=True, hourly=True, plot=True)
#         # adjust default values if given in keyword arguments
#         for key in kwargs:
#             if key in values: values[key] = kwargs[key]
#         # grab shorthands for data
#         raw         =   self.GET_RAW_DATA()
#         data        =   self.GET_DATA()
#         dates       =   data.datetime.values[trim]
#         xlim        =   dates[0], dates[-1]
#         # fit functions to describe data
#         def fitfunc1(x,a,b,c):
#             return a + b*x**c
#         # create X array to fit data
#         dates1      =   data.datetime
#         X           =   np.array([ (dates1[i]-dates1[0]).days/14 for i in range(dates1.shape[0]) ])
#         popt,pcov   =   curve_fit(fitfunc1, X, data.grossRate.values[trim])
#         Y           =   fitfunc1(X,*popt)
#         print("function fitted to data: %.2f + %.2f * (n*14)^%.2f" % (popt[0], popt[1], popt[2]) )
#         # set up figure
#         if values['plot']:
#             plt.close('all')
#             fig,ax      =   plt.subplots(2,1, sharex=True, figsize=(20,10))
#             # plot gross rate and net rate
#             ax[0].plot(dates, data.grossRate.values[trim], "bo", label='gross rate')
#             ax[0].plot(dates, data.netRate.values[trim], 'go', label='net rate')
#             ax[0].plot(dates, Y[trim], 'g', linewidth=3, label='fit to net rate')
#             ax[0].set_ylabel('$/hour', fontsize=20)
#             ax[0].set_title("Massage Envy: Hourly Rate", fontsize=24)
#             ax[0].set_xlim(xlim)
#             ax[0].set_ylim(0)
#             ax[0].legend(loc=1)
#             # plot cash tips, credit card tips, serv comm, reg hours, misc
#             if values['cashTips']: ax[1].plot(dates, (raw['Cash Tips']/data['income']).values[trim], 'go', label='cash tips : income')
#             if values['cardTips']: ax[1].plot(dates, (raw['Cred Card Tips']/data['income']).values[trim], 'bo', label='card tips: : income')
#             if values['servComm']: ax[1].plot(dates, ((raw['Serv Comm Wk1']+raw['Serv Comm Wk2'])/data['income']).values[trim], 'ro', label='serv comm : income')
#             if values['hourly']: ax[1].plot(dates, ((raw['hourly Wk1']+raw['hourly Wk2'])/data['income']).values[trim], 'yo', label='hourly : income')
#             ax[1].set_xlabel('date [year/month]', fontsize=20)
#             ax[1].set_ylabel('ratio', fontsize=20)
#             ax[1].set_title("Income Ratios", fontsize=24)
#             ax[1].tick_params(labelrotation=90)
#             ax[1].legend(loc=1)
#             ax[1].set_xlim(xlim)
#             ax[1].set_ylim(0)
#             plt.show()
#         self.params =   popt
#
#     def GET_PAY_RATE(self,date):
#         date    =   pd.to_datetime(date)
#         date0   =   self.data.datetime.values[0]
#         x       =   (date - date0).days/14
#         return self.params[0] + self.params[1]*x**self.params[2]
#
#     def GET_NET_PERCENTAGE(self):
#         netrate =   (1 - self.data.taxPercent).values
#         return np.average(netrate)
#
#     #===============================================================================================
#     # private methods
#     #===============================================================================================
#
#     def __LOAD_RAW_DATA(self):
#         print("loading raw data")
#         self.raw_data       =   pd.read_csv(self.__filename['raw_data'], index_col='Unnamed: 0').fillna(value=0)
#         self.__ADD_TIME_COLUMNS_2_RAW_DATA()
#
#     def __LOAD_DATA(self):
#         print("loading data")
#         data                =   pd.read_csv(self.__filename['data'], index_col='Unnamed: 0')
#         data['datetime']    =   pd.to_datetime(data.date)
#         self.data           =   data
#
#     def __SAVE_RAW_DATA(self):
#         print("saving raw data")
#         self.__ADD_TIME_COLUMNS_2_RAW_DATA()
#         data            =   self.raw_data
#         data            =   data.fillna(value=0)
#         data            =   data.sort_values('datetime')
#         self.raw_data   =   data
#         data.to_csv(self.__filename['raw_data'])
#
#     def __SAVE_DATA(self):
#         print("saving data")
#         data                =   self.data
#         data['datetime']    =   pd.to_datetime(self.data.date)
#         data                =   data.sort_values('datetime')
#         self.data           =   data
#         data.to_csv(self.__filename['data'])
#
#     def __FORMAT_RAW_DATA(self):
#         taxKeys             =   ['AZ INCOME TAX', 'FEDERAL INCOME TAX', 'FICA - MEDICARE', 'FICA - OASDI']
#         hrKeys              =   ['Hrs Wk1', 'Hrs Wk2']
#         timeKeys            =   ['date', 'datetime', 'year', 'month']
#         miscKeys            =   ['rate Wk1', 'rate Wk2']
#         raw                 =   self.GET_RAW_DATA()
#         Zero                =   np.zeros(raw.shape[0])
#         dic                 =   dict(tax=np.zeros_like(Zero), income=np.zeros_like(Zero), hours=np.zeros_like(Zero))
#         data                =   pd.DataFrame(dic)
#         for key in raw.keys():
#             if key in timeKeys:
#                 data[key]       =   raw[key]
#             elif key in taxKeys:
#                 data['tax']     +=  raw[key]
#             elif key in hrKeys:
#                 data['hours']   +=  raw[key]
#             else:
#                 if not key in miscKeys: data['income'] += raw[key]
#         data['grossRate']   =   data.income / data.hours
#         data['netRate']     =   (data.income - data.tax) / data.hours
#         data['taxPercent']  =   data.tax / data.income
#         self.data         =   data
#         self.__SAVE_DATA()
#
#     def __GET_YEAR_LIST(self):
#         # create empty list to collect years
#         years       =   []
#         year        =   self.__startYear
#         while year <= self.__currentYear:
#             years.append(str(year))
#             year        +=  1
#         return years
#
#     def __OPEN_BROWSER(self):
#         print("opening browser")
#         chromedriver    = 'E:/Programs/chromedriver.exe' #where you have the file
#         driver          =   webdriver.Chrome(chromedriver)
#         # geckodriver     =   "E:/Programs/geckodriver.exe"
#         # driver          =   webdriver.Firefox()
#         driver.implicitly_wait(1)
#         driver.maximize_window()
#         return driver
#
#     def __LOGIN(self,driver):
#         print("logging in")
#         # navigate to web page
#         driver.get(self.__login.url)
#         # enter in username
#         driver.find_element_by_id("user_id").send_keys(self.__login.username)
#         # enter in password
#         driver.find_element_by_id("password").send_keys(self.__login.password)
#         # submit login info
#         driver.find_element_by_id("login-button").click()
#         # add base url to instance
#         self.__url['base_url']  =   driver.current_url
#
#     def __GOTO_INTERNAL_IFRAME(self,driver):
#         # go to base url
#         driver.get(self.__url['base_url'])
#         # click on "inquiries"
#         driver.find_element_by_id("in_EMPINQ").click()
#         # click on "check history"
#         driver.find_element_by_id("CheckHistory_sub").click()
#         # switch frames
#         driver.switch_to_frame("internal-iframe")
#
#     def __SELECT_YEAR(self,driver,year):
#         self.__GOTO_INTERNAL_IFRAME(driver)
#         attempts    =   1
#         while attempts <= 10:
#             try:
#                 options     =   driver.find_element_by_id("yearsAsOptions")
#                 options     =   Select(options)
#                 options.select_by_value(year)
#                 print("able to select year %s from dropdown after %s attempts" % (year,attempts))
#                 return True
#             except:
#                 attempts    +=  1
#                 driver.implicitly_wait(1)
#                 driver.refresh()
#         print("unable to select year %s from dropdown after %s attempts" % (year,attempts))
#         driver.close()
#         return False
#
#     def __OPEN_LINK(self,driver,year,index):
#         success     =   self.__SELECT_YEAR(driver,year)
#         if not success: return False
#         actions     =   ActionChains(driver)
#         attempts    =   1
#         # "//table[@id='check-history-table']//a[@class='link com-link']"
#         while attempts <= 10:
#             try:
#                 link        =   driver.find_elements_by_xpath(self.__xpath['checkLinks'])[index]
#                 driver.execute_script("arguments[0].scrollIntoView();", link)
#                 link.click()
#                 print("able to open up check link after %s attempts" % attempts)
#                 return True
#             except:
#                 pdb.set_trace()
#                 attempts    +=  1
#                 driver.implicitly_wait(5)
#                 # driver.refresh()
#         print("unable to open check link after %s attempts" % attempts)
#         return False
#
#     def __ADD_TIME_COLUMNS_2_RAW_DATA(self):
#         data                =   self.raw_data
#         data['datetime']    =   pd.to_datetime(data.date)
#         data['year']        =   data.apply(lambda x: x['datetime'].year, axis=1)
#         data['month']       =   data.apply(lambda x: x['datetime'].month, axis=1)
#
#     def __GET_RAW_DATA_BY_YEAR_AND_INDEX(self,year,index):
#         # open link in new window
#         driver              =   self.__OPEN_BROWSER()
#         # login
#         self.__LOGIN(driver)
#         # open link
#         success             =   self.__OPEN_LINK(driver,year,index)
#         if not success:
#             driver.close()
#             print("paycheck retrieval failed")
#             return dict(success=False, row=None)
#         # switch to paycheck details frame
#         driver.switch_to_frame("details-iframe")
#         # initialize empty dictionary to collect results
#         results             =   {}
#         # get row index (date)
#         header              =   driver.find_element_by_class_name("com-h2")
#         date                =   header.get_attribute("textContent")
#         date                =   date[-10:]
#         results['date']     =   date
#         results['datetime'] =   pd.to_datetime(date)
#         # xpath to income rows relative to earnings-detail table
#         iRows_xpath         =   "//table[@id='earnings-detail']/tbody/tr"
#         # gather income rows
#         iRows               =   driver.find_elements_by_xpath(iRows_xpath)
#         # clip header and column names
#         iRows               =   iRows[2:]
#         # loop through income rows to extract data
#         for i,row in enumerate(iRows):
#             # xpath to row values
#             xpaths              =   iRows_xpath + "[%s]/td" % (i+3)
#             # get list of values
#             values              =   driver.find_elements_by_xpath(xpaths)
#             # trim values to only include [description, hours, rate, amount]
#             values              =   values[:4]
#             # extract data from income values
#             key                 =   values[0].get_attribute("innerText")
#             if key == 'Reg Hrs Wk1':
#                 results['Hrs Wk1']      =   values[1].get_attribute("innerText")
#                 results['rate Wk1']     =   values[2].get_attribute("innerText")
#                 results['hourly Wk1']   =   values[3].get_attribute("innerText")
#             elif key == 'Reg Hrs Wk2':
#                 results['Hrs Wk2']      =   values[1].get_attribute("innerText")
#                 results['rate Wk2']     =   values[2].get_attribute("innerText")
#                 results['hourly Wk2']   =   values[3].get_attribute("innerText")
#             else:
#                 results[key]            =   values[3].get_attribute("innerText")
#         # xpath to tax rows
#         tRows_xpath         =   "//table[@id='taxes-detail']/tbody/tr"
#         # gather tax rows
#         tRows               =   driver.find_elements_by_xpath(tRows_xpath)
#         # clip header and column names
#         tRows               =   tRows[2:]
#         # loop through tax rows to extract data
#         for i,row in enumerate(tRows):
#             # get xpath to row values
#             xpaths              =   tRows_xpath + "[%s]/td" % (i+3)
#             # get list of values
#             values              =   driver.find_elements_by_xpath(xpaths)
#             # extract data from tax values
#             key                 =   values[0].get_attribute("innerText")
#             results[key]        =   values[1].get_attribute("innerText")
#         # make row into DataFrame
#         row                 =   pd.Series(results)
#         # close new window
#         driver.close()
#         print("retrieved paycheck for %s" % date)
#         return dict(success=True, row=row)
#
# class GOOGLE_CALENDAR:
#
#     def __init__(self,**kwargs):
#         print("\nInitializing hours...")
#         # setting up default values
#         update                  =   True
#         if 'update' in kwargs: update = kwargs['update']
#         # get login info [pd.Series]
#         print("getting login info...")
#         self.__login            =   pd.read_csv("config/credentials.csv", index_col='name', dtype='O').loc['hours']
#         print("collecting filenames...")
#         self.__filename         =   "data/hours_data.csv"
#         print("collecting xpaths...")
#         xpath                   =   {}
#         xpath['week']           =   "//div[@role='row']/div[@role='gridcell']"
#         xpath['nextWeek']       =   "//div[@aria-label='Next week']"
#         self.__xpath            =   xpath
#         # collect urls [dict]
#         print("collecting urls")
#         url                     =   {}
#         url['asuLogin']         =   "https://weblogin.asu.edu/cas/login"
#         self.__url              =   url
#         # add time information
#         self.__fmt              =   '%H:%M'
#         # other attributes
#         self.today              =   pd.to_datetime('today')
#         self.jobs               =   dict(amber=["Envy", "Cortiva"], jacob=[])
#         # make sure data is present and up to date
#         if update:
#             print("checking for data/updates...")
#             self.UPDATE()
#         print("finished creating hours.")
#
#     #===============================================================================================
#     # public methods
#     #===============================================================================================
#
#     def UPDATE(self):
#         # if file exists load file, otherwise create empty DataFrame. Open up Google calendar and gather all the hour data for weeks with entries. Save the data to self.__filename
#         if os.path.isfile(self.__filename):
#             data        =   self.__LOAD_DATA()
#         else:
#             data        =   pd.DataFrame()
#         update      =   self.__COLLECT_CALENDAR_HOURS()
#         data        =   data.append(update)
#         self.data   =   data
#         self.__SAVE_DATA()
#
#     def GET_DATA(self):
#         return self.data
#
#     #===============================================================================================
#     # private methods
#     #===============================================================================================
#
#     def __LOGIN(self):
#         # open webpage
#         chromedriver    = 'E:/Programs/chromedriver.exe' #where you have the file
#         self.driver     =   webdriver.Chrome(chromedriver)
#         self.driver.implicitly_wait(5)
#         # navigate to ASU login page
#         self.driver.get(self.__url['asuLogin'])
#         # enter username
#         self.driver.find_element_by_id("username").send_keys(self.__login.username)
#         # enter in password
#         self.driver.find_element_by_id("password").send_keys(self.__login.password)
#         # submit login info
#         self.driver.find_element_by_class_name("submit").click()
#         # navigate to web google calendar
#         self.driver.get(self.__login.url)
#         # enter in email
#         self.driver.find_element_by_id("identifierId").send_keys(self.__login.email)
#         # click next button
#         self.driver.find_element_by_id("identifierNext").click()
#
#     def __CREATE_EMPTY_DATA_DICTIONARY(self):
#         data                =   {}
#         for key in (self.jobs):
#             for jobname in self.jobs[key]:
#                 data[jobname + "Hours"] =   []
#         data['weekdate']    =   []
#         return data
#
#     def __GET_WEEKDATE(self,nWeek):
#         if nWeek == 1:
#             today   =   pd.to_datetime('today')
#         else:
#             url     =   self.driver.current_url
#             today   =   url[url.find("week/")+5:]
#             today   =   pd.to_datetime(today)
#         date0   =   today - pd.DateOffset(today.isoweekday())
#         return "%s/%s/%s" % (date0.month,date0.day,date0.year)
#
#     def __READ_CALENDAR_EVENT(self,event):
#         # get text content
#         text    =   event.get_attribute("textContent")
#         # trim text content
#         text    =   text[:text.find(",")]
#         # split the text into start and finish sections
#         i       =   text.find("to")
#         start   =   text[:i-1]
#         finish  =   text[i+3:]
#         # convert start and finish times to datetime instances
#         start   =   dt.strptime(start, self.__fmt)
#         finish  =   dt.strptime(finish, self.__fmt)
#         # find time difference in hours
#         hrs     =   (finish - start).seconds/3600
#         return hrs
#
#     def __COLLECT_CALENDAR_HOURS(self):
#         # get an empty dictionary to collect data
#         data            =   self.__CREATE_EMPTY_DATA_DICTIONARY()
#         # login and goto calendar
#         self.__LOGIN()
#         # wait for page to load
#         WebDriverWait(self.driver, 30).until(EC.presence_of_element_located( (By.XPATH, self.__xpath['week']) ))
#         # initiate nWeeks counter
#         nWeek           =   1
#         # continue to go through each week until there are no events for any job
#         while True:
#             print("\nstarting week %s..." % nWeek)
#             # go through entries in jobs dictionary
#             # get the starting date of that week
#             data['weekdate'].append(self.__GET_WEEKDATE(nWeek))
#             for key in self.jobs:
#                 print("starting %s's jobs..." % key)
#                 # go through each job in the key's list
#                 for jobindex,jobname in enumerate(self.jobs[key]):
#                     print("starting %s..." % jobname)
#                     # make a key to search for calendar events
#                     if key == 'amber':
#                         search_key          =   "//div[contains(text(), '%s, Calendar: Amber Cluff')]" % jobname
#                     else:
#                         search_key          =   "//div[contains(text(), '%s, Jacob Cluff')]" % jobname
#                     # get the events
#                     events              =   self.driver.find_elements_by_xpath(search_key)
#                     # if there aren't any events for the job, see if loop should be terminated
#                     if len(events) == 0:
#                         while True:
#                             vacation            =   input("is %s taking a vacation from %s this week? [y/n]\n" % (key,jobname) )
#                             if vacation == 'y':
#                                 print("this week is marked as vacation for this job, moving on to next job...")
#                                 break
#                             elif vacation == 'n':
#                                 print("this week is not marked as vacation, stopping calander search...")
#                                 # put data into DataFrame
#                                 try:
#                                     data                =   pd.DataFrame(data)
#                                 except:
#                                     lengths             =   []
#                                     for key in data: lengths.append(len(data[key]))
#                                     size                =   min(lengths)
#                                     print("dropping previously collected data for this week...")
#                                     for key in data:
#                                         data[key]           =   data[key][:size]
#                                     data                =   pd.DataFrame(data)
#                                 # close browser and return the DataFrame
#                                 self.driver.close()
#                                 return data
#                             else:
#                                 print("answer was not given in required format; please enter either 'y' or 'n'.")
#                     # instanciate hour counter for job's weekly hours
#                     hours1              =   0
#                     # go through each event that mathces the search key
#                     for event in events:
#                         hours2              =   self.__READ_CALENDAR_EVENT(event)
#                         print("week %s: job %s: hours %s" % (nWeek,key,hours2))
#                         assert hours2 > 0, "problem extracting hours from event"
#                         # add event hours to weekly hours
#                         hours1              +=  hours2
#                     # add job's weekly hours to data
#                     data[jobname+"Hours"].append(hours1)
#             # click "next week" button
#             self.driver.find_element_by_xpath(self.__xpath['nextWeek']).click()
#             # increment nWeek
#             nWeek               +=  1
#
#     def __SAVE_DATA(self):
#         self.data.to_csv(self.__filename)
#
#     def __LOAD_DATA(self):
#         self.data       =   pd.read_csv(self.__filename, index_col='Unnamed: 0')
#
# class DESERT_FINANTIAL:
#
#     def __init__(self,**kwargs):
#         # set up default values
#         update                  =   True
#         if 'update' in kwargs: update = kwargs['update']
#         print("\nInitializing DESERT_FINANTIAL instance...")
#         # get login info [pd.Series]
#         print("getting login info...")
#         self.__login            =   pd.read_csv("config/credentials.csv", index_col='name', dtype='O').loc['DF']
#         # set filenames [dict]
#         print("collecting filenames...")
#         filename                =   {}
#         filename['data']        =   "data/DF_data.csv"
#         filename['export']      =   'C:/Users/Djakjake/Downloads/ExportedTransactions.csv'
#         self.__filename         =   filename
#         # collect xpaths [dict]
#         print("collecting xpaths...")
#         xpath                   =   {}
#         xpath['username']       =   "//input[@placeholder='Username']"
#         xpath['password']       =   "//input[@placeholder='Password']"
#         xpath['login']          =   "//button[@id='username-btn']"
#         xpath['checking']       =   "//ul[@aria-label='Checking Account']/li[2]/a"
#         xpath['export']         =   "//a[@id='export_transactions']"
#         xpath['select']         =   "//input[@id='ext-gen39']"
#         xpath['download']       =   "//div[@id='ext-gen43']//div[contains(text(), 'CSV')]"
#         xpath['startDate']      =   "//input[@id='Parameters_StartDate']"
#         xpath['export_btn']     =   "//button[@id='ext-gen35']"
#         xpath['logout1']        =   "//button[@id='profile_nav_toggle']"
#         xpath['logout2']        =   "//a[@title='Log Out']"
#         xpath['priusV']         =   "//li[@id='account_type_1651']//div[@class='account-type-total']"
#         xpath['savings_total']  =   "//li[@id='account_type_1495']//div[@class='account-type-total']"
#         xpath['checking_total'] =   "//li[@id='account_type_1492']//div[@class='account-type-total']"
#         self.__xpath            =   xpath
#         # collect urls [dict]
#         print("collecting urls")
#         url                     =   {}
#         self.__url              =   url
#         # add time information
#         self.__startDate        =   '01/01/2015'
#         # make sure data is present and up to date
#         self.data               =   self.GET_DATA(update=update)
#         print("finished creating DESERT_FINANTIAL instance.")
#
#     #===============================================================================================
#     # public methods
#     #===============================================================================================
#
#     def GET_DATA(self,**kwargs):
#         # set up default values
#         update          =   False
#         if 'update' in kwargs: update = kwargs['update']
#         # check if data file exists
#         if os.path.isfile(self.__filename['data']):
#             # update data if necessary
#             if update: self.__UPDATE()
#             # load and return data
#             return self.__LOAD_DATA()
#         else:
#             # create the data by exporting the entire history from startDate till today, save it and return it
#             self.data       =   self.__EXPORT_DATA(self.__startDate)
#             self.__SAVE_DATA()
#             return self.data
#
#     #===============================================================================================
#     # private methods
#     #===============================================================================================
#
#     def __UPDATE(self):
#         # load previously collected data
#         data        =   self.__LOAD_DATA()
#         # get date of last entry
#         date0       =   data['Posting Date'].values[0]
#         # use date of last entry as starting point for exporting new data
#         upData      =   self.__EXPORT_DATA(date0)
#         # append updated data to existing data
#         self.data   =   upData.append(data)
#         # save updated data
#         self.__SAVE_DATA()
#
#     def __LOAD_DATA(self):
#         print("loading data...")
#         data            =   pd.read_csv(self.__filename['data'], index_col='Unnamed: 0')
#         return data
#
#     def __SAVE_DATA(self):
#         print("saving data...")
#         self.data.to_csv(self.__filename['data'])
#
#     def __OPEN_BROWSER(self):
#         print("opening browser...")
#         chromedriver    = 'E:/Programs/chromedriver.exe' #where you have the file
#         driver          =   webdriver.Chrome(chromedriver)
#         driver.implicitly_wait(1)
#         driver.maximize_window()
#         return driver
#
#     def __LOGIN(self,driver):
#         # navigate to web page
#         driver.get(self.__login.url)
#         # enter in username
#         driver.find_element_by_xpath(self.__xpath['username']).send_keys(self.__login.username)
#         # enter in password
#         driver.find_element_by_xpath(self.__xpath["password"]).send_keys(self.__login.password)
#         # submit login info
#         driver.find_element_by_xpath(self.__xpath["login"]).click()
#         # add base url to instance
#         self.__url['base_url']  =   driver.current_url
#
#     def __LOGOUT(self,driver):
#         # # setup explicit wait
#         # wait        =   WebDriverWait(driver,10)
#         # # click logout dropdown button
#         # dropdown    =   wait.until(EC.element_to_be_clickable((By.XPATH, self.__xpath['logout1'])))
#         # driver.execute_script("arguments[0].scrollIntoView();", dropdown)
#         # dropdown.click()
#         # # click the logout link
#         # wait.until(EC.element_to_be_clickable((By.XPATH, self.__xpath['logout2']))).click()
#         # diver.find_element_by_xpath(self.__xpath['logout2']).click()
#         # # close browser
#         driver.close()
#
#     def __GRAB_ELEMENT(self,wait,key):
#         return wait.until(EC.visibility_of_element_located((By.XPATH, self.__xpath[key])))
#
#     def __GET_AMOUNT(self,*par):
#         amount      =   self.__GRAB_ELEMENT(*par)
#         amount      =   amount.get_attribute('innerText')
#         amount      =   amount.replace("$","")
#         amount      =   amount.replace(",","")
#         return float(amount)
#
#     def __ADD_BALANCES(self,wait):
#         # add the loan amount on the Prius V
#         print("grabbing loan amount for prius V...")
#         self.balance_priusV     =   self.__GET_AMOUNT(wait,'priusV')
#         # add the total amount in savings
#         print("grabbing total in savings...")
#         self.balance_savings    =   self.__GET_AMOUNT(wait,'savings_total')
#         # add checking total
#         print("grabbing total in checking...")
#         self.balance_checking   =   self.__GET_AMOUNT(wait,'checking_total')
#
#     def __EXPORT_DATA(self,date):
#         # open browser
#         driver      =   self.__OPEN_BROWSER()
#         # login
#         self.__LOGIN(driver)
#         # setup explicit wait
#         wait        =   WebDriverWait(driver,10)
#         # add updated balances to checking, savings, and priusV loan
#         self.__ADD_BALANCES(wait)
#         # click on the checking account
#         checking    =   self.__GRAB_ELEMENT(wait,'checking')
#         checking.click()
#         # click on the export button
#         export      =   self.__GRAB_ELEMENT(wait,'export')
#         export.click()
#         # click on 'Select'
#         select      =   self.__GRAB_ELEMENT(wait,'select')
#         select.click()
#         # select csv download option
#         download    =   self.__GRAB_ELEMENT(wait,'download')
#         download.click()
#         # enter in start date
#         startDate   =   self.__GRAB_ELEMENT(wait,'startDate')
#         startDate.send_keys(date) # MM/DD/YYYY
#         # click on the export button
#         button      =   self.__GRAB_ELEMENT(wait,'export_btn')
#         button.click()
#         # load exported file
#         attempts    =   0
#         while not os.path.isfile(self.__filename['export']):
#             attempts    +=  1
#             if attempts == 11: break
#         try:
#             data        =   pd.read_csv(self.__filename['export'])
#             print("loaded export file after %s attempts" % attempts)
#         except:
#             print("couldn't load export file")
#             pdb.set_trace()
#         # delete exported file
#         try:
#             os.remove(self.__filename['export'])
#             print("deleted export file")
#         except OSError as e: # name the Exception `e`
#             print("Failed with:", e.strerror) # look what it says
#             print("Error code:", e.code)
#         # logout and close browser
#         self.__LOGOUT(driver)
#         # return exported file as DataFrame
#         return data

class NAVIENT(BROWSER,DATA):

    def __init__(self,cred_key,**kwargs):
        print("\nInitializing NAVIENT...")
        # handle kwargs
        output              =   False
        if 'output' in kwargs:
            output              =   kwargs['output']
        else:
            kwargs['output']    =   output
        # get login info [pd.Series]
        print("getting login info...")
        self._login         =   self._GET_CREDENTIALS(cred_key)
        # set filenames [dict]
        print("collecting filenames...")
        filename            =   {}
        filename['data']    =   "data/%s_data.csv" % cred_key
        self._filename      =   filename
        # collect xpaths [dict]
        print("collecting xpaths...")
        xpath               =   {}
        xpath['username']   =   "//input[@name='UserID']"
        xpath['password']   =   "//input[@name='Password']"
        xpath['login']      =   "//input[@id='LogInSubmit']"
        xpath['SSN1']       =   "//input[@name='tSSN1']"
        xpath['SSN2']       =   "//input[@name='tSSN2']"
        xpath['SSN3']       =   "//input[@name='tSSN3']"
        xpath['DOB1']       =   "//input[@id='dob1']"
        xpath['DOB2']       =   "//input[@id='dob2']"
        xpath['DOB3']       =   "//input[@id='dob']"
        xpath['submit']     =   "//button[@id='Submit']"
        xpath['amount']     =   "//tbody[@id='transactions-info-container']/tr"
        xpath['details']    =   "//a[@href='/Loans/AllLoanDetails']"
        xpath['table']      =   "//tbody[@id='transactions-info-container']/tr"
        self._xpath         =   xpath
        # collect urls [dict]
        print("collecting urls")
        url                 =   {}
        self._url           =   url
        # make sure data is present and up to date
        self.GET_DATA(**kwargs)
        print("finished creating NAVIENT.")

    #===============================================================================================
    # methods used in BROWSER
    #===============================================================================================

    #===============================================================================================
    # methods used in DATA
    #===============================================================================================

    def _COLLECT_DATA(self):
        # create empty table to hold data
        data                =   pd.DataFrame()
        # open browser
        driver,wait         =   self._OPEN_BROWSER()
        # login
        self._LOGIN(driver,wait,frame_index=0)
        # finish authentification
        auth_dict           =   dict(SSN1=self._login.SSN[:3], SSN2=self._login.SSN[3:5], SSN3=self._login.SSN[5:], DOB1=self._login.DOB[:2], DOB2=self._login.DOB[2:4], DOB3=self._login.DOB[4:])
        for key in auth_dict:
            self._GRAB_ELEMENT(driver,wait,key).send_keys(auth_dict[key])
            self._GRAB_ELEMENT(driver,wait,'submit').click()
        # get the number of loans
        nLoans              =   len(self._GRAB_ELEMENTS(driver,wait,'amount'))
        # create an empty array to collect amounts
        amounts             =   np.empty(nLoans, dtype='O')
        # go through each loan
        for i in range(nLoans):
            # get xpath to loan amount
            xpath           =   self._xpath['amount'] + "[%s]/td[@class='loan amount']" % (i+1)
            # grab the amount
            amount          =   driver.find_element_by_xpath(xpath).get_attribute("innerText")
            # add amount to amounts array
            amounts[i]      =   amount
        # scroll halfway down the page so details button is in view
        self._SCROLL(driver,.5)
        # click the loan details button
        self._GRAB_ELEMENT(driver,wait,'details').click()
        # get the number of rows on the table
        nRows               =   len(driver.find_elements_by_xpath(self._xpath['table']))
        # go through each row in the table
        for i in range(nRows):
            # get empty list to put row info
            row1                =   []
            # get xpaths to list of elements in the row
            xpaths              =   self._xpath['table'] + "[%s]/td" % (i+1)
            # go through each element in the row
            for element in driver.find_elements_by_xpath(xpaths):
                # add the data to the row list
                row1.append(element.get_attribute("title"))
            # make the row data into a dictionary
            row2                =   dict(name=row1[0], balance=row1[1], APR=row1[2], dueDate=row1[3])
            # make the row data dictionary into a Series
            row3                =   pd.Series(row2)
            # append the row Series to the data
            data                =   data.append(row3, ignore_index=True)
        # filter out any paidoff loans from data
        data                =   data[data.balance != '$0.00']
        # add amounts to data
        data['minPayment']  =   amounts
        # close browser
        driver.close()
        return data

    def _FORMAT_DATA(self,data):
        data    =   self._STRING_2_FLOAT_FORMATS(data,["APR", "balance", "minPayment"])
        return data

    #===============================================================================================
    # methods used in LOAN
    #===============================================================================================

    def GET_LOAN_META(self):
        data        =   self.data.copy()
        meta        =   []
        for i in range(data.shape[0]):
            try:
                row                 =   data.iloc[i]
                row1                =   dict()
                row1["loan"]        =   row["name"]
                row1["balance"]     =   row["balance"]
                row1["minPayment"]  =   row["minPayment"]
                row1["APR"]         =   row["APR"]
                row1["dueDay"]      =   pd.to_datetime(row["dueDate"]).day
                meta.append(row1)
            except:
                print("loan with index %s has been paid off" % i)
        return meta

    #===============================================================================================
    # methods defined in BROWSER, but implemented in NAVIENT
    #===============================================================================================

class DF_CARDMEMBER(BROWSER,DATA):

    def __init__(self,**kwargs):
        print("\nInitializing DF_CARDMEMBER...")
        # handle kwargs
        file_key            =   "meta"
        output              =   False
        if 'file_key' in kwargs:
            file_key            =   kwargs['file_key']
        else:
            kwargs['file_key']  =   file_key
        if 'output' in kwargs:
            output              =   kwargs['output']
        else:
            kwargs['output']    =   output
        # get login info [pd.Series]
        print("getting login info...")
        self._login         =   self._GET_CREDENTIALS('DF-Cardmember')
        # set filenames [dict]
        print("collecting filenames...")
        filename            =   {}
        filename['meta']    =   "data/df_cardmember_%s.csv" % file_key
        self._filename      =   filename
        # collect xpaths [dict]
        print("collecting xpaths...")
        xpath               =   {}
        xpath['username']   =   "//input[@id='userId']"
        xpath['continue']   =   "//button[@id='nextButton']"
        xpath['question']   =   "//span[@id='challengeQuestion']"
        xpath['answer']     =   "//input[@id='answer']"
        xpath['next']       =   "//button[@name='Next']"
        xpath['password']   =   "//input[@name='password']"
        xpath['login']      =   "//button[@name='Log in']"
        xpath['table']      =   "//table[@id='transactionDetailTable_summary']/tbody/tr"
        xpath['closing']    =   xpath['table'] + "[2]/td[2]/div[2]"
        xpath['due']        =   xpath['table'] + "[3]/td[2]/div[2]"
        self._xpath         =   xpath
        # collect urls [dict]
        print("collecting urls")
        url                 =   {}
        self._url           =   url
        # make sure data is present and up to date
        self.GET_DATA(**kwargs)
        print("finished creating DF_CARDMEMBER instance.")

    #===============================================================================================
    # methods used in BROWSER
    #===============================================================================================

    def _LOGIN(self,driver,wait):
        driver.get(self._login.url)
        self._GRAB_ELEMENT(driver,wait,'username').send_keys(self._login.username)
        self._GRAB_ELEMENT(driver,wait,'continue').click()
        question    =   self._GRAB_ELEMENT(driver,wait,'question').get_attribute("innerText")
        question1   =   None
        question2   =   "What are the last five digits of your student id?"
        question3   =   "What was the name of your best friend in high-school?"
        if question == question2:
            self._GRAB_ELEMENT(driver,wait,'answer').send_keys(self._login.answer2)
        elif question == question3:
            self._GRAB_ELEMENT(driver,wait,'answer').send_keys(self._login.answer3)
        else:
            self._GRAB_ELEMENT(driver,wait,'answer').send_keys(self._login.answer1)
        self._GRAB_ELEMENT(driver,wait,'next').click()
        self._GRAB_ELEMENT(driver,wait,'password').send_keys(self._login.password)
        self._GRAB_ELEMENT(driver,wait,'login').click()
        self._url['base_url']   =   driver.current_url

    #===============================================================================================
    # methods used in DATA
    #===============================================================================================

    def _COLLECT_DATA(self):
        # open browser
        driver,wait     =   self._OPEN_BROWSER()
        # login
        self._LOGIN(driver,wait)
        # create empty DataFrame to hold data
        data            =   pd.DataFrame()
        # go through each row in the table
        for i in np.arange(1,4):
            # get path to the row
            row_xpath        =   self._xpath['table'] + '[%s]/' % i
            # collect the first two items in the row through a loop
            for j in np.arange(1,3):
                # make sure to skip the date entries
                if i >= 2 & j >=2: continue
                # get the xpath to the item
                item_xpath              =   row_xpath + 'td[%s]/' % j
                name_xpath              =   item_xpath + 'div[1]' % j
                amount_xpath            =   item_xpath + 'div[2]/span' % j
                # add temporary xpaths to instance
                self._xpath['name']     =   name_xpath
                self._xpath['amount']   =   amount_xpath
                # collect the name and value for the item
                name                    =   self._GRAB_ELEMENT(driver,wait,'name').get_attribute("innerText")
                amount                  =   self._GRAB_ELEMENT(driver,wait,'amount').get_attribute("innerText")
                # put row results into a dictionary
                row                     =   dict(name=name, amount=amount)
                # make row dictionary into Series
                row                     =   pd.Series(row)
                # append row Series into DataFrame
                data                    =   data.append(row, ignore_index=True)
        # get closing and due dates
        closing         =   self._GRAB_ELEMENT(driver,wait,'closing').get_attribute("innerText")
        due             =   self._GRAB_ELEMENT(driver,wait,'due').get_attribute("innerText")
        # add closing and due dates data
        row1            =   dict(name="Closing Date", value=closing)
        row2            =   dict(name="Due Date", value=due)
        row1            =   pd.Series(row1)
        row2            =   pd.Series(row2)
        data            =   data.append(row1, ignore_index=True)
        data            =   data.append(row2, ignore_index=True)
        # close browser
        driver.close()
        return data

    def _FORMAT_DATA(self,data):
        return self._STRING_2_FLOAT_FORMATS(data,["value"])

    #===============================================================================================
    # methods used in LOAN
    #===============================================================================================

    def GET_LOAN_META(self):
        data                =   self.meta.copy()
        meta                =   []
        results             =   {}
        results["loan"]     =   "DF_Cardmember"
        mapDict             =   dict(balance="Current Balance", pending="Pending Transactions", previousBalance="Last Statement Balance", minPayment="Minimum Payment", dueDay="Due Date")
        for key in mapDict:
            results[key]        =   data[data.name==mapDict[key]].value.values[0]
        results['dueDay']   =   pd.to_datetime(results['dueDay']).day
        results['APR']      =   .1799
        meta.append(results)
        return meta

class CARRINGTON(BROWSER,DATA):

    def __init__(self,**kwargs):
        print("\nInitializing CARRINGTON...")
        # handle kwargs
        file_key            =   "meta"
        output              =   False
        if 'file_key' in kwargs:
            file_key            =   kwargs['file_key']
        else:
            kwargs['file_key']  =   file_key
        if 'output' in kwargs:
            output              =   kwargs['output']
        else:
            kwargs['output']    =   output
        # get login info [pd.Series]
        print("getting login info...")
        self._login         =   self._GET_CREDENTIALS('Carrington')
        # set filenames [dict]
        print("collecting filenames...")
        filename            =   {}
        filename[file_key]  =   "data/carrington_%s.csv" % file_key
        self._filename      =   filename
        # collect xpaths [dict]
        print("collecting xpaths...")
        xpath               =   {}
        xpath['username']   =   "//input[@id='UserName']"
        xpath['password']   =   "//input[@id='Password']"
        xpath['login']      =   "//button[@id='btnLogin']"
        xpath['details']    =   "//div[@id='myloan-details-tab']"
        self._xpath         =   xpath
        # collect urls [dict]
        print("collecting urls")
        url                 =   {}
        self._url           =   url
        # make sure data is present and up to date
        self.GET_DATA(**kwargs)
        print("finished creating CARRINGTON instance.")

    #===============================================================================================
    # methods used in BROWSER
    #===============================================================================================

    #===============================================================================================
    # methods used in DATA
    #===============================================================================================

    def _COLLECT_DATA(self):
        # open browser
        driver,wait     =   self._OPEN_BROWSER()
        # login
        self._LOGIN(driver,wait)
        # create empty DataFrame to hold data
        data            =   pd.DataFrame()
        # go through all three sections in the details section
        for i in np.arange(1,4):
            sec_xpath       =   self._xpath['details'] + '/dl[%s]/' % i
            # find the number of entries in section
            nEntries        =   len(driver.find_elements_by_xpath(sec_xpath + 'dt'))
            # go through each entry in the section
            for j in np.arange(1,nEntries+1):
                # get the xpaths to the name and value of entry
                name_xpath              =   sec_xpath + 'dt[%s]' % j
                value_xpath             =   sec_xpath + 'dd[%s]' % j
                # throw the temporary name and value xpaths into instance's _xpath
                self._xpath['name']     =   name_xpath
                self._xpath['value']    =   value_xpath
                # grab the values
                name                    =   self._GRAB_ELEMENT(driver,wait,'name').get_attribute("innerText")
                value                   =   self._GRAB_ELEMENT(driver,wait,'value').get_attribute("innerText")
                # collect entry results into dictionary
                entry                   =   dict(name=name, value=value)
                # make entry dictionary into Series
                entry                   =   pd.Series(entry)
                # append entry to data
                data                    =   data.append(entry, ignore_index=True)
        # close browser
        driver.close()
        return data

    def _FORMAT_DATA(self,data):
        data.name   =   data.name.str.replace(":","")
        data.name   =   data.name.str.replace("*","")
        data.value  =   data.value.str.replace(" \r\n",", ")
        data.value  =   data.value.str.replace("AZ","AZ,")
        data        =   self._STRING_2_FLOAT_FORMATS(data,["value"])
        return data

    #===============================================================================================
    # methods used in LOAN
    #===============================================================================================

    def GET_LOAN_META(self):
        data                =   self.meta.copy()
        meta                =   []
        results             =   {}
        results["loan"]     =   "Carrington"
        mapDict             =   dict(balance="Unpaid Principal Balance", APR="Current Interest Rate", dueDay="Next Payment Due", originalBalance="Original Loan Amount", startDate="First Payment Date")
        for key in mapDict:
            results[key]        =   data[data.name==mapDict[key]].value.values[0]
        results['dueDay']   =   pd.to_datetime(results['dueDay']).day
        results['nPer']     =   360
        meta.append(results)
        return meta
