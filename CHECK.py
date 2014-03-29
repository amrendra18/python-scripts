"""
Author: Amrendra Kumar (theCodeGame)
Email: amrendra[DOT]nitb[AT]gmail[DOT]com

This python script is general checker used by various online judges
and often helpful for comparing two files locally

Usage: > CHECK.py input1.txt input2.txt

Example

File 1
_______________________
abcd efg    hij
klm
nop      rstuv
_______________________


File 2
_______________________
abcd
efg
    hij
        klm
nop
rstuv

_______________________

File 1 Matches with File 2

"""

import os
import sys
import re

#name of files
file1 = ""
file2 = ""

#content of files
str1 = ""
str2 = ""

def getNames():
    global file1,file2
    try:
        file1 = sys.argv[1]
        file2 = sys.argv[2]
    except:
        print "Usage: > CHECK.py input1.txt input2.txt"
        print "Programs needs two file names as 2 arguments. EXITING!!"
        exit(0)


def readFiles():
    global file1,file2
    global str1,str2
    try:
        f1 = open(file1,'r')
        str1 = f1.read()
    except:
        print "Couldnot read 1st file [%s] EXITING!!"%(file1)
        exit(0) 

    try:
        f2 = open(file2,'r')
        str2 = f2.read()
    except:
        print "Couldnot read 2nd file [%s] EXITING!!"%(file2)
        exit(0) 

    f1.close()
    f2.close()

def matchFiles():
    global str1,str2
    str2 = re.sub('\\s+', ' ', str2).strip()
    str1 = re.sub('\\s+', ' ', str1).strip()
    if str1==str2:
        print "[[ MATCH ]]"
    else:
        print "[[ DO NOT MATCH ]]"


if __name__ == '__main__':
    getNames()
    readFiles()
    matchFiles()
