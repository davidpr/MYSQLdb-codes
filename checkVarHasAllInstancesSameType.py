#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#Author: David Prat

import sys
import traceback
import os
import MySQLdb

def main(argv):

        db=MySQLdb.connect(host="1.1.1.1",user="root", passwd="root",db="My_DB_1")
        cursorDB  = db.cursor()
        cursorDB4 = db.cursor()
        table=argv[0]

	#Load table rows using MySQLdb driver
        try:
                sql= "SELECT * FROM   "+table+" WHERE 1 "
                cursorDB.execute(sql)
                db.commit()
		sql= "SELECT DISTINCT dtId FROM "+table+" WHERE 1 "
                cursorDB4.execute(sql)
                db.commit()
	
        except:
                print "an error occurred"
                traceback.print_exc(file=sys.stdout)
                db.rollback()

	#Load table rows using List Comprehension; only required fields are loaded
	rows = [{'dtId': row[1], 'iVal': row[2], 'tVal': row[3], 'fVal': row[4], 'dVal': row[5]} for row in cursorDB.fetchall()]

	#Dictionary with all the variables, (only one instance)
	dictIds = {}
	#Load table rows without specifying data fields
	dataIds = cursorDB4.fetchall()
	for val in dataIds:
		dictIds[val[0]]=[]

	#print "rowcount "+str(len(rows))
	#Create a dictionary with key:variable value:vector of number of ocurrences of each type
	types={}
	for val in dataIds:
		types[val[0]]=[0,0,0,0]

	#Fill the dictionary
        for row in rows:
		idData = row['dtId']
		iValue = row['iVal']
		tValue = row['tVal']
		fValue = row['fVal']
		dValue = row['dVal']

		if iValue!=None:
			dictIds[idData].append("i")
			types[idData][0]=types[idData][0] + 1
		if tValue!=None:
			dictIds[idData].append("t")
			types[idData][1]=types[idData][1] + 1
		if fValue!=None:
			dictIds[idData].append("f")
			types[idData][2]=types[idData][2] + 1
		if dValue!=None:
			dictIds[idData].append("d")
			types[idData][3]=types[idData][3] + 1

	#For each variable, there's only a need to check if there are instances of different type and check which one is more numerous
	#Although dicIds was filled, there's no need to use it for what the analysis needed
	for val in dataIds:
		val=val[0]
		#Check all possible pairs for that variable			
		if ( (types[val][0]!=0  and  ((types[val][1]!=0) or (types[val][2]!=0) or (types[val][3]!=0) ))   or	
		     (types[val][1]!=0  and  ((types[val][0]!=0) or (types[val][2]!=0) or (types[val][3]!=0) ))   or	
		     (types[val][2]!=0  and  ((types[val][0]!=0) or (types[val][1]!=0) or (types[val][3]!=0) ))   or	
		     (types[val][3]!=0  and  ((types[val][0]!=0) or (types[val][1]!=0) or (types[val][2]!=0) )) )  :	
			#Print the problematic case	
			print str(val)+" "+str(types[val])
		
main(sys.argv[1:])
