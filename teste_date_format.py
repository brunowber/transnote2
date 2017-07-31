__author__ = 'vilmar'
from datetime import datetime

data = '03/11/2015 13:03:15'

data_format = datetime.strptime(data, '%d/%m/%Y %H:%M:%S')

print data_format
