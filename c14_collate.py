import csv

def process():
	f1 = open('temp/set_all.js', 'rU')
	f2 = open('temp/c14_dates_detailed.csv', 'wb')
	
	writer = csv.writer(f2)
	
	header = ['CGr_ID','date_mid','prob']
	writer.writerow(header)
	
	cgr_id = 0
	start_date = 0
	resolution = 0
	normalise = 0
	processing = 0
	
	for line in f1:
		line = line.lstrip().rstrip()
		if 'if(!ocd' in line:
			processing = 1
		if processing == 1 and '.name' in line:
			pos1 = line.find('\"') + 1
			pos2 = line[pos1 + 1:].find('\"') + pos1 + 1
			cgr_id = int(line[pos1:pos2])
		if processing == 1 and 'likelihood.start' in line:
			pos1 = line.find('=') + 1
			pos2 = line.find(';')
			start_date = float(line[pos1:pos2])
		if processing == 1 and 'likelihood.resolution' in line:
			pos1 = line.find('=') + 1
			pos2 = line.find(';')
			resolution = float(line[pos1:pos2])
		if processing == 1 and 'likelihood.probNorm' in line:
			pos1 = line.find('=') + 1
			pos2 = line.find(';')
			normalise = float(line[pos1:pos2])
		if processing == 1 and 'likelihood.prob=' in line:
			pos1 = line.find('likelihood.prob')
			tempstr = line[pos1:]
			pos1 = tempstr.find('[') + 1
			pos2 = tempstr.find(']')
			tempstr = tempstr[pos1:pos2]
			pos = tempstr.find(',')
			if pos != -1:
				while pos != -1:
					tempint = float(tempstr[:pos].lstrip().rstrip()) * normalise
					outrow = [cgr_id,start_date,tempint]
					writer.writerow(outrow)
					start_date += resolution
					pos += 1
					tempstr = tempstr[pos:]
					pos = tempstr.find(',')
				tempint = float(tempstr.lstrip().rstrip())
				outrow = [cgr_id,start_date,tempint]
				writer.writerow(outrow)
			processing = 0
	
	f1.close()
	f2.close()