# Module to read in EH pdf data (from converted text file)

import csv

def ehconvert(file_in, file_out): # This is the module to be called
	eh_in = open(file_in, 'r') # This is the input file
	eh_out = csv.writer(open(file_out, 'wb'), delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL) # This is the (new) file we will write out to (which will be a csv table)
	processing = -1 # This is set to -1 to show that we aren't working through an entry to begin with
	header = ['HOBID','desc_long','Palaeolith','Mesolithic','Neolithic','EBA','BronzeAge','IronAge','Prehist','PrehOrRo','Roman','EarlyMed','Medieval','PostMed','Modern','Uncertain','Dates_Min','Dates_Max','url']
	eh_out.writerow(header)
	counter = 0
	
	# just here for a bug fix:
	peri_pos = -1
	type_pos = -1
	date_pos = -1
	c_pos = -1
	
	outrow = []
	hobid = ''
	desc = ''
	palaeo = ''
	meso = ''
	neo = ''
	eba = ''
	ba = ''
	ia = ''
	prehist = ''
	preOrRo = ''
	roman = ''
	early = ''
	medi = ''
	post = ''
	mod = ''
	uncertain = ''
	min_dates = ''
	max_dates = ''
	url = ''
	current = 0 # 1= palaeo, 2= meso, 3= neo, 14= eba, 4= ba, 5= ia, 6= pre, 7= prORro, 8= ro, 9= em, 10= med, 11= pm, 12= mod, 13 = un
	
	post_med_list = ['ELIZABETHAN','GEORGIAN','POSTMED','STUART','TUDOR','VICTORIAN','JACOBEAN','HANOVERIAN']
	post_med_abbrev = ['[ELZ] ','[GEO] ','[PM] ','[STU] ','[TUD] ','[VIC] ','[JAC] ','[HAN] ']
	modern_list = ['20TH CENTURY','21ST CENTURY','FIRST WORLD WAR','SECOND WORLD WAR','EDWARDIAN','20TH   CENTURY']
	modern_abbrev = ['[C20] ','[C21] ','[WW1] ','[WW2] ','[EDW] ','[C20] ']
	
	for line in eh_in: # We iterate through each line of the input file until we reach the end
		linestr = str(line) # Converts the current line to a string object
		linestr = linestr.rstrip()
		linelen = len(linestr) # Obtains the length of the line string
		if linelen > 0:
			tempstr = linestr[0] # Obtains the first character of the line string
		if linestr[0:10] == 'Identifier': # This spots the heading line at the top of each page...
			type_pos = linestr.find('Term') # ...and obtains the position of the Term heading
		elif linestr[0:11] == 'Description' and 'Parish or (NPA)' in linestr: # This spots the next heading line at the top of each page...
			peri_pos = linestr.find('Period') # ...and obtains the position of the Period heading
			date_pos = linestr.find('Dates') #...and the Dates heading
			c_pos = linestr.find('C') # ...and the C heading (i.e. end of desc lines)
		# If the first character of the line is a numeral, the line is a long line, and we are currently not processing an entry:
		elif tempstr.isdigit() == True and processing == -1 and linelen > peri_pos:
			processing = 1 # We are now processing the first line of a record
			pos = linestr.find(' ')
			hobid = linestr[:pos]
			period = linestr[peri_pos:date_pos].rstrip()
			if period == 'POST MEDIEVAL' or period == 'POST   MEDIEVAL':
				period = 'POSTMED'
			type = ''
			if 'PALAEOLITHIC' in period:
				current = 1
			elif 'MESOLITHIC' in period:
				current = 2
			elif 'NEOLITHIC' in period:
				current = 3
			elif 'BRONZE AGE' in period:
				if 'EARLY' in period:
					current = 14
				else:
					current = 4
			elif 'IRON AGE' in period:
				current = 5
			elif 'PREHISTORIC' in period and 'ROMAN' in period:
				current = 7
			elif 'PREHISTORIC' in period:
				current = 6
			elif 'ROMAN' in period:
				current = 8
			elif 'EARLY MED' in period:
				current = 9
			elif 'MEDIEVAL' in period:
				current = 10
			elif 'UNCERTAIN' in period:
				current = 13
			else:
				xnum = 0
				for x in post_med_list:
					if x in period:
						current = 11
						type += post_med_abbrev[xnum]
					xnum += 1
				xnum = 0
				for x in modern_list:
					if x in period:
						current = 12
						type += modern_abbrev[xnum]
					xnum += 1
			if current == 0:
				print 'ERROR: ' + period + ' ' + str(hobid)
			if 'EARLY' in period and current != 9 and current != 14:
				type += '[EARLY] '
			elif 'MIDDLE' in period:
				type += '[MIDDLE] '
			elif 'MID' in period:
				type += '[MID] '
			elif 'LATE' in period:
				type += '[LATE] '
			elif 'LATER' in period and current != 9:
				type += '[LATER] '
			elif 'LOWER' in period:
				type += '[LOWER] '
			elif 'UPPER' in period:
				type += '[UPPER] '
			elif current == 9 and 'LATER' in period:
				type += '[OR LATER] '
			dates = linestr[date_pos:type_pos].rstrip()
			found = 0
			if 'to' in dates:
				pos = dates.find('to')
				min_temp = dates[:pos].rstrip()
				pos += 2
				max_temp = dates[pos:].lstrip()
				found = 1
			elif 'Post' in dates:
				min_temp = dates[4:].lstrip()
				max_temp = 2012
				found = 1
			elif 'Pre' in dates:
				min_temp = -100000
				max_temp = dates[3:].lstrip()
				found = 1
			if found == 1:
				if len(min_dates) > 0:
					min_dates += '; ' + str(min_temp)
				else:
					min_dates = str(min_temp)
				if len(max_dates) > 0:
					max_dates += '; ' + str(max_temp)
				else:
					max_dates = str(max_temp)
			type += linestr[type_pos:]
			if current == 1:
				if len(palaeo) > 0:
					palaeo += '; ' + type
				else:
					palaeo = type
			elif current == 2:
				if len(meso) > 0:
					meso += '; ' + type
				else:
					meso = type
			elif current == 3:
				if len(neo) > 0:
					neo += '; ' + type
				else:
					neo = type
			elif current == 14:
				if len(eba) > 0:
					eba += '; ' + type
				else:
					eba = type
			elif current == 4:
				if len(ba) > 0:
					ba += '; ' + type
				else:
					ba = type
			elif current == 5:
				if len(ia) > 0:
					ia += '; ' + type
				else:
					ia = type
			elif current == 6:
				if len(prehist) > 0:
					prehist += '; ' + type
				else:
					prehist = type
			elif current == 7:
				if len(preOrRo) > 0:
					preOrRo += '; ' + type
				else:
					preOrRo = type
			elif current == 8:
				if len(roman) > 0:
					roman += '; ' + type
				else:
					roman = type
			elif current == 9:
				if len(early) > 0:
					early += '; ' + type
				else:
					early = type
			elif current == 10:
				if len(medi) > 0:
					medi += '; ' + type
				else:
					medi = type
			elif current == 11:
				if len(post) > 0:
					post += '; ' + type
				else:
					post = type
			elif current == 12:
				if len(mod) > 0:
					mod += '; ' + type
				else:
					mod = type
			elif current == 13:
				if len(uncertain) > 0:
					uncertain += '; ' + type
				else:
					uncertain = type
		# This spots a line of 1 character length, which will mark the end of our item entry, if processing:
		elif linelen < 2 and processing == 1:
			if len(palaeo) > 254 or len(meso) > 254 or len(neo) > 254 or len(eba) > 254 or len(ba) > 254 or len(ia) > 254 or len(prehist) > 254 or len(preOrRo) > 254 or len(roman) > 254 or len(early) > 254 or len(uncertain) > 254:
				print 'BLOB!!!! ' + str(hobid)
			url = 'http://www.pastscape.org.uk/hob.aspx?hob_id=' + hobid
			desc = desc.rstrip()
			outrow.append(hobid)
			outrow.append(desc)
			outrow.append(palaeo)
			outrow.append(meso)
			outrow.append(neo)
			outrow.append(eba)
			outrow.append(ba)
			outrow.append(ia)
			outrow.append(prehist)
			outrow.append(preOrRo)
			outrow.append(roman)
			outrow.append(early)
			outrow.append(medi)
			outrow.append(post)
			outrow.append(mod)
			outrow.append(uncertain)
			outrow.append(min_dates)
			outrow.append(max_dates)
			outrow.append(url)
			eh_out.writerow(outrow) # Write the output string to our output file
			processing = -1 # And record that we have stopped processing this record
			outrow = []
			hobid = ''
			desc = ''
			palaeo = ''
			meso = ''
			neo = ''
			eba = ''
			ba = ''
			ia = ''
			prehist = ''
			preOrRo = ''
			roman = ''
			early = ''
			medi = ''
			post = ''
			mod = ''
			uncertain = ''
			min_dates = ''
			max_dates = ''
			url = ''
			current = 0
		# This spots a line of a length likely to mean it contains useful data, if processing:
		elif linelen > peri_pos and processing == 1:
			if linestr[peri_pos] == " ": # If there is no period entry in the line, we assume it just has a term continuation
				if tempstr != ' ':
					tempstr2 = linestr[:c_pos].rstrip()
					desc += tempstr2 + '\n'
				type = linestr[type_pos:]
				if current == 1:
					if len(palaeo) > 0:
						palaeo += ' ' + type
					else:
						palaeo = type
				elif current == 2:
					if len(meso) > 0:
						meso += ' ' + type
					else:
						meso = type
				elif current == 3:
					if len(neo) > 0:
						neo += ' ' + type
					else:
						neo = type
				elif current == 14:
					if len(eba) > 0:
						eba += '; ' + type
					else:
						eba = type
				elif current == 4:
					if len(ba) > 0:
						ba += ' ' + type
					else:
						ba = type
				elif current == 5:
					if len(ia) > 0:
						ia += ' ' + type
					else:
						ia = type
				elif current == 6:
					if len(prehist) > 0:
						prehist += ' ' + type
					else:
						prehist = type
				elif current == 7:
					if len(preOrRo) > 0:
						preOrRo += ' ' + type
					else:
						preOrRo = type
				elif current == 8:
					if len(roman) > 0:
						roman += ' ' + type
					else:
						roman = type
				elif current == 9:
					if len(early) > 0:
						early += ' ' + type
					else:
						early = type
				elif current == 10:
					if len(medi) > 0:
						medi += ' ' + type
					else:
						medi = type
				elif current == 11:
					if len(post) > 0:
						post += ' ' + type
					else:
						post = type
				elif current == 12:
					if len(mod) > 0:
						mod += ' ' + type
					else:
						mod = type
				elif current == 13:
					if len(uncertain) > 0:
						uncertain += ' ' + type
					else:
						uncertain = type
			else: # Otherwise:
				if tempstr != ' ':
					if linelen > c_pos:
						tempstr2 = linestr[:c_pos].rstrip()
					else:
						tempstr2 = linestr
					desc += tempstr2 + '\n'
				period = linestr[peri_pos:date_pos].rstrip()
				if period == 'POST MEDIEVAL' or period == 'POST   MEDIEVAL':
					period = 'POSTMED'
				type = ''
				if 'PALAEOLITHIC' in period:
					current = 1
				elif 'MESOLITHIC' in period:
					current = 2
				elif 'NEOLITHIC' in period:
					current = 3
				elif 'BRONZE AGE' in period:
					if 'EARLY' in period:
						current = 14
					else:
						current = 4
				elif 'IRON AGE' in period:
					current = 5
				elif 'PREHISTORIC' in period and 'ROMAN' in period:
					current = 7
				elif 'PREHISTORIC' in period:
					current = 6
				elif 'ROMAN' in period:
					current = 8
				elif 'EARLY MED' in period:
					current = 9
				elif 'MEDIEVAL' in period:
					current = 10
				elif 'UNCERTAIN' in period:
					current = 13
				else:
					xnum = 0
					for x in post_med_list:
						if x in period:
							current = 11
							type += post_med_abbrev[xnum]
						xnum += 1
					xnum = 0
					for x in modern_list:
						if x in period:
							current = 12
							type += modern_abbrev[xnum]
						xnum += 1
				if current == 0:
					print 'ERROR: ' + period + ' ' + str(hobid)
				if 'EARLY' in period and current != 9 and current != 14:
					type += '[EARLY] '
				elif 'MIDDLE' in period:
					type += '[MIDDLE] '
				elif 'MID' in period:
					type += '[MID] '
				elif 'LATE' in period:
					type += '[LATE] '
				elif 'LATER' in period and current != 9:
					type += '[LATER] '
				elif 'LOWER' in period:
					type += '[LOWER] '
				elif 'UPPER' in period:
					type += '[UPPER] '
				elif current == 9 and 'LATER' in period:
					type += '[OR LATER] '
				dates = linestr[date_pos:type_pos].rstrip()
				found = 0
				if 'to' in dates:
					pos = dates.find('to')
					min_temp = dates[:pos].rstrip()
					pos += 2
					max_temp = dates[pos:].lstrip()
					found = 1
				elif 'Post' in dates:
					min_temp = dates[4:].lstrip()
					max_temp = 2012
					found = 1
				elif 'Pre' in dates:
					min_temp = -100000
					max_temp = dates[3:].lstrip()
					found = 1
				if found == 1:
					if len(min_dates) > 0:
						min_dates += '; ' + str(min_temp)
					else:
						min_dates = str(min_temp)
					if len(max_dates) > 0:
						max_dates += '; ' + str(max_temp)
					else:
						max_dates = str(max_temp)
				type += linestr[type_pos:]
				if current == 1:
					if len(palaeo) > 0:
						palaeo += '; ' + type
					else:
						palaeo = type
				elif current == 2:
					if len(meso) > 0:
						meso += '; ' + type
					else:
						meso = type
				elif current == 3:
					if len(neo) > 0:
						neo += '; ' + type
					else:
						neo = type
				elif current == 4:
					if len(ba) > 0:
						ba += '; ' + type
					else:
						ba = type
				elif current == 5:
					if len(ia) > 0:
						ia += '; ' + type
					else:
						ia = type
				elif current == 6:
					if len(prehist) > 0:
						prehist += '; ' + type
					else:
						prehist = type
				elif current == 7:
					if len(preOrRo) > 0:
						preOrRo += '; ' + type
					else:
						preOrRo = type
				elif current == 8:
					if len(roman) > 0:
						roman += '; ' + type
					else:
						roman = type
				elif current == 9:
					if len(early) > 0:
						early += '; ' + type
					else:
						early = type
				elif current == 10:
					if len(medi) > 0:
						medi += '; ' + type
					else:
						medi = type
				elif current == 11:
					if len(post) > 0:
						post += '; ' + type
					else:
						post = type
				elif current == 12:
					if len(mod) > 0:
						mod += '; ' + type
					else:
						mod = type
				elif current == 13:
					if len(uncertain) > 0:
						uncertain += '; ' + type
					else:
						uncertain = type
		elif linelen > 1 and processing == 1 and linelen < c_pos and tempstr != ' ':  # i.e. likely to be a description continuation
			tempstr2 = linestr
			desc += tempstr2 + '\n'
		elif linelen > 1 and processing == 1 and linelen < peri_pos and tempstr != ' ':  # i.e. likely to be a description continuation
			tempstr2 = linestr[:c_pos].rstrip()
			desc += tempstr2 + '\n'
		else: # i.e. ignore this line of the file as it's not of interest to us
			continue
	
	eh_in.close() # Close the input file