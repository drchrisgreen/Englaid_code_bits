# Module to create standard periods from years or other period terms: it requires four inputs:
# the name of the HER, and the lists of periods, start and end dates.  These should be python
# list objects.

def lookup(her_name, period_list, start_list, end_list):
	
	outlist = []
	
	# First, we need to define our break points (for the specific HER if it uses 700 BC for the BA to IA transition).
	# There actually seem to be rather a lot of them...
	
	her_set = set(['Devon','Greater Manchester','Central Bedfordshire and Luton','Birmingham','Coventry','Lancashire','NorthLincolnshire','NorthYorkshire','Sandwell','Winchester','Southampton','WestBerkshire','Isle of Wight'])
	if her_name in her_set:
		BA_to_IA = -700
	else:
		BA_to_IA = -800
	BA_end = -700
	IA_start = -800
	IA_to_RO = 43
	RO_to_EM = 410
	EM_end = 1066
			
	# Next, we define the sets of period terms that might relate to our six periods (lower case).
	# The ones with closing but no opening brackets aren't a mistake, the brackets don't seem to be opened in the HER data (Wiltshire & Swindon).
	PR_terms = set(['prehistoric','later prehistoric','prehistoric - 500000 bc to 42 ad)'])
	BA_terms = set(['bronze age','early bronze age','middle bronze age','late bronze age','bronze age - 2350 bc to 701 bc)'])
	IA_terms = set(['iron age','lpria','early iron age','middle iron age','late iron age','iron age - 800 bc to 42 ad)'])
	RO_terms = set(['roman','c1','c2','c3','c4','1st century','2nd century','3rd century','4th century','earlier roman','later roman','roman - 43 ad to 409 ad)'])
	EM_terms = set(['early medieval','saxon','anglian','viking','post-roman','sub-roman','anglo-saxon','dark age','dark ages','earlier medieval','c5','c6','c7','c8','c9','c10','c11','early medieval (saxon) - 410 ad to 1065 ad)'])
	UN_terms = set(['uncertain','unknown','unknown date'])
	
	# if there is data in the period list we will use that:
	if len(period_list) > 0:
		for x in period_list:
			current = x.lower()
			if current in PR_terms:
				outlist.append('Prehistoric')
			if current in BA_terms:
				outlist.append('Bronze Age')
			if current in IA_terms:
				outlist.append('Iron Age')
			if current in RO_terms:
				outlist.append('Roman')
			if current in EM_terms:
				outlist.append('Early medieval')
			if current in UN_terms:
				outlist.append('Uncertain')
		if len(outlist) == 0:  # If the list is still empty, it must be a bad date...
			outlist.append('BAD DATE!')
	# if there is no data in the period list, we will use the start and end dates
	# this assumes that they are ordered in order of association:
	else:
		xnum = 0
		for x in start_list:
			start = x
			end = end_list[xnum]
			if start == None or start == 'None' or '\n' in start or start == '' or end == '' or end == None or end == 'None':
				outlist.append('Uncertain')
			elif start[-1:].isdigit() == True and end[-1:].isdigit() == True:  # Otherwise turn it into an integer (testing it is a digit first)
				start = int(start)
				end = int(end)
				if end < start:  # If the end date is lower than the start date, they must be a bad date...
					outlist.append('BAD DATE!')
				else:
					if end <= BA_end and start >= -3000:  # 3000 BC is actually before the Bronze Age, but I just want to separate out all of those entries that go back to -500000 or something
						outlist.append('Bronze Age')
					elif start == EM_end:
						outlist.append('Medieval')
					elif end <= BA_to_IA and start < -3000:
						outlist.append('Prehistoric')
					elif start < BA_to_IA and end <= IA_to_RO:
						outlist.append('Prehistoric')
					elif start >= IA_start and end <= IA_to_RO:
						outlist.append('Iron Age')
					elif start >= IA_to_RO and end <= RO_to_EM:
						outlist.append('Roman')
					elif start >= RO_to_EM:
						outlist.append('Early medieval')
					elif start < BA_to_IA and end <= RO_to_EM:
						outlist.append('Prehistoric; Roman')
					elif start < IA_to_RO and end <= RO_to_EM:
						outlist.append('Iron Age; Roman')
					elif start >= IA_to_RO and end > RO_to_EM:
						outlist.append('Roman; Early medieval')
					elif start < BA_to_IA and end > RO_to_EM:
						outlist.append('Prehistoric; Roman; Early medieval')
					elif start < IA_to_RO and end > RO_to_EM:
						outlist.append('Iron Age; Roman; Early medieval')
					else:
						outlist.append('Uncertain')
			else:  #  Otherwise assume it is a bad date...
				outlist.append('BAD DATE!')
			xnum += 1
	
	return outlist