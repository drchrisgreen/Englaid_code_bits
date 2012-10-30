# This python script contains modules designed to process 'xls' spreadsheets (actually html) downloaded from the AIP:
# http://csweb.bournemouth.ac.uk/aip/aipintro.htm

# The process should be:
# 1. Download relevant spreadsheets from the AIP website and save to a folder with no other 'xls' files in it.
# 2. Run the convertFromXls module to convert the spreadsheets to csv format and add numeric coordinates.
#    (NB: the 'collate' attribute should either be a filename to collate results into one spreadsheet or 'N' to create an output spreadsheet for each input)
# 3. Run the checkForDupes module to remove duplicate entries and to create separate coordinate spreadsheet.
# 4. (OPTIONAL) Run the periodProcess module to try to minimise data loss when entering data into ArcGIS (needs adaptation for non-EngLaId).
# 5. Run the createMultipointShapefile module to create a shapefile from the coordinate spreadsheet (REQUIRES ARCGIS).
# 6. Join data table to shapefile in ArcGIS and export the result to a new shapefile.

# Note that this coordinate conversion part of this script only has conversion figures for OS grid squares covering England.

# Import dependencies:
import glob
import csv
import arcpy  # This script requires ArcPy, i.e. it must be run on a computer on which ArcGIS 10+ is installed
from arcpy import env

# This module converts all of the so-called 'xls' files in a specified directory into csv files (and adds numeric coordinates):
def convertFromXls(dir, type, collate):  # User must input directory and the file type.  Enter filename for collate to collate into one table or 'N' to not collate.
	searchstr = dir + '*.' + type
	if collate != 'N':
		writer = csv.writer(open(dir + collate + '.csv', 'wb'), delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
	fileno = 1
	for filename in glob.glob(searchstr):
		with open(filename, 'r') as f:
			if collate == 'N':
				outfilestr = filename[:-4] + '.csv'
				writer = csv.writer(open(outfilestr, 'wb'), delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
			headerrow = 0
			ngrpos = 0
			crossref = ''
			process_crossref = 0
			header = []
			currentrow = []
			for line in f:
				if '<tr bgcolor' in line:  # i.e. start of header
					header = []
					headerrow = 1
					counter = 1
				elif '<th><h6>' in line:  # i.e. a column title
					pos = 8
					pos2 = line.find('</h6></th>')
					header.append(line[pos:pos2])
					if 'NGR' in line:
						ngrpos = counter  # we need to save this value to create numeric coords later
					counter += 1
				elif headerrow == 1 and '</tr>' in line: # i.e. end of header, so write to file
					header.append('X')
					header.append('Y')
					if collate == 'N':
						writer.writerow(header)
					elif fileno == 1:
						writer.writerow(header)
					headerrow = 0
				elif headerrow == 0 and '<tr>' in line:  # i.e. we have reached a new data entry
					currentrow = []
					counter = 1
				elif headerrow == 0 and '</tr>' in line: # i.e. reached the end of a data entry, so write to file
					currentrow.append(xcoord)
					currentrow.append(ycoord)
					writer.writerow(currentrow)
				elif '<td>' in line: # i.e. an item of data within an entry
					if '<br>' in line: # The cross reference field runs over several lines, so requires special treatment
						process_crossref = 1
						pos = 4
						pos2 = line.find('<br>')
						crossref = line[pos:pos2]
					else:
						pos = 4
						pos2 = line.find('</td>')
						currententry = line[pos:pos2].rstrip()
						if '<i>' in currententry: # remove html codes for italics / bold
							pos = currententry.find('<i>')
							pos2 = pos + 3
							tempstr1 = currententry[:pos]
							tempstr2 = currententry[pos2:]
							currententry = tempstr1 + tempstr2
						if '<b>' in currententry: # remove html codes for italics / bold
							pos = currententry.find('<b>')
							pos2 = pos + 3
							tempstr1 = currententry[:pos]
							tempstr2 = currententry[pos2:]
							currententry = tempstr1 + tempstr2
						if '</i>' in currententry: # remove html codes for italics / bold
							pos = currententry.find('</i>')
							pos2 = pos + 4
							tempstr1 = currententry[:pos]
							tempstr2 = currententry[pos2:]
							currententry = tempstr1 + tempstr2
						if '</b>' in currententry: # remove html codes for italics / bold
							pos = currententry.find('</b>')
							pos2 = pos + 4
							tempstr1 = currententry[:pos]
							tempstr2 = currententry[pos2:]
							currententry = tempstr1 + tempstr2
						currentrow.append(currententry)
						if counter == ngrpos: # i.e. this is a coordinate line, so look up using ngrconvert module
							xcoord = ''
							ycoord = ''
							if ',' in currententry: # i.e. multiple grid refs for this entry
								pos2 = 0
								while pos != -1:
									pos = currententry[pos2:].find(',')
									if pos != -1:
										pos3 = pos2 + pos
										tempstr = currententry[pos2:pos3].lstrip()
										coords = ngrconvert(tempstr)
										if xcoord == '':
											xcoord = str(coords[0])
											ycoord = str(coords[1])
										else:
											xcoord += ',' + str(coords[0])
											ycoord += ',' + str(coords[1])
										pos2 = pos3 + 1
								tempstr = currententry[pos2:].lstrip()
								coords = ngrconvert(tempstr)
								if xcoord == '':
									xcoord = str(coords[0])
									ycoord = str(coords[1])
								else:
									xcoord += ',' + str(coords[0])
									ycoord += ',' + str(coords[1])
							else:
								coords = ngrconvert(currententry)
								xcoord = str(coords[0])
								ycoord = str(coords[1])
					counter += 1
				elif process_crossref == 1 and '<br>' in line: # i.e. this line is a part of the cross refs field
					line = line.lstrip()
					pos2 = line.find('<br>')
					crossref += '; ' + line[:pos2]
				elif process_crossref == 1 and '</td>' in line: # i.e. this line is the end of the cross refs field
					line = line.lstrip()
					pos2 = line.find('</td>')
					crossref += '; ' + line[:pos2]
					process_crossref = 0
					currentrow.append(crossref)
		fileno += 1
			
# Process to convert NGRS to numeric coordinates (called by module above):
def ngrconvert(ngrstr):
	ngrstr = ngrstr.lstrip().rstrip()  # This strips off any carriage returns etc. at start / end of item
	ngrstr = ''.join(ngrstr.split())  # This strips out whitespace
	ngrlen = len(ngrstr)  # The coordinates will be calculated according to their number of digits / letters
	ignoreitem = 0
	if ngrlen == 16:
		ngsqr = ngrstr[:2]
		precision = 1
		try:
			eaststub = int(ngrstr[2:9]) / 100  # i.e. I only want this to the nearest metre
			northstub = int(ngrstr[9:]) / 100  # i.e. I only want this to the nearest metre
		except ValueError:
			ignoreitem = 1
	elif ngrlen == 14:
		ngsqr = ngrstr[:2]
		precision = 1
		try:
			eaststub = int(ngrstr[2:8]) / 10  # i.e. I only want this to the nearest metre
			northstub = int(ngrstr[8:]) / 10  # i.e. I only want this to the nearest metre
		except ValueError:
			ignoreitem = 1
	elif ngrlen == 12:
		ngsqr = ngrstr[:2]
		precision = 1
		try:
			eaststub = int(ngrstr[2:7])
			northstub = int(ngrstr[7:])
		except ValueError:
			ignoreitem = 1
	elif ngrlen == 10:
		ngsqr = ngrstr[:2]
		precision = 10
		try:
			eaststub = int(ngrstr[2:6]) * precision
			northstub = int(ngrstr[6:]) * precision
		except ValueError:
			ignoreitem = 1
	elif ngrlen == 8:
		ngsqr = ngrstr[:2]
		precision = 100
		try:
			eaststub = int(ngrstr[2:5]) * precision
			northstub = int(ngrstr[5:]) * precision
		except ValueError:
			ignoreitem = 1
	elif ngrlen == 6:
		ngsqr = ngrstr[:2]
		precision = 1000
		try:
			eaststub = int(ngrstr[2:4]) * precision
			northstub = int(ngrstr[4:]) * precision
		except ValueError:
			ignoreitem = 1
	elif ngrlen == 4:
		ngsqr = ngrstr[:2]
		precision = 10000
		try:
			eaststub = int(ngrstr[2:3]) * precision
			northstub = int(ngrstr[3:]) * precision
		except ValueError:
			ignoreitem = 1
	elif ngrlen == 2:
		ngsqr = ngrstr
		precision = 100000
		eaststub = 0
		northstub = 0
	else:
		print 'incorrect NGR  ' + str(ngrlen) + '    ' + ngrstr  # print a warning if the NGR is incorrectly formatted
		ignoreitem = 1
		eaststub = ''
		northstub = ''
	if ignoreitem != 1:
		ngsqr = ngsqr.upper()
		convs = ngrsqrlookup(ngsqr)  # Calls function to look up conversion figures for NGR tile
		eastconv = convs[0]
		northconv = convs[1]
		if eastconv == -1 or northconv == -1:
			ignoreitem = 1
		else:
			east = eaststub + eastconv
			north = northstub + northconv
			actualprecision = testprecision(east, north, precision)  # This calls the precision testing function, but I'm not actually using the result
	if ignoreitem == 1:
		#  Records with bad NGRs are given coords of -1, -1
		east = -1
		north = -1
		precision = -1
		actualprecision = -1
	return east, north, precision, actualprecision  # I'm not using the precision measures for now, but calculating them anyway in case needed later

# Function to test precision (called by module above):
def testprecision(incoming1, incoming2, precision):
	# This process tests the easting and northing figures against their apparent precision
	# as based upon the number of digits in the NGR.  The input variables are the easting,
	# the northing and the apparent precision.  The process iterates through base 10 orders
	# of magnitude until it finds an incompatible figure (i.e. a digit other than 0).  It
	# repeats this for both x and y and then outputs the true precision of the NGR, based
	# upon the most precise of x and y. 
	
	tester = precision
	outgoing = 0
	while outgoing != tester:
		tester = tester * 10
		test = int(incoming1 / tester) * tester
		if test < incoming1:
			outgoing = tester
	outgoing = outgoing / 10
	
	tester = precision
	outgoing2 = 0
	while outgoing2 != tester:
		tester = tester * 10
		test = int(incoming2 / tester) * tester
		if test < incoming2:
			outgoing2 = tester
	outgoing2 = outgoing2 / 10
	
	if outgoing2 < outgoing:
		outgoing = outgoing2
	
	return outgoing

# Function listing conversion figures for each NGR square (ENGLAND ONLY!) (called by module further above):
def ngrsqrlookup(ngsqr):
	if ngsqr == 'NT': #		NT - 300000, 600000
		eastconv = 300000
		northconv = 600000
	elif ngsqr == 'NU': # 	NU - 400000, 600000
		eastconv = 400000
		northconv = 600000
	elif ngsqr == 'NX': # 	NX - 200000, 500000
		eastconv = 200000
		northconv = 500000
	elif ngsqr == 'NY': # 	NY - 300000, 500000
		eastconv = 300000
		northconv = 500000
	elif ngsqr == 'NZ': # 	NZ - 400000, 500000
		eastconv = 400000
		northconv = 500000
	elif ngsqr == 'OV': # 	OV - 500000, 500000
		eastconv = 500000
		northconv = 500000
	elif ngsqr == 'SC': # 	SC - 200000, 400000
		eastconv = 200000
		northconv = 400000
	elif ngsqr == 'SD': # 	SD - 300000, 400000
		eastconv = 300000
		northconv = 400000
	elif ngsqr == 'SE': # 	SE - 400000, 400000
		eastconv = 400000
		northconv = 400000
	elif ngsqr == 'SJ': # 	SJ - 300000, 300000
		eastconv = 300000
		northconv = 300000
	elif ngsqr == 'SK': # 	SK - 400000, 300000
		eastconv = 400000
		northconv = 300000
	elif ngsqr == 'SO': # 	SO - 300000, 200000
		eastconv = 300000
		northconv = 200000
	elif ngsqr == 'SP': # 	SP - 400000, 200000
		eastconv = 400000
		northconv = 200000
	elif ngsqr == 'SS': # 	SS - 200000, 100000
		eastconv = 200000
		northconv = 100000
	elif ngsqr == 'ST': # 	ST - 300000, 100000
		eastconv = 300000
		northconv = 100000
	elif ngsqr == 'SU': # 	SU - 400000, 100000
		eastconv = 400000
		northconv = 100000
	elif ngsqr == 'SV': # 	SV - 0, 0
		eastconv = 0
		northconv = 0
	elif ngsqr == 'SW': # 	SW - 100000, 0
		eastconv = 100000
		northconv = 0
	elif ngsqr == 'SX': # 	SX - 200000, 0
		eastconv = 200000
		northconv = 0
	elif ngsqr == 'SY': # 	SY - 300000, 0
		eastconv = 300000
		northconv = 0
	elif ngsqr == 'SZ': # 	SZ - 400000, 0
		eastconv = 400000
		northconv = 0
	elif ngsqr == 'TA': # 	TA - 500000, 400000
		eastconv = 500000
		northconv = 400000
	elif ngsqr == 'TF': # 	TF - 500000, 300000
		eastconv = 500000
		northconv = 300000
	elif ngsqr == 'TG': # 	TG - 600000, 300000
		eastconv = 600000
		northconv = 300000
	elif ngsqr == 'TL': # 	TL - 500000, 200000
		eastconv = 500000
		northconv = 200000
	elif ngsqr == 'TM': # 	TM - 600000, 200000
		eastconv = 600000
		northconv = 200000
	elif ngsqr == 'TQ': # 	TQ - 500000, 100000
		eastconv = 500000
		northconv = 100000
	elif ngsqr == 'TR': # 	TR - 600000, 100000
		eastconv = 600000
		northconv = 100000
	elif ngsqr == 'TV': # 	TV - 500000, 0
		eastconv = 500000
		northconv = 0
	# Wales:
	elif ngsqr == 'SC': # 	SC - 200000, 400000
		eastconv = 200000
		northconv = 400000
	elif ngsqr == 'SH': # 	SH - 200000, 300000
		eastconv = 200000
		northconv = 300000
	elif ngsqr == 'SM': # 	SM - 100000, 200000
		eastconv = 100000
		northconv = 200000
	elif ngsqr == 'SN': # 	SN - 200000, 200000
		eastconv = 200000
		northconv = 200000
	# Scotland:
	
	else:
		print 'incorrect NGR sqr  ' + ngsqr  # Error if NGR letters are wrong
		eastconv = -1
		northconv = -1
	return eastconv, northconv

# This module checks for duplicate entries in the csv spreadsheet and adds a unique ID code for each row;
# it also creates a second csv spreadsheet just containing the ID code and the numeric coordinates
# (ID and second spreadsheet needed for later modules):
def checkForDupes(infile, outfile, outfile2): # infile is the input csv file, outfile1 is the main spreadsheet and outfile2 is the coords spreadsheet
	reader = csv.reader(open(infile, 'rb'), delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
	writer = csv.writer(open(outfile, 'wb'), delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
	writer2 = csv.writer(open(outfile2, 'wb'), delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
	
	counter = 0
	idlist = []
	rowstr = ''
	for row in reader:
		rowstr = str(row)
		if rowstr not in idlist:
			idlist.append(rowstr)
			outrow = row
			cgr_code = 'CGr_' + str(counter)
			if cgr_code == 'CGr_0':
				cgr_code = 'CGr_ID'
			outrow.insert(0,cgr_code)
			writer.writerow(outrow)
			outrow2 = [cgr_code,row[14],row[15]]
			writer2.writerow(outrow2)
			counter += 1

# This module processes the main csv spreadsheet to cut down the description field to less than 254 characters
# due to restrictions for shapefiles.  It also separates out the monument types to several new fields: pre-EngLaId,
# undefined prehistoric, Bronze Age, Iron Age, Roman, early medieval, post-EngLaId, and other.  Obviously, these
# categories would need redefining for use by other projects!
def periodProcess(infile, outfile): # infile is the input csv file and outfile is the output csv file
	reader = csv.reader(open(infile, 'rb'), delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
	writer = csv.writer(open(outfile, 'wb'), delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
	
	rownum = 0
	descpos = 0
	typepos = 0
	idpos = 0
	current = 0
	tempcur = 0
	for row in reader:
		if rownum == 0:
			colnum = 0
			for col in row:
				if col == 'CGr_ID':  # note the column of the ID code
					idpos = colnum
				if col == 'Summary': # note the column of the summary field
					descpos = colnum
				if col == 'Monuments': # note the column of the monument type field
					typepos = colnum
				colnum += 1
			outrow = row
			# Append our new fields:
			outrow.append('Desc_short') # the shortened description field
			outrow.append('Pre_ELI') # monument types that are pre-Bronze Age
			outrow.append('Prehist') # monument types that are undefined prehistoric
			outrow.append('BronzeAge') # monument types that are Bronze Age
			outrow.append('IronAge') # monument types that are Iron Age
			outrow.append('Roman') # monument types that are Roman
			outrow.append('EarlyMed') # monument types that are early medieval
			outrow.append('Post_ELI') # monument types that are medieval or later
			outrow.append('Other') # monument types that do not fit above (i.e. mostly undated)
			writer.writerow(outrow)
		else:
			id_no = row[idpos]
			descin = row[descpos]
			typein = row[typepos]
			if len(descin) > 254:
				descout = '**BLOB**  ' + descin[:243]  # Curtails the description to less than 254 chars and marks with BLOB
			else:
				descout = descin
			preelid = ''
			prehist = ''
			bronze = ''
			iron = ''
			roman = ''
			earlymed = ''
			postelid = ''
			other = ''
			if len(typein) > 0: # i.e. many entries have no type
				pre_list = []
				pr_list = []
				ba_list = []
				ia_list = []
				ro_list = []
				em_list = []
				post_list = []
				other_list = []
				finished = 0
				fintemp = 0
				pos2 = typein.find(',')
				while finished == 0:
					if pos2 != -1:
						pos3 = pos2 + 1
						pos4 = typein[pos3:].find(',')
						if pos4 == -1:
							pos5 = len(typein)
							fintemp = 1
						else:
							pos5 = pos3 + pos4
						montype = typein[:pos2].translate(None, '[]()').upper()  # removes any brackets and sets to upper case for consistency
						period = typein[pos3:pos5].translate(None, '[]()')
						if period == '' and fintemp == 1:  # this captures the case where the end of the line is reached without encountering a period term
							period = 'undated'
						tester = 0
						temp = ' ' + period.lower() + ' '  # adds spaces before and after period so that abbreviations are caught only where they exist as a whole word
						# the terms searched for seem to be all of the period terms used by the AIP, but may need adding to if others exist:
						period_set = set(['undated', 'palaeolithic', 'mesolithic', 'neolithic', 'prehistoric', 'bronze age', 'iron age', 'roman', 'medieval', 'modern', ' ud ', ' pa ', ' me ', ' ne ', ' pr ', ' ba ', ' ia ', ' ro ', ' em ', ' me ', ' pm ', ' md ', ' mo ', ' ene ', ' lne ', ' eba ', ' mba ', ' lba ', ' eia ', ' mia ', ' lia '])
						for i in period_set:
							if i in temp:
								tester = 1
						if tester == 0: # i.e. no period term encountered yet in the current entry...
							while tester == 0: # ...so keep looking for one!
								# The module can sometimes get stuck in this loop if data is formatted unusually, so be careful!
								pos2 = pos5
								pos3 = pos5 + 1
								pos3 = pos2 + 1
								pos4 = typein[pos3:].find(',')
								if pos4 == -1:
									pos5 = len(typein)
									fintemp = 1
								else:
									pos5 = pos3 + pos4
								montype = typein[:pos2].translate(None, '[]()').upper() # removes any brackets and sets to upper case for consistency
								period = typein[pos3:pos5].translate(None, '[]()')
								temp = ' ' + period.lower() + ' '
								for i in period_set:
									if i in temp:
										tester = 1
									elif fintemp == 1:
										tester = 1
										temp = 'undated'
						period = temp
						if 'palaeolithic' in period or 'mesolithic' in period or 'neolithic' in period or ' pa ' in period or ' me ' in period or ' ne ' in period or ' ene ' in period or ' lne ' in period:
							pos = montype.find(',')
							if pos == -1:
								pre_list.append(montype)
							else:
								found = 0
								while found == 0:
									if pos == -1:
										pos = len(montype)
										found = 1
									pre_list.append(montype[:pos])
									pos = pos + 1
									montype = montype[pos:].lstrip()
									pos = montype.find(',')
						elif 'prehistoric' in period or ' pr ' in period:
							pos = montype.find(',')
							if pos == -1:
								pr_list.append(montype)
							else:
								found = 0
								while found == 0:
									if pos == -1:
										pos = len(montype)
										found = 1
									pr_list.append(montype[:pos])
									pos = pos + 1
									montype = montype[pos:].lstrip()
									pos = montype.find(',')
						elif 'bronze age' in period or ' ba ' in period or ' eba ' in period or ' mba ' in period or ' lba ' in period:
							pos = montype.find(',')
							if pos == -1:
								ba_list.append(montype)
							else:
								found = 0
								while found == 0:
									if pos == -1:
										pos = len(montype)
										found = 1
									ba_list.append(montype[:pos])
									pos = pos + 1
									montype = montype[pos:]
									pos = montype.find(',')
						elif 'iron age' in period or ' ia ' in period or ' eia ' in period or ' mia ' in period or ' lia ' in period:
							pos = montype.find(',')
							if pos == -1:
								ia_list.append(montype)
							else:
								found = 0
								while found == 0:
									if pos == -1:
										pos = len(montype)
										found = 1
									ia_list.append(montype[:pos])
									pos = pos + 1
									montype = montype[pos:].lstrip()
									pos = montype.find(',')
						elif 'roman' in period or ' ro ' in period:
							pos = montype.find(',')
							if pos == -1:
								ro_list.append(montype)
							else:
								found = 0
								while found == 0:
									if pos == -1:
										pos = len(montype)
										found = 1
									ro_list.append(montype[:pos])
									pos = pos + 1
									montype = montype[pos:].lstrip()
									pos = montype.find(',')
						elif 'early med' in period or ' em ' in period:
							pos = montype.find(',')
							if pos == -1:
								em_list.append(montype)
							else:
								found = 0
								while found == 0:
									if pos == -1:
										pos = len(montype)
										found = 1
									em_list.append(montype[:pos])
									pos = pos + 1
									montype = montype[pos:].lstrip()
									pos = montype.find(',')
						elif 'medieval' in period or 'modern' in period or ' me ' in period or ' md ' in period or ' mo ' in period or ' pm ' in period:  # E Med already filtered out and Med catches post-med too...
							pos = montype.find(',')
							if pos == -1:
								post_list.append(montype)
							else:
								found = 0
								while found == 0:
									if pos == -1:
										pos = len(montype)
										found = 1
									post_list.append(montype[:pos])
									pos = pos + 1
									montype = montype[pos:].lstrip()
									pos = montype.find(',')
						else:
							pos = montype.find(',')
							if pos == -1:
								other_list.append(montype)
							else:
								found = 0
								while found == 0:
									if pos == -1:
										pos = len(montype)
										found = 1
									other_list.append(montype[:pos])
									pos = pos + 1
									montype = montype[pos:].lstrip()
									pos = montype.find(',')
						pos5 += 1
						typein = typein[pos5:]
						pos2 = typein.find(',')
						if pos2 <= 0:
							finished = 1
						if fintemp == 1:
							finished = 1
				# we then create sets of each type list to remove duplicates, then convert back to list to sort
				tempset = set(pre_list)
				pre_list = list(tempset)
				pre_list.sort()
				tempset = set(pr_list)
				pr_list = list(tempset)
				pr_list.sort()
				tempset = set(ba_list)
				ba_list = list(tempset)
				ba_list.sort()
				tempset = set(ia_list)
				ia_list = list(tempset)
				ia_list.sort()
				tempset = set(ro_list)
				ro_list = list(tempset)
				ro_list.sort()
				tempset = set(em_list)
				em_list = list(tempset)
				em_list.sort()
				tempset = set(post_list)
				post_list = list(tempset)
				post_list.sort()
				tempset = set(other_list)
				other_list = list(tempset)
				other_list.sort()
				# we then pop out the entries for each list and write to a string
				if len(pre_list) > 0:
					while len(pre_list) > 0:
						tempstr = pre_list.pop(0)
						if preelid == '':
							preelid = tempstr
						else:
							preelid += '; ' + tempstr
				if len(pr_list) > 0:
					while len(pr_list) > 0:
						tempstr = pr_list.pop(0)
						if prehist == '':
							prehist = tempstr
						else:
							prehist += '; ' + tempstr
				if len(ba_list) > 0:
					while len(ba_list) > 0:
						tempstr = ba_list.pop(0)
						if bronze == '':
							bronze = tempstr
						else:
							bronze += '; ' + tempstr
				if len(ia_list) > 0:
					while len(ia_list) > 0:
						tempstr = ia_list.pop(0)
						if iron == '':
							iron = tempstr
						else:
							iron += '; ' + tempstr
				if len(ro_list) > 0:
					while len(ro_list) > 0:
						tempstr = ro_list.pop(0)
						if roman == '':
							roman = tempstr
						else:
							roman += '; ' + tempstr
				if len(em_list) > 0:
					while len(em_list) > 0:
						tempstr = em_list.pop(0)
						if earlymed == '':
							earlymed = tempstr
						else:
							earlymed += '; ' + tempstr
				if len(post_list) > 0:
					while len(post_list) > 0:
						tempstr = post_list.pop(0)
						if postelid == '':
							postelid = tempstr
						else:
							postelid += '; ' + tempstr
				if len(other_list) > 0:
					while len(other_list) > 0:
						tempstr = other_list.pop(0)
						if other == '':
							other = tempstr
						else:
							other += '; ' + tempstr
				# any entries over 254 characters have to be cut off, but a warning is printed
				if len(preelid) > 254:
					preelid = '**BLOB**  ' + preelid[:243]
					print 'BLOB (preELI): ' + id_no
				if len(prehist) > 254:
					prehist = '**BLOB**  ' + prehist[:243]
					print 'BLOB (PR): ' + id_no
				if len(bronze) > 254:
					bronze = '**BLOB**  ' + bronze[:243]
					print 'BLOB (BA): ' + id_no
				if len(iron) > 254:
					iron = '**BLOB**  ' + iron[:243]
					print 'BLOB (IA): ' + id_no
				if len(roman) > 254:
					roman = '**BLOB**  ' + roman[:243]
					print 'BLOB (RO): ' + id_no
				if len(earlymed) > 254:
					earlymed = '**BLOB**  ' + earlymed[:243]
					print 'BLOB (EM): ' + id_no
				if len(postelid) > 254:
					postelid = '**BLOB**  ' + postelid[:243]
					print 'BLOB (postELI): ' + id_no
				if len(other) > 254:
					other = '**BLOB**  ' + other[:243]
					print 'BLOB (other): ' + id_no
			# we then add the data to our row and write it to the new file
			outrow = row
			outrow.append(descout)
			outrow.append(preelid)
			outrow.append(prehist)
			outrow.append(bronze)
			outrow.append(iron)
			outrow.append(roman)
			outrow.append(earlymed)
			outrow.append(postelid)
			outrow.append(other)
			writer.writerow(outrow)
		rownum += 1
		if rownum / 1000 > current:  # this prints a count every 1000 records to show the process is working still...
			current = rownum / 1000
			print rownum
			
# This is the module that creates a shapefile (multipoint) from the coordinates csv spreadsheet:
def createMultipointShapefile(file_path, in_file, out_file):

	reader = csv.reader(open(file_path + in_file, 'rb'), delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
	
	# Lists to collate out various fields, this is a selection of relevant / usable fields from our HER database
	id_list = []
	x_list = []
	y_list = []
	
	# Iterates through records object and populates field lists (which are naturally kept in the correct order)
	rownum = 0
	for row in reader:
		if rownum != 0:
			id_list.append(row[0])
			x_list.append(row[1])
			y_list.append(row[2])
		rownum += 1
		
	# Create shapefile (NB: YOU MAY NEED TO CHANGE LOCATION OF PROJECTION FILE IF IT IS NOT AT THE LOCATION MENTIONED BELOW)
	env.workspace = file_path  # Workspace location
	out_path = file_path # Output path
	out_name = out_file + '.shp' # Output extension
	geometry_type = 'MULTIPOINT'  # The type is Multipoint, as some entries have multiple grid refs
	spatial_reference = arcpy.SpatialReference('C:\Program Files\ArcGIS\Desktop10.0\Coordinate Systems\Projected Coordinate Systems\National Grids\Europe\British National Grid.prj')
	new_shp = arcpy.CreateFeatureclass_management(out_path, out_name, geometry_type, '', 'DISABLED', 'DISABLED', spatial_reference)
	
	# Add fields to shapefile (2nd argument is field name, 3rd is the data type):
	arcpy.AddField_management(new_shp,'CGr_id','TEXT')
	arcpy.AddField_management(new_shp,'xcoords','TEXT')
	arcpy.AddField_management(new_shp,'ycoords','TEXT')
	
	# Then populate fields (NB: we are removing any unicode encoding and any [ or ] or ' characters from each entry):
	rows = arcpy.InsertCursor(new_shp)
	newpoint = arcpy.Point()
	newarray = arcpy.Array()
	n = 0
	for i in id_list:
		row = rows.newRow()
		row.CGr_id = str(id_list[n])
		row.xcoords = str(x_list[n])
		row.ycoords = str(y_list[n])
		
		x_str = str(x_list[n])
		y_str = str(y_list[n])
		if x_str == '' or x_str == '0' or y_str == '0':
			print 'Oh noes, no grid ref in record (skipped!) : ' + str(id_list[n])  # Triggers if no coords, skips record
		else:
			test = x_str.find(',')  # Checks for commas to find records with multiple grid refs
			if test == -1:  # Single grid ref
				easting = x_str
				northing = y_str
				east_fl = float(easting)
				north_fl = float(northing)
				newpoint.X = east_fl
				newpoint.Y = north_fl
				newarray.add(newpoint)
			else:  # Multiple grid refs
				xpos = 0
				xpos2 = x_str.find(',')
				easting = x_str[xpos:xpos2]
				ypos = 0
				ypos2 = y_str.find(',')
				northing = y_str[ypos:ypos2]
				xpos2 += 1  # assumes , between each entry in the list
				ypos2 += 1
				east_fl = float(easting)
				north_fl = float(northing)
				newpoint.X = east_fl
				newpoint.Y = north_fl
				newarray.add(newpoint)
				if len(x_str) > xpos2:
					while len(x_str) > xpos2:
						xpos = xpos2
						xpos2 = xpos + x_str[xpos:].find(',')
						test = x_str[xpos:].find(',')
						if test == -1:
							xpos2 = len(x_str)
						easting = x_str[xpos:xpos2]
						ypos = ypos2
						ypos2 = ypos + y_str[ypos:].find(',')
						test = y_str[ypos:].find(',')
						if test == -1:
							ypos2 = len(y_str)
						northing = y_str[ypos:ypos2]
						xpos2 += 1
						ypos2 += 1
						east_fl = float(easting)
						north_fl = float(northing)
						newpoint.X = east_fl
						newpoint.Y = north_fl
						newarray.add(newpoint)
			newMultiPoint = arcpy.Multipoint(newarray)  # Creates Multipoint object from point array
			newarray.removeAll()  # Clears point array for next entry
			row.shape = newMultiPoint  # Sets the geometry of this row to the Multipoint object
			rows.insertRow(row) # And finally we add the new row to the shapefile inc. geometry and attributes...
		n += 1