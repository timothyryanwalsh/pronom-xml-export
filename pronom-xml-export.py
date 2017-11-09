import urllib2
import os
import time
import ConfigParser

puid_type_list = ['x-fmt', 'fmt']

config = ConfigParser.RawConfigParser()
config.read('pronom-xml-export.cfg')

puid_dict = {}

for type in puid_type_list:
   tmpint = config.getint('puids', type)
   if tmpint > 0:
      puid_dict[type] = tmpint

error_string=config.get('doctypes', 'error-string')
good_string=config.get('doctypes', 'good-string')

#url through which to access Pronom data...
base_url=config.get('urls', 'base-url')

def export_data():

   proxy = ''
   
   #comment this to remove proxy requirement
   #proxy = urllib2.ProxyHandler({'http': 'dummy@host:port'})

   for puid_type in puid_dict.keys():
      puid_type_url = base_url + puid_type + '/'
      current_dir = os.getcwd()
      new_dir = os.getcwd() + '//' + config.get('locations', 'export') + '//' + puid_type + '//'
      
      try:
         os.makedirs(new_dir)
      except OSError as (errno, strerror):
         print "OS error({0}): {1}".format(errno, strerror)

      #change to expor directory to store xml...
      os.chdir(new_dir)
      
      #urlib code here...
      puid_no = puid_dict[puid_type]

      for i in range(1, puid_no + 1):
         filename = puid_type + str(i) + '.xml'
         puid_url = puid_type_url + str(i) + '.xml'
         
         request = urllib2.Request(puid_url)
         
         if proxy != '':
            opener = urllib2.build_opener(proxy)
         else:
            opener = urllib2.build_opener()
         
         request.add_header('User-Agent', 'bitarchivist-PRONOM-Export/0.0.0')
         
         print puid_url

         url = opener.open(request)
         
         test_string = url.read(14)
         
         if(check_record(test_string)):
            f = open(filename, 'wb')
            f.write(test_string + url.read())
            f.close()

      #revert back to original directory...
      os.chdir(current_dir)		


def check_record(test_string):
   return_val = 0;

   if test_string == error_string:
      return_val = 0
   elif test_string == good_string:
      return_val = 1
   else:
      #some other value discovered, do not allow...
      return_val = 0
      
   return return_val

#time script execution time roughly...
t0 = time.clock()

export_data()

#print script execution time...
print 'Execution time: ' + str(time.clock() - t0) + ' seconds.'
