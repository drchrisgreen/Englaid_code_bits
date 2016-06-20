# Script created by Dr Chris Green (christopher.green@arch.ox.ac.uk) as part of the EngLaID project: http://www.englaid.com

import csv		# CSV library used by script

# Python script for processing percentage (as a decimal between 0 and 1) probabilities of records.
# Requires two input tables in CSV format:
# infile = this is the input data; it should contain a header row with four specified fields called:
#   "id_field" - a field containing a unique ID code for each record
#   "quantity" - a field containing the quantity of objects (e.g. finds) for each record
#   "Min" - a field containing the minimum date for each record
#   "Max" - a field containing the maximum date for each record
# datefile = this defines the time-slices to be processed; it should contain a header row with two specified fields called:
#   "Min" - a field containing the minimum date for each time-slice
#   "Max" - a field containing the maximum date for each time-slice
# Also:
# outfile = location of CSV file to be created with the output from the script

def process(infile, datefile, outfile):
	
	f1 = open(infile, 'rU')		# opens the input data file
	f2 = open(datefile, 'rU')	# opens the time-slice data file
	f3 = open(outfile, 'wb')	# creates the output data file
	
	periods = csv.reader(f2)	# Processing time-slice table
	mins = []					# List to contain minimum values of time-slices
	maxs = []					# List to contain maximum values of time-slices
	min_pos = 0
	max_pos = 0
	rownum = 0
	for row in periods:
		if rownum == 0:			# processing first row...
			colnum = 0
			for col in row:
				if col == 'Min':		# discovers column containing Min values - edit to change name
					min_pos = colnum
				if col == 'Max':		# discovers column containing Max values - edit to change name
					max_pos = colnum
				colnum += 1
		else:					# processing all other rows...
			mins.append(row[min_pos])	# appends minimum value to List
			maxs.append(row[max_pos])	# appends maximum value to List
		rownum +=1
	f2.close()					# closes time-slice table
	
 	writer = csv.writer(f3)		# processing output table
	reader = csv.reader(f1)		# processing input table
	rownum = 0
	id_pos = 0
	quant_pos = 0
	min_pos = 0
	max_pos = 0
	for row in reader:
		if rownum == 0:			# processing first row...
			colnum = 0
			for col in row:
				if col == 'id_field':	# discovers column containing ID values - edit to change name
					id_pos = colnum
				if col == 'quantity':	# discovers column containing quantity values - edit to change name
					quant_pos = colnum
				if col == 'Min':		# discovers column containing Min values - edit to change name
					min_pos = colnum
				if col == 'Max':		# discovers column containing Max values - edit to change name
					max_pos = colnum
				colnum += 1
			outrow = ['id_field','quantity','Min','Max']	# creates output header row
			inum = 0
			for i in mins:				# adds time-slice names to header row
				bmin = str(i)
				bmax = str(maxs[inum])
				bracket = 'b'+bmin+'_'+bmax		# time-slice name is 'b' + the min value + '_' + the max value
				outrow.append(bracket)
				inum += 1
			writer.writerow(outrow)		# writes header row to output file
		else:					# processing all other rows...
			id_value = int(row[id_pos])		# obtains ID value
			quant = int(row[quant_pos])		# obtains quantity value
			try:
				datemin = float(row[min_pos])	# obtains record minimum date value
				datemax = float(row[max_pos])	# obtains record maximum date value
				outrow = [id_value,quant,datemin,datemax]	# creates output row
				daterange = float(datemax - datemin)	# calculates temporal range of record
				inum = 0
				for i in mins:		# for each time-slice...
					prob = -1.0		# defines initial probability as -1 (this will be output where a record contains broken dates)
					bracketmin = float(i)				# minimum value of time-slice
					bracketmax = float(maxs[inum])		# maximum value of time-slice
					bracketrange = float(bracketmax - bracketmin)	# calculates temporal range of time-slice
					if datemin == datemax:		# if the time-slice is of 0 length
						if datemin >= bracketmin and datemin <= bracketmax:
							prob = 1.0			# probability = 1 where date range exactly matches time-slice range (both 0 length)
						elif datemin < bracketmin:
							prob = 0.0			# probability = 0 where date is earlier than time-slice
						elif datemin > bracketmax:
							prob = 0.0			# probability = 0 where date is later than time-slice
						else:
							prob = -1.0			# probability remains as -1 where the dates are broken
					elif bracketmin <= datemin and bracketmax >= datemax:
						prob = 1.0				# probability = 1 where date falls entirely within time-slice
					elif bracketmin > datemax:
						prob = 0.0				# probability = 0 where date is later than time-slice
					elif bracketmax < datemin:
						prob = 0.0				# probability = 0 where date is earlier than time-slice
					elif bracketmin <= datemin and bracketmax < datemax:
						prob = (bracketmax - datemin) / daterange	# probability calculated as a % where date overlaps minimum of time-slice
					elif bracketmin > datemin and bracketmax >= datemax:
						prob = (datemax - bracketmin) / daterange	# probability calculated as a % where date overlaps maximum of time-slice
					elif bracketmin > datemin and bracketmax < datemax:
						prob = bracketrange / daterange				# probability calculated as a % where date overlaps all of time-slice
					else:
						prob = -1.0				# probability remains as -1 where the dates are broken
					prob = round(prob, 5)		# rounds the output probability to 5 decimal places
					outrow.append(prob)			# appends probability for time-slice to output row
					inum += 1
				writer.writerow(outrow)			# writes output row to output file
 			except ValueError:		# prints a message to screen for broken date entries
 				if str(row[min_pos]) != '' and str(row[max_pos]) != '':
					print 'Bad dates: ' + str(id_value) + ' - ' + str(row[min_pos]) + ', ' + str(row[max_pos])
		rownum += 1
		
	f1.close()		# closes input table
	f3.close()		# closes output table