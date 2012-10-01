import csv

def getdates(infile, outfile):
	
	xmlin = open (infile, 'r')
	csvout = csv.writer(open(outfile, 'wb'), delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
	
	header = ['MonUID','term','startdate','enddate']
	
	csvout.writerow(header)
	
	processing = 0
	for line in xmlin:
		if processing == 0 and '<xmlzEngLaID_MonType>' in line:
			processing = 1
			outlist = []
		elif processing == 0:
			continue
		elif '<xmlzEngLaID_Evidence>' in line:
			processing = 0
		elif '</xmlzEngLaID_MonType>' in line:
			if len(outlist) == 2:
				outlist.append('')
				outlist.append('')
			elif len(outlist) == 3:
				outlist.append('')
			csvout.writerow(outlist)
			outlist = []
		elif '<MonUID>' in line:
			pos1 = line.find('>') + 1
			pos2 = pos1 + line[pos1:].find('<')
			tempstr = line[pos1:pos2]
			outlist.append(tempstr)
		elif '<Term>' in line:
			pos1 = line.find('>') + 1
			pos2 = pos1 + line[pos1:].find('<')
			tempstr = line[pos1:pos2]
			outlist.append(tempstr)
		elif '<YearFrom>' in line:
			pos1 = line.find('>') + 1
			pos2 = pos1 + line[pos1:].find('<')
			tempstr = line[pos1:pos2]
			outlist.append(tempstr)
		elif '<YearTo>' in line:
			pos1 = line.find('>') + 1
			pos2 = pos1 + line[pos1:].find('<')
			tempstr = line[pos1:pos2]
			outlist.append(tempstr)