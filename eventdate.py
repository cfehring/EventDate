# This python script displays and saves the event date for a program currently airing on any of the seven Pac-12 networks.  

# The script requires at least one attribute to be passed upon execution.  
# Enter the first letter of the network desired after the script name as shown in the following example for Washington.
# python eventdate.py w

# Multiple letters can also be entered, separated by spaces
# python eventdate.py n a b l m o w

# The script uses the Pac-12 EPG API to find what is currently airing on the network(s) requested.  
# If there is an event currently airing, the date of the original event will be pulled from Pac-12 events API and returned.
# The date will also be written to a text file in the directory of execution.  
# One file will be written for each network.  These files will be overwritten if they already exist.

import requests #Digital recommends the request lib to interact w/ apis over http. http://docs.python-requests.org/
from dateutil.parser import * # for parse() method to convert datetime format
import pytz # to convert to pacific time
import sys # for sys.argv to pass arguments from command line 

# initialize static variables for urls
epg_url = 'http://api.pac-12.com/v2/epg' #production server
event_url = 'http://api.pac-12.com/v2/events'  #production server

#Get arguments from python command line and iterate through the networks
for i in range(len(sys.argv)):
    if i == 0:
        None # Don't need to do anything with the name of the script, just the arguments

    else:
        net = "%s" % (sys.argv[i])
    
        if net == 'n':            
            networks = 88 #Pac-12 Networks
            file = "p12nat.txt"
        elif net == 'b':
            networks = 86 #Pac-12 Bay Area
            file = "p12bay.txt"
        elif net == 'a':
            networks = 91 #Pac-12 Arizona
            file = "p12arz.txt"
        elif net == 'l':
            networks = 92 #Pac-12 Los Angeles
            file = "p12lax.txt"
        elif net == 'm':
            networks = 87 #Pac-12 Mountain
            file = "p12mtn.txt"
        elif net == 'o':
            networks = 89 #Pac-12 Oregon
            file = "p12org.txt"
        elif net == 'w':
            networks = 90 #Pac-12 Washington
            file = "p12was.txt"
        
        else:
            print "enter the first letter of each network after the script name as shown in the following examples"
            print "python eventdate.py n a b l m o w"
            print "python eventdate.py n"
            print "python eventdate.py b l"
            sys.exit()

        print file # indicate which file the date will be written to
        
        # limit results to just the next event
        pagesize = 1

        # request to p12 api for EPG data
        epg_get_params = {'pagesize': pagesize , 'networks': networks}
        epg_get_request  = requests.get(epg_url, params=epg_get_params)
        epg_get_response = epg_get_request.json()
      
        # Pull out the event_id from the epg api to pass to the events api
        event_id = epg_get_response['programs'][0]['event_id'] 
        
        # When there isn't an event on the network, event_id returns "None"
        if event_id is None:
            my_date = "-"  #this dash will be written to the file if there isn't an event on now
            
        else:
            # Use the event_id to get all data about the event
            event_get_request  = requests.get(event_url+"/"+event_id)
            event_get_response = event_get_request.json()
            
            # Pull out the value of the start_time key, which indicates the original air date
            start_time = event_get_response['event_date']['start_time']
            
            # parse date to change format
            parsed_time_zulu = parse(start_time)
            
            # convert zulu to Pacific time
            tz_pacific = pytz.timezone('US/Pacific')
            time_pacific = parsed_time_zulu.astimezone(tz_pacific)

            # format date, disregard time
            format = '%b %d, %Y'  #Format date as Jan 01, 2014
            my_date = time_pacific.strftime(format) 
                
        # print the date of the original broadcast
        print my_date
        print ""
        
        # write the date of the original broadcast to a file (for each network requested by attribute)
        f = open (file, "w")   
        f.write (my_date)
        f.close ()  
        