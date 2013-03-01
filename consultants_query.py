#  Query to simplify terms used for top 50 consultants in AIP:

import csv

def cons_query(infile,outfile):
	
	reader = csv.reader(open(infile,'rb'))
	writer = csv.writer(open(outfile,'wb'))
	
	rownum = 0
	for row in reader:
		outrow = row
		if rownum == 0:
			outrow.append('Top50Cons')
		else:
			try:
				cons = str(row[1])
			except TypeError:
				cons = ''
			tempstr = 'Other'
			temp_set = set(["Museum of London Archaeology Service","Mueum of London Archaeology Service","Museum fo London Archaeology Service","Museum of Lodon, Department of Greater London Archaeology","Museum of London","Museum of London Archaeological Service","Museum of London Archaeology","Museum of London Archaeology  Service","Museum of London Archaeology Service","Museum of London Archaeology Service, Passmore Edwards Museum","Museum of London Archaeology Services","Museum of London Archaology Service","Museum of London Arhaeology Service","Museum of London Department of Greater London Archaeology","Museum of London, Department of Greater Archaeology","Museum of London, Department of Greater London Archaeology","Museum of London, Department of Greater London Archaeology (South West Section)","Museum of London, Department of Greater London Archaeology (Southwark & Lambeth)","Museum of London, Department of Greater London Archaeology, (South West)","Museum of London, Department of Greater London Archaeology, South West Section","Museum of London, Department of Urban Archaeology","Museum of London, Deprtment of Greater London Archaeology","Museum of London,Department of Greater London Archaeology","Museum of London. The Department of Greater London Archaeology (North)","MoLAS"])
			if cons in temp_set:
				tempstr = 'MOLA'
			temp_set = set(["Wessex Archaeology","Wessex Archaeology in London","Wessex Archaeology Ltd","Wessex Archaeology Ltd."])
			if cons in temp_set:
				tempstr = 'Wessex'
			temp_set = set(["Suffolk County Council Archaeological Service","Suffolk County Council Archaeological Section","Suffolk County Council Archaeological Section, Field Projects Team","Suffolk County Council Archaeological Service","Suffolk County Council Archaeological Service Field Project Team","Suffolk County Council Archaeological Service Field Projects Team","Suffolk County Council Archaeological Services","Suffolk County Council Archaeological Unit","Suffolk County Council Archaeology Section","Suffolk County Council Archeological Unit","Suffolk County Council, Archaeological Section"])
			if cons in temp_set:
				tempstr = 'Suffolk CC'
			temp_set = set(["Thames Valley Archaeological Services","Thames Valey Archaeological Services","Thames Valley Archaeological Service","Thames Valley Archaeological Services","Thames Valley Archaeological Society","Thames Valley Archaeological Unit","Thames Valley Archaeology Service","Thames Valley Archaeology service","Thames Vlley","Thames Vlley Archaeological Services"])
			if cons in temp_set:
				tempstr = 'Thames Valley'
			temp_set = set(["Archaeological Project Services","Archaeologcial Project Services","Archaeologial Project Services"])
			if cons in temp_set:
				tempstr = 'Arch. Project Services'
			temp_set = set(["Canterbury Archaeological Trust","Canterbury Archeological Trust"])
			if cons in temp_set:
				tempstr = 'Canterbury'
			temp_set = set(["University of Leicester Archaeological Services","ULAS","University of Leicester Arcaheological Services","University of Leicester Archaeolgoical Services","University of Leicester Archaeological Service","University of Leicester Archaeological Services","University Of Leicester Archaeological Services","University of LeicesterArchaeological Services"])
			if cons in temp_set:
				tempstr = 'ULAS'
			temp_set = set(["Norfolk Archaeological Unit"])
			if cons in temp_set:
				tempstr = 'Norfolk'
			temp_set = set(["Archaeology South-East","Archaeology South East"])
			if cons in temp_set:
				tempstr = 'Arch. S.E.'
			temp_set = set(["Northamptonshire Archaeology","Northampton Archaeology","Northampton Archeology Unit","Northamptonshire Archaeological Unit","Northamptonshire Archaeology","Northamptonshire Archaeology Unit","Northamptonshire County Council","Northamptonshire County Council Archaeology Unit","Northamptonshire County Council Archaeology unit","Northamptonshire County Council, Northamptonshire Archaeology","Northamptonshire Heritage","Northamptoshire Archaeology"])
			if cons in temp_set:
				tempstr = 'Northampton'
			temp_set = set(["Oxford Archaeological Unit","Oxford Archaeology","Oxford Archaeology North","Oxford Achaeological Unit","Oxford Archaeological Advisory Service","Oxford Archaeological Associates","Oxford Archaeological Associates Ltd","Oxford Archaeologicl Unit","Oxford Archaeology East","Oxford Archaeology South","Oxford Archaeology Unit","Oxford Archaeoogical Unit","Oxford Archaeotechnics","Oxford Archaeotechnics Limited","Oxford Archaological Unit","oxford archeology","Oxford City UAD","Oxford University","Oxford University Archaeological Society","Oxfordshire County Archaeological Service","Oxord Archaeological Unit"])
			if cons in temp_set:
				tempstr = 'Oxford'
			temp_set = set(["Humber Field Archaeology","Humber Archaeology Partnership","Humber Field Archaeology","Humberside Archaeological Partnership","Humberside Archaeological Unit","Humberside Archaeology","Humberside Archaeology Unit"])
			if cons in temp_set:
				tempstr = 'Humber'
			temp_set = set(["Warwickshire Museum Field Services","Warwickshire County Council, Warwickshire Museum (?Field Archaeology Section)","Warwickshire County Council, Warwickshire Museum Field Archaeology Section","Warwickshire County Council, Warwickshire Museum Field Archaeology Section (subcon to Dr P Collins)","Warwickshire County Council, Warwickshire Museum Field Archaeology Section (subcon: Dr Paul Collins)","Warwickshire Museum","Warwickshire Museum Field Archaeology Section","Warwickshire Museum Field Archaeology Unit","Warwickshire Museum Field Services","Warwickshire Museum, Warwickshire County Council Libraries and Heritage","Warwickshire Museums"])
			if cons in temp_set:
				tempstr = 'Warwickshire'
			temp_set = set(["AC archaeology","AC Archaeology","AC archaeology, Wareham and District Archaeology"])
			if cons in temp_set:
				tempstr = 'AC Arch.'
			temp_set = set(["Cotswold Archaeological Trust","Cotswold Archaeology","Cotswold Archaeological Trust Limited","Cotswold Archaeological Trust Ltd","Cotswold Archaeological Trust Ltd."])
			if cons in temp_set:
				tempstr = 'Cotswold'
			temp_set = set(["Hertfordshire Archaeological Trust","Hertford Archaeological Trust","Hertfordshire Archaeological Trust","Hertfordshire Archaeoloigical Trust"])
			if cons in temp_set:
				tempstr = 'Hertfordshire'
			temp_set = set(["Gloucestershire County Council Archaeology Service","Gloucester Archaeological Unit","Gloucester Archaeology","Gloucester Archaeology Unit","Gloucester City Excavations Unit","Gloucester City Museum Excavations Unit","Gloucester City Musuem Excavations Unit","Gloucestershire County Council Archaeological Service","Gloucestershire County Council Archaeology Service","Gloucestershire County Council, County Archaeological Service"])
			if cons in temp_set:
				tempstr = 'Gloucestershire'
			temp_set = set(["Lindsey Archaeological Services","Lindsey Arcaheological Services","Lindsey Archaeological Services","Lindsey Archaeoological Services","Lindsey Arhcaeological Services"])
			if cons in temp_set:
				tempstr = 'Lindsey'
			temp_set = set(["Surrey County Archaeological Unit"])
			if cons in temp_set:
				tempstr = 'Surrey'
			temp_set = set(["Exeter Archaeology","Exeter Museums Archaeological Field Unit","Exeter Museums Field Archaeological Unit","Exeter Museums Field Archaeology Unit"])
			if cons in temp_set:
				tempstr = 'Exeter'
			temp_set = set(["Pre-Construct Archaeology Ltd.","Pre-Construct Archaeology (Lincoln)","Pre-Construct Archaeology Ltd","Pre- Construct Archaeology","Pre--Construct Archaeology","Pre-Construct (Lincoln)","Pre-Construct Archaeology","Pre-construct Archaeology","Pre-Construct Archaeology (Lincoln)","Pre-Construct Archaeology Ltd","Pre-Construct Archaeology Ltd, CgMs","Pre-Construct Archaeology Ltd.","Pre-Construct Archaeoology Ltd.","Pre-Construct Geophysics","Pre-Costruct Archaeology (Lincoln)"])
			if cons in temp_set:
				tempstr = 'Pre-Construct'
			temp_set = set(["Cambridge Archaeological Unit","Cambridge Archaeological Field Group","Cambridge Archaeological Unit","Cambridge Archaeological unit","Cambridge Archaeology Field Club","Cambridge Archaeology Field Group","Cambridge Archaeology Unit"])
			if cons in temp_set:
				tempstr = 'Cambridge'
			temp_set = set(["Northern Archaeological Associates","Northern Archaeological Assocaites","Northern Archaeological Associates","Northern Archaeological Associates.","Northern Archaeology Group","Northern Counties Archaeological Services"])
			if cons in temp_set:
				tempstr = 'Northern Arch.'
			temp_set = set(["Archaeological Solutions","Archaeological Solutions Ltd","Archaeological Solutions LTD"])
			if cons in temp_set:
				tempstr = 'Arch. Solutions'
			temp_set = set(["Birmingham University Field Archaeology Unit","Birmingham University Archaeology Unit","Birmingham University Field Archaeology Section","Birmingham University Field Archaeology Unit","BIrmingham University Field Archaeology Unit","Birmingham University Field Archaeology Unit and Glasgow University","Birmingham University Field Archaeology Unit, Phoenix Consultants","Birmingham University Field Archaeology Unit, Worcestershire County Council Archaeological Services","Birmingham University Field Archaeoloy Unit","Birmingham University Field Unit"])
			if cons in temp_set:
				tempstr = 'Birmingham Univ.'
			temp_set = set(["AOC Archaeology Group","AOC Archaeology","AOC Archaeology Group","AOC Archaeology Limited","AOC Archaeology Ltd"])
			if cons in temp_set:
				tempstr = 'AOC Arch.'
			temp_set = set(["Essex County Coucil Field Archaeology Group","Essex County Coucil Field Archaeology Unit","Essex County Council","Essex County Council Archaeaology Section","Essex County Council Archaeological Advisory Group","Essex County Council Archaeological Field Project Service","Essex County Council Archaeological Field Project Unit","Essex County Council Archaeological Field Projects Section","Essex County Council Archaeological Field Projects Service","Essex County Council Archaeology Field Projects Service","Essex County Council Archaeology Section","Essex County Council Archaeology Service","Essex County Council Archeology Section","Essex County Council Field Archaeaology Group","Essex County Council Field Archaeolgy Group","Essex County Council Field Archaeology Group","Essex County Council Field Archaeology Service","Essex County Council Field Archaeology Unit","Essex County Council Field Archeology Group","Essex County Council Heritage Advice Management & Promotion Team","Essex County Council Heritage Advice Mangagement & Promotion Team","Essex County Council Heritage Advice Mangagement and Promotion Team","Essex County Council Heritage Conservation Branch","Essex County Council Planning-Field Archaeology Group","Essex County Council, Archaeological Advisory Group","Essex County Council, Archaeology Field Projects Section","Essex County Council, Field Archaeology Group","Essex County Council, Field Archaeology Unit","Essex County Council, Planning Department, Archaeological Field Projects Service","Essex County Council: archaeology section"])
			if cons in temp_set:
				tempstr = 'Essex'
			temp_set = set(["Archaeological Services WYAS"])
			if cons in temp_set:
				tempstr = 'Arch. Services WYAS'
			temp_set = set(["Lancaster University Archaeological Unit","Lancaster Univeristy Archaeological Unit","Lancaster University Archaeological Unit","Lancaster University Archaeological Unit.","Lancaster University Archaeology Unit","Lancaster University Heritage Planning Consultancy","Lancaster Unviersity Archaeological Unit"])
			if cons in temp_set:
				tempstr = 'Lancaster Univ.'
			temp_set = set(["University of Durham, Archaeological Services","Archaeological Services, Durham University","Archaeological Services, Univerisity of Durham","Archaeological Services, University of Durham"])
			if cons in temp_set:
				tempstr = 'Durham'
			temp_set = set(["Colchester Archaeological Trust","Colchester Archaeological Group","Colchester Archaeological Trust","Colchester Archaeological Trust Ltd","Colchester Archaeological Trust/Howard Brooks Archaeological Services","Colchester Archaeological Unit"])
			if cons in temp_set:
				tempstr = 'Colchester'
			temp_set = set(["Southampton City Council Archaeology Unit","Southampton City Council","Southampton City Council Arch.&Heri. Manage. Sctn.","Southampton City Council Archaeological Operations Unit","Southampton City Council Archaeology","Southampton City Council Archaeology & Heritage Management Section","Southampton City Council Archaeology Operations Unit","Southampton City Council Archaeology Unit","Southampton CIty Council Archaeology Unit","Southampton City Council Heritage Policy Unit"])
			if cons in temp_set:
				tempstr = 'Southampton'
			temp_set = set(["Archaeological Services & Consultancy Ltd.","Archaeological Services & Consultancy Limited","Archaeological Services & Consultancy Ltd","Archaeological Services & Consultancy Ltd.","Archaeological Services and Consultancy Limited","Archaeological Services and Consultancy Ltd"])
			if cons in temp_set:
				tempstr = 'Arch. Services & Consultancy'
			temp_set = set(["John Moore Heritage Services","John Moore Heritage Consultants"])
			if cons in temp_set:
				tempstr = 'John Moore'
			temp_set = set(["Cornwall Archaeological Unit","Cornwall Archaeological Unit Cornwall County Council","Cornwall Archaeological Unit, Cornwall County Council","Cornwall Archaeological Unit, Cornwall County Council & North Cornwall District Council","Cornwall County Council"])
			if cons in temp_set:
				tempstr = 'Cornwall'
			temp_set = set(["Albion Archaeology"])
			if cons in temp_set:
				tempstr = 'Albion'
			temp_set = set(["Hereford & Worcester County Council, County Archaeological Service","Hereford & Worcester Archaeology Section (C.C.)","Hereford & Worcester County Council, County Archaeological Service","Hereford and Worceser County Archaeological Service","Hereford and Worcester Archaeology Section","Hereford and Worcester Archaeology section","Hereford and Worcester County Archaeological Service","Hereford and Worcester County Council Archaeological Service"])
			if cons in temp_set:
				tempstr = 'Hereford & Worcester'
			temp_set = set(["Tyne & Wear Museums Archaeology Department","Tyne & Wear Specialist Conservation Team","Tyne & Wears Museum Archaeology Department","Tyne and Wear Museums Archaeology","Tyne and Wear Museums Archaeology Department","Tyne and Wear Museums Archaeology Service"])
			if cons in temp_set:
				tempstr = 'Tyne & Wear'
			temp_set = set(["Bristol and Region Archaeological Services","Bristol and Region and Archaeological Servcies","Bristol and Region Archaological Services"])
			if cons in temp_set:
				tempstr = 'Bristol'
			temp_set = set(["Foundations Archaeology"])
			if cons in temp_set:
				tempstr = 'Foundations'
			temp_set = set(["Avon Archaeological Unit"])
			if cons in temp_set:
				tempstr = 'Avon'
			temp_set = set(["City of Lincoln Archaeology Unit","Lincoln Archaeology"])
			if cons in temp_set:
				tempstr = 'Lincoln'
			temp_set = set(["Southern Archaeological Services","Southern Archaeological  Services Ltd","Southern Archaeological Services","southern Archaeological Services","Southern Archaeological Services Limited","Southern Archaeological Services Ltd","Southern Archaeological Services Ltd.","Southern Archaeologiical Services"])
			if cons in temp_set:
				tempstr = 'Southern Arch.'
			temp_set = set(["North Pennines Archaeology Ltd.","North Pennines Archaeology Ltd"])
			if cons in temp_set:
				tempstr = 'North Pennines'
			temp_set = set(["John Samuels Archaeological Consultants","John Samules Archaeological Consultants"])
			if cons in temp_set:
				tempstr = 'John Samuels'
			temp_set = set(["Trent and Peak Archaeological Trust","Trent & Peak Archaeological Trust","Trent & Peak Archaeological Tust","Trent & Peak Archaeological Unit","Trent and Peak Archaeological Trust Ltd","Trent and Peak Archaeological Unit"])
			if cons in temp_set:
				tempstr = 'Trent & Peak'
			temp_set = set(["University of Manchester Archaeological Unit","University of Manchester","University of Manchester Archaeology Unit"])
			if cons in temp_set:
				tempstr = 'Manchester Univ.'
			temp_set = set(["MAP Archaeological Consultancy Ltd.","MAP Arcahaeological Consultancy","MAP Archaeological Consultancy","MAP Archaeological Consultancy Ltd","MAP Archaeological Consultancy Ltd.,","MAP Archaeological Consultants","MAP Archaeological Consultants Ltd"])
			if cons in temp_set:
				tempstr = 'MAP'
			temp_set = set(["Birmingham Archaeology","Birmingham City Council, Planning Archaeologist","Birmingham Field Archaeology Unit"])
			if cons in temp_set:
				tempstr = 'Birmingham City'
			temp_set = set(["Heritage Network","Hertiage Network","Heritage network"])
			if cons in temp_set:
				tempstr = 'Heritage Network'
			temp_set = set(["York Archaeological Trust","York Archaeological Trust for Excavation and Research","York Archaeological Trust for Excavation and Research Ltd","York Archaeological Trust for Excavation and Research Ltd.","York Archaeological Trust for Excavtion and Research Ltd","York Archaeological Trust for Research and Excavation","York Archaeological Trust for Research and Excavation Ltd"])
			if cons in temp_set:
				tempstr = 'York Arch. Trust'
			outrow.append(tempstr)
		writer.writerow(outrow)
		rownum += 1