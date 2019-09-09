#!/usr/bin/python
#-*- coding:utf-8 -*-
import os
from argparse import ArgumentParser
from fordLogRetrieve import FordLogRetrieve

def main(outputDir, fordLogFiles):
	fordLogRetrieve = FordLogRetrieve()
	for fordLogFile in fordLogFiles:
		fordLogRetrieve.setFordLog(fordLogFile)
		fordLogRetrieve.setOutputDir(outputDir)
		fordLogRetrieve.retrieveLog()


def getFileList( p ):
    """ get file name that in dictory. """
    p = str( p )
    if p=="":
        return [ ]
    p = p.replace( "/","\\")
    if p[ -1] != "\\":
        p = p+"\\"
    a = os.listdir( p )
    b = [ x   for x in a if os.path.isfile( p + x ) ]
    return b


if __name__ == "__main__":
	arg_parser = ArgumentParser(prog="python retrieve.py", description="ford log retrieve.")
	arg_parser.add_argument('log_files', nargs = '*', help = "ford log files")
	arg_parser.add_argument('--dir', help="output directory")
	args = arg_parser.parse_args()

	fordLogFiles = []
	if args.log_files:
		for f_p in args.log_files:
			if os.path.isdir(f_p):
				files = getFileList(f_p)
				for file in files:
					fordLogFiles.append(f_p + file)
			else:
				fordLogFiles.append(f_p)

	if args.dir:
		outputDir = args.dir
	else:
		outputDir = os.curdir

	main(outputDir, fordLogFiles)
	pass