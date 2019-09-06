#!/usr/bin/python
#-*- coding: utf-8 -*-
import os
import sys

class FordLogRetrieve:
	def __init__(self):
		self.m_logPath = ""
		self.m_navLogDir = ""
		self.m_map = {}
		self.dirName = ""

	
	def setFordLog(self, logPath):
		if os.path.exists(logPath):
			self.m_logPath = logPath
		else:
			print(logPath + "doesn't exists!")
			sys.exit(-1)


	def setOutputDir(self, dirName):
		if os.path.isdir(dirName):
			self.dirName = os.path.dirname(dirName)
		else:
			print(dirName + "isn't directory!")
			sys.exit(-2)

	def retrieveLog(self):
		isNewLine = False
		logPath = self.m_logPath
		fordLogLines = []
		tempLine = ""
		with open(logPath, "r") as fordLog:
			lines = fordLog.readlines()
			while "\n" in lines:
				lines.remove("\n")
			for line in lines:
				if "vendor.telenav" in line:
					if isNewLine:
						fordLogLines.append(tempLine)
						tempLine = ""
						tempLine += line
						isNewLine = False
					else:
						tempLine = ""
						tempLine += line
						isNewLine = True
				elif line[0] == '<':
					if isNewLine:
						fordLogLines.append(tempLine)
						isNewLine = False
					else:
						pass
				else:
					if isNewLine:
						tempLine += line
					else:
						pass

			if "vendor.telenav" in tempLine:
				fordLogLines.append(tempLine)
				tempLine = ""

		self.__filterPid(fordLogLines)
		self.__output()


	def __filterPid(self, fordLogLines):
		for line in fordLogLines:
			key = line.split(" ")[4]
			if self.m_map.has_key(key):
				self.m_map[key].append(line)
			else:
				self.m_map[key] = []
				self.m_map[key].append(line)


	def __output(self):
		oldDir = os.getcwd()
		newDir = os.path.normpath(self.dirName)
		os.chdir(newDir)
		subDir = os.path.basename(self.m_logPath).split(".")[0]
		if not os.path.isdir(subDir):
			os.mkdir(subDir)
		os.chdir(subDir)
		for key, value in self.m_map.items():
			filePath = "navigation-" + key + ".log"
			lines = []
			with open(filePath, "w") as navLogFile:
				for line in value:
					lines.append(line[line.index(" ", line.index("tid")) + 1 : ])
				navLogFile.writelines(lines)

		os.chdir(oldDir)



