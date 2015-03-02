import csv

def process():
	f1 = open('temp/sub_periods_conventional.csv','rU')
	mins = []
	maxs = []
	reader = csv.reader(f1)
	rownum = 0
	for row in reader:
		if rownum > 0:
			mins.append(float(row[0]))
			maxs.append(float(row[1]))
		rownum += 1
	f1.close()
	del reader
	mins = tuple(mins)
	maxs = tuple(maxs)
	
	print 'Periods set'
	
	f1 = open('temp/c14_dates_detailed.csv','rU')
	date_codes = set([])
	reader = csv.reader(f1)
	rownum = 0
	for row in reader:
		if rownum > 0:
			date_codes.add(str(row[0]))
		rownum += 1
	f1.close()
	del reader
	date_codes = list(date_codes)
	date_codes.sort()
	date_codes = tuple(date_codes)
	
	print 'Date codes loaded'
	
	probs = []
	r_len = len(date_codes)
	r = 0
	while r < r_len:
		temp_list = []
		b_len = len(mins)
		b = 0
		while b < b_len:
			temp_list.append(0.0)
			b += 1
		probs.append(temp_list)
		r += 1
		del temp_list
	del r_len
	del r
	
	print 'Lists populated'
	
	f1 = open('temp/c14_dates_detailed.csv','rU')
	reader = csv.reader(f1)
	rownum = 0
	for row in reader:
		if rownum > 0:
			date = str(row[0])
			pos = date_codes.index(date)
			cur_date = float(row[1])
			cur_prob = float(row[2]) * 5
			if cur_prob > 0:
				b = 0
				while b < b_len:
					min = mins[b]
					max = maxs[b]
					if cur_date >= min  and cur_date < max:
						probs[pos][b] += cur_prob
					b += 1
		rownum += 1
	f1.close()
	del reader
	
	print 'Probabilities summed'
	
	f1 = open('temp/c14_dates_probs.csv','wb')
	writer = csv.writer(f1)	
	header = ['CGr_ID']
	b = 0
	while b < b_len:
		outstr = 'b' + str(int(mins[b])) + '_' + str(int(maxs[b]))
		header.append(outstr)
		b += 1
	writer.writerow(header)
	del header
	inum = 0
	for i in date_codes:
		outrow = [i]
		for j in probs[inum]:
			j = j * 1000
			j = int(j)
			j = float(j) / 1000
			outrow.append(j)
		writer.writerow(outrow)
		inum += 1	
	f1.close()
	del writer
	
	print 'Finished!'