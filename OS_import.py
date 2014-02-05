# Import dependencies:
import csv

def convert(infile, outfile, ngr_name):
	f1 = open(infile, 'rU')
	f2 = open(outfile, 'wb')
	reader = csv.reader(f1)
	writer = csv.writer(f2)
	
	ngrpos = 0
	rownum = 0
	for row in reader:
		if rownum == 0:
			colnum = 0
			for col in row:
				if col == ngr_name:
					ngrpos = colnum
				colnum += 1
			header = row
			header.append('X')
			header.append('Y')
			header.append('precision')
			writer.writerow(header)
		else:
			ngr = row[ngrpos]
			result = ngrconvert(ngr)
			x = result[0]
			y = result[1]
			precision = result[2]
			if x != -1 and y != -1:
				list1 = row
				list1.append(x)
				list1.append(y)
				list1.append(precision)
				writer.writerow(list1)
		rownum += 1
		
	f1.close()
	f2.close()
		
def convert_split(infile, outfile):
	sqrpos = 1
	eastpos = 2
	northpos = 3
	
	f1 = open(infile, 'rU')
	f2 = open(outfile, 'wb')
	reader = csv.reader(f1)
	writer = csv.writer(f2)
	
	rownum = 0
	for row in reader:
		if rownum == 0:
			header = row
			header.append('X')
			header.append('Y')
			header.append('precision')
			writer.writerow(header)
		else:
			ngrsqr = str(row[sqrpos])
			easting = str(row[eastpos])
			northing = str(row[northpos])
			
			ngrstr = ''
			ngrstr += ngrsqr
			e_len = len(easting)
			n_len = len(northing)
			if e_len > n_len:
				diff = e_len - n_len
				inum = 0
				while inum < diff:
					northing = '0' + northing
					inum += 1
			elif n_len > e_len:
				diff = n_len - e_len
				inum = 0
				while inum < diff:
					easting = '0' + easting
					inum += 1
			ngrstr += easting + northing
			
			result = ngrconvert(ngrstr)
			x = result[0]
			y = result[1]
			precision = result[2]
			if x != -1 and y != -1:
				list1 = row
				list1.append(x)
				list1.append(y)
				list1.append(precision)
				writer.writerow(list1)	
		rownum += 1
	
	f1.close()
	f2.close()
			
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
	elif ngsqr == 'SR': # 	SR - 100000, 100000
		eastconv = 100000
		northconv = 100000
	# Scotland:
	elif ngsqr == 'NW':
		eastconv = 100000
		northconv = 500000
	elif ngsqr == 'NR':
		eastconv = 100000
		northconv = 600000
	elif ngsqr == 'NS':
		eastconv = 200000
		northconv = 600000
	elif ngsqr == 'NL':
		eastconv = 0
		northconv = 700000
	elif ngsqr == 'NM':
		eastconv = 100000
		northconv = 700000
	elif ngsqr == 'NN':
		eastconv = 200000
		northconv = 700000
	elif ngsqr == 'NO':
		eastconv = 300000
		northconv = 700000
	elif ngsqr == 'NF':
		eastconv = 0
		northconv = 800000
	elif ngsqr == 'NG':
		eastconv = 100000
		northconv = 800000
	elif ngsqr == 'NH':
		eastconv = 200000
		northconv = 800000
	elif ngsqr == 'NJ':
		eastconv = 300000
		northconv = 800000
	elif ngsqr == 'NK':
		eastconv = 400000
		northconv = 800000
	elif ngsqr == 'NA':
		eastconv = 0
		northconv = 900000
	elif ngsqr == 'NB':
		eastconv = 100000
		northconv = 900000
	elif ngsqr == 'NC':
		eastconv = 200000
		northconv = 900000
	elif ngsqr == 'ND':
		eastconv = 300000
		northconv = 900000
	elif ngsqr == 'NE':
		eastconv = 400000
		northconv = 900000
	elif ngsqr == 'HW':
		eastconv = 100000
		northconv = 1000000
	elif ngsqr == 'HX':
		eastconv = 200000
		northconv = 1000000
	elif ngsqr == 'HY':
		eastconv = 300000
		northconv = 1000000
	elif ngsqr == 'HZ':
		eastconv = 400000
		northconv = 1000000
	elif ngsqr == 'HU':
		eastconv = 300000
		northconv = 1100000
	elif ngsqr == 'HT':
		eastconv = 400000
		northconv = 1100000
	elif ngsqr == 'HP':
		eastconv = 400000
		northconv = 1200000
	else:
		print 'incorrect NGR sqr  ' + ngsqr  # Error if NGR letters are wrong
		eastconv = -1
		northconv = -1
	return eastconv, northconv