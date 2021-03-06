from __future__ import print_function
from pyspark import SparkContext
from csv import reader

import sys

import re
import datetime

class Point:
    def __init__(self,x,y):
        self.x = x
        self.y = y

#Function to check validity of complaint number x[0]
def is_valid_cmplnt_num(x):
    try:
    	if x is "" or x is " ":
    		return "NULL"
        #check using regular expression
    	elif re.match('[1-9][0-9]+$',x):
    		return "VALID"
    	else :
    		return "INVALID"
    except ValueError:
        return "INVALID"


if __name__ == "__main__":
	sc=SparkContext();
	data = sc.textFile(sys.argv[1], 1);
	data = data.mapPartitions(lambda x : reader(x));
	#extract header
	header = data.first();
	#removing the header
	data = data.filter(lambda x : x != header);
	#extract the required column
	col=data.map(lambda x : (x[0],x[0],is_valid_cmplnt_num(x[0])));
	#count "Valid" "Invalid" or "NULL"
	count=col.map(lambda x: (x[2],1)).reduceByKey(lambda x,y:x+y).collect();
	cnt=sc.parallelize(count);
	#output the specific column and the counts
	col.saveAsTextFile('NYPD_data_column0.out');
	cnt.saveAsTextFile('NYPD_count_column0.out');
