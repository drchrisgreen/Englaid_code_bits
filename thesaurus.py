# Module to define simple classification terms
import thesaurus_PAS as thPAS
import csv

def process_file():
	infile = 'temp/montypes.csv'
	outfile = 'temp/new_terms.csv'
	eidpos = 0
	perpos = 1
	typpos = 2
	
	f1 = open(infile,'rU')
	f2 = open(outfile,'wb')
	reader = csv.reader(f1)
	writer = csv.writer(f2)
	rownum = 0
	header = ['eid','term']
	writer.writerow(header)
	for row in reader:
		if rownum > 0:
			eid = row[eidpos]
			per = row[perpos].upper()
			typ = row[typpos]
			if 'PREHISTORIC' in per:
				templist = createsimple('PR',typ)
				if len(templist) > 0:
					for i in templist:
						outrow = [eid,i]
						writer.writerow(outrow)
			if 'BRONZE AGE' in per:
				templist = createsimple('BA',typ)
				if len(templist) > 0:
					for i in templist:
						outrow = [eid,i]
						writer.writerow(outrow)
			if 'IRON AGE' in per:
				templist = createsimple('IA',typ)
				if len(templist) > 0:
					for i in templist:
						outrow = [eid,i]
						writer.writerow(outrow)
			if 'ROMAN' in per:
				templist = createsimple('RO',typ)
				if len(templist) > 0:
					for i in templist:
						outrow = [eid,i]
						writer.writerow(outrow)
			if 'EARLY MEDIEVAL' in per:
				templist = createsimple('EM',typ)
				if len(templist) > 0:
					for i in templist:
						outrow = [eid,i]
						writer.writerow(outrow)
		rownum +=1
	f1.close()
	f2.close()
		

# This module defines simplified type terms (as ArcGIS has a 254 char limit for text fields):
def createsimple(period, input):
	period = period.upper()
	if period == 'UNCERTAIN':  # These are just in case the period terms aren't already abbreviated
		period = 'UN'
	if period == 'PREHISTORIC':
		period = 'PR'
	if period == 'BRONZE AGE':
		period = 'BA'
	if period == 'IRON AGE':
		period = 'IA'
	if period == 'ROMAN':
		period = 'RO'
	if period == 'EARLY MEDIEVAL':
		period = 'EM'
	simplelist = []
	input2 = ' ' + input.lower() + ' ' # switch to lower case and add spaces to differentiate villa from village etc!
	set1 = set([" vaccary "," cord rig ","clearance cairn", " pound ", "shieling", "corn drier", "ridge and furrow","field system", " field ", " fields", "lynchet", "reave", "plough", "waterhole", "pit alignment", "strip field", "linear earthwork", "agricultur", "animal", "granary", "granaries", "corn drying", "fishpond", "stock enclosure", "grazing", "cultivation", "livestock", " ard ", " spade ", " hoe ", " arable", "pasture", "terrace", " farm", " pond", " well "," cross dyke"])
	set2 = set([" lann "," bishops palace ","viereckschanzen", "votive pit", " urnfield", " ossuary", " tomb", " altar", " cross ", "guest house", "hermitage", " college ", "augustinian", "cluniac", "benedictine", "inhumation", "cremation", "burial", "cemetery", "barrow", "temple", "shrine", "church", "abbey", "monastery", "minster", "ritual", "religious", "funerary", "cist", "baptistery", "coffin", " grave ", "graveyard", "gravestone", "human remains", "mausoleum", "mithraeum", "mortuary", "nunnery", "nymphaeum", "cremated", "cairn", "stone circle", "stone cove", "standing stone", "timber platform", " slab "])
	set3 = set(["promontory fort","cliff castle"," civic ", "town", "burh", "burgh", "civitas", "colonia", "hamlet", "village", "vicus", "canabae", "oppidum", "hillfort", "hill-fort", "hill fort", "settlement", "midden", "timber platform", "occupation"])
	set4 = set(["sunken feature building", " sfb ", "villa ", "mansio", "roundhouse", "house", "longhouse", "ringwork", "d-shaped enclosure", "sub-rectangular enclosure", "d shaped enclosure", "subrectangular enclosure", "sub rectangular enclosure", "banjo enclosure", "farmstead", "burnt mound", "barn", "fogou", " hut ", "grubenhaus", "mosaic", "floor", "moat", "farmhouse", "farm enclosure"])
	set5 = set([" lead working"," red hill","working site", "metal working", "metalworking", "iron working", "bronze working", "mine ", " quarry", " kiln ", " tile kiln", " tile works", "manufacturing", " works", "saltern", "salt pan", "salt production", "mint", "industrial", " ore ", "streamworks", "bloomery", "furnace", " slag ", "textile manufacturing", "textile production"])
	set6 = set(["ferry terminal", "pavement", " road ", " track ", "trackway", "hollow way", "ridgeway", " drove", "quay", "jetty", " bridge ", " canal ", "aqueduct", "harbour", "port", "causeway ", "walkway"])
	set7 = set(["marching camp", "principia", " palisade" "legionary", "fortification"," fortified", "fortlet", "hillfort", "hill-fort", " fort ", "fortress", "castellum", "castrum", "burh", "burgh", "ringwork", "defensive", "defences", "defended", "defence", "cliff castle"])
	set8 = set([" post alignment "," post built "," wreck"," mounds ","dyke", "viereckschanzen", " mound ", "ditch", "ditches", " ditched", " pit", " pits", "find", "hoard", "metalwork ", "watercraft", " boat ", "canoe", " ship ", "coastal transport", "enclosure", "gully", "gullies", " building ", "midden", "linear earthwork", "boundar", "land division", "timber", "wooden", "flood defence", "flood protect", " manor "," ringditch"," ring ditch"])
	set9 = set([" object ", " adze ", " amphora ", " brooch ", " animal shoe ", " arm band ", " arm guard ", " armour ", " weapon ", " weapons ", " arrowhead ", " artefact ", " finds ", " findspot ", " find spot ", " awl ", " axe ", " axehead ", " axes ", " battleaxe ", " bead ", " beads ", " beaker ", " quern ", " belt buckle ", " belt fitting ", " blade ", " blades ", " scraper ", " bell ", " bowl ", " bracelet ", " bracteate ", " bridle ", " sword ", " handle ", " vessel ", " bronzes", " buckle ", " bucket ", " buckles ", " brooches ", " burin ", " fastener ", " button ", " buttons ", " carved ", " celtic head ", " chess piece ", " chisel ", " chisels ", " cinerary urn ", " fastening ", " coin ", " collared urn ", " coins ", " comb ", " cosmetic ", " currency ", " cutlery ", " dagger ", " detector", " dice ", " die ", " dirk ", " disc ", " dish ", " denarius ", " accessories ", " dress ", " ear ", " effigy ", " ferrule ", " fibula ", " figurine ", " figure of a", " find ", " ring ", " cup ", " flake ", " container ", " gallienus ", " gilt bronze leaf ", " girdle hanger ", " vessels ", " stater ", " hair pin ", " hairpin ", " hair care ", " hammer ", " hammerstone ", " harness ", " hob nail ", " hook ", " horseshoe ", " horse shoe ", " horseshoes ", " inscribed stone ", " intaglio ", " ironwork ", " implement ", " jewellery", " jewelry ", " key ", " knife ", " ladle ", " latchlifter ", " arrowhea ", " lock ", " tool ", " lomweight ", " loomweight ", " mace ", " macehead ", " mortaria ", " mortarium ", " mould ", " nail ", " nails ", " needle ", " palette ", " palm cup ", " palstave ", " pestle ", " pick ", " pin ", " pins ", " pitch forks ", " plumb bob ", " point ", " pot ", " pottery", " projectile ", " punch ", " rake ", " sherd ", " scabbard ", " seal ", " shackle ", " equipment ", " shears ", " shield ", " sickle ", " sleeve ", " spatula ", " spear ", " spearhead", " spindle whorl ", " spoon ", " spurs ", " statue ", " statuette ", " stirrup ", " stirrups ", " strap ", " stud ", " studs ", " stylus ", " sword ", " swords ", " thimble ", " toggle ", " tools  ", " tripod ", " tweezers ", " urn ", " urn: ", " vase ", " votive tablet ", " weight ", " weights ", " whetstone ", " worked ", " writing", " ligula ", " sherd ", " sherds ", " sherd(s) ", " vessel ", " pottery ", " potsherd ", " potsherds ", " potsherd(s) ", " anchor ", " anchors "])
	for x in set1:
		if x in input2:
			tempstr = period + "01"
			found = 0
			if 'ridge and furrow' in input2 or' field ' in input2 or 'lynchet' in input2 or 'reave' in input2 or ' fields' in input2 or ' cord rig' in input2:
				if 'coaxial field' in input2 or 'co-axial field' in input2:
					simplelist.append(tempstr + 'A')
					found = 2
				if 'linear field' in input2 or 'rectilinear field' in input2:
					simplelist.append(tempstr + 'B')
					found = 2
				if 'aggregate field' in input2:
					simplelist.append(tempstr + 'C')
					found = 2
				if 'strip field' in input2:
					simplelist.append(tempstr + 'D')
					found = 2
				if found != 2:
					simplelist.append(tempstr + 'E')
				found = 1
			if ' ard ' in input2 or ' hoe ' in input2 or ' spade ' in input2 or ' plough' in input2 or 'farming' in input2 or 'agricultur' in input2 or 'cultivation' in input2 or ' arable' in input2  or 'terrace' in input2 or 'clearance cairn' in input2:
				simplelist.append(tempstr + 'F')
				found = 1
			if 'linear earthwork' in input2:
				simplelist.append(tempstr + 'G')
				found = 1
			if 'pit alignment' in input2:
				simplelist.append(tempstr + 'H')
				found = 1
# 			if '???' in input2:
# 				simplelist.append(tempstr + 'I')
# 				found = 1
			if 'waterhole' in input2 or ' pond' in input2 or ' well ' in input2:
				simplelist.append(tempstr + 'J')
				found = 1
			if 'corn drying' in input2 or 'corn drier' in input2:
				simplelist.append(tempstr + 'K')
				found = 1
			if 'granary' in input2 or 'granaries' in input2:
				simplelist.append(tempstr + 'L')
				found = 1
			if 'fishpond' in input2:
				simplelist.append(tempstr + 'M')
				found = 1
			if 'stock enclosure' in input2 or ' pound ' in input2 or 'grazing' in input2 or 'pasture' in input2 or 'shieling' in input2 or ' vaccary ' in input2:
				simplelist.append(tempstr + 'N')
				found = 1
			if ' cross dyke' in input2:
				simplelist.append(tempstr + 'O')
				found = 1
			if found == 0:
				simplelist.append(tempstr)
	for x in set2:
		if x in input2:
			if input2 != ' cross dyke ':
				tempstr = period + "02"
				found = 0
				if 'inhumation' in input2 or 'cist' in input2 or ' grave' in input2:
					if 'cemetery' in input2 or 'graveyard' in input2:
						simplelist.append(tempstr + 'D')
						found = 1
					else:
						simplelist.append(tempstr + 'A')
						found = 1
				if 'cremation' in input2 or 'cremated' in input2 or ' urnfield' in input2:
					if 'cemetery' in input2 or ' urnfield' in input2:
						simplelist.append(tempstr + 'E')
						found = 1
					else:
						simplelist.append(tempstr + 'B')
						found = 1
				if found != 1 and 'cemetery' in input2:
					simplelist.append(tempstr + 'F')
					found = 1
				if found != 1 and ('burial' in input2 or 'cist' in input2 or 'grave' in input2):
					simplelist.append(tempstr + 'C')
					found = 1
				if 'funerary' in input2 or 'mortuary' in input2 or 'human remains' in input2 or 'mausoleum' in input2 or ' tomb' in input2 or ' ossuary' in input2:
					simplelist.append(tempstr + 'G')
					found = 1
				if 'barrow' in input2:
					simplelist.append(tempstr + 'H')
					found = 1
				if 'cairn' in input2:
					simplelist.append(tempstr + 'I')
					found = 1
				if 'temple' in input2 or 'mithraeum' in input2 or 'nymphaeum' in input2:
					simplelist.append(tempstr + 'J')
					found = 1
				if 'shrine' in input2 or 'sanctuary' in input2:
					simplelist.append(tempstr + 'K')
					found = 1
				if 'church' in input2 or 'baptistery' in input2 or ' lann '  in input2:
					simplelist.append(tempstr + 'L')
					found = 1
				if 'abbey' in input2 or 'monastery' in input2 or 'minster' in input2 or 'nunnery' in input2 or 'augustinian' in input2 or 'cluniac' in input2 or 'benedictine' in input2 or ' college ' in input2 or 'hermitage' in input2 or 'guest house' in input2 or ' bishops palace ' in input2:
					simplelist.append(tempstr + 'M')
					found = 1
				if 'standing stone' in input2:
					simplelist.append(tempstr + 'N')
					found = 1
				if 'stone circle' in input2 or 'stone cove' in input2:
					simplelist.append(tempstr + 'O')
					found = 1
				if input2 == ' cross ' or ' grave marker ' in input2 or input2 == ' slab ' or ' gravestone ' in input2 or ' grave stone ' in input2 or ' grave-stone ' in input2:
					simplelist.append(tempstr + 'P')
					found = 1
				if 'timber platform' in input2:
					simplelist.append(tempstr + 'Q')
					found = 1
				if found == 0 and 'cross dyke' not in input2:
					simplelist.append(tempstr)
	for x in set3:
		if x in input2:
			tempstr = period + "03"
			found = 0
			if 'town' in input2:
				simplelist.append(tempstr + 'A')
				found = 1
			if 'burh' in input2 or 'burgh' in input2:
				simplelist.append(tempstr + 'B')
				found = 1
			if 'civitas' in input2 or 'colonia' in input2:
				simplelist.append(tempstr + 'C')
				found = 1
			if 'hamlet' in input2 or 'village' in input2:
				simplelist.append(tempstr + 'D')
				found = 1
			if 'vicus' in input2:
				simplelist.append(tempstr + 'E')
				found = 1
			if 'canabae' in input2:
				simplelist.append(tempstr + 'F')
				found = 1
			if 'oppidum' in input2:
				simplelist.append(tempstr + 'G')
				found = 1
			if 'hillfort' in input2 or 'hill fort' in input2 or 'hill-fort' in input2 or 'promontory fort' in input2 or 'cliff castle' in input2:
				simplelist.append(tempstr + 'H')
				found = 1
			if 'unenclosed' in input2:
				simplelist.append(tempstr + 'I')
				found = 1
			if ' enclosed' in input2 or 'enclosure' in input2:
				simplelist.append(tempstr + 'J')
				found = 1
			if 'linear settlement' in input2:
				simplelist.append(tempstr + 'K')
				found = 1
			if 'palisaded' in input2:
				simplelist.append(tempstr + 'L')
				found = 1
			if 'riverside' in input2:
				simplelist.append(tempstr + 'M')
				found = 1
			if 'dispersed' in input2:
				simplelist.append(tempstr + 'N')
				found = 1
			if 'nucleated' in input2:
				simplelist.append(tempstr + 'O')
				found = 1
			if 'road-side' in input2 or 'roadside' in input2 or ' road ' in input2:
				simplelist.append(tempstr + 'P')
				found = 1
			if 'midden' in input2:
				simplelist.append(tempstr + 'Q')
				found = 1
			if 'timber platform' in input2:
				simplelist.append(tempstr + 'R')
				found = 1
			if found == 0:
				simplelist.append(tempstr + 'S')  # i.e. unspecified settlement
	if input2 == ' round ':
		simplelist.append(period + '03J')
	for x in set4:
		if x in input2:
			tempstr = period + "04"
			found = 0
			if 'villa ' in input2:
				simplelist.append(tempstr + 'A')
				found = 1
			if 'mansio ' in input2:
				simplelist.append(tempstr + 'B')
				found = 1
			if 'roundhouse' in input2 or 'round house' in input2 or 'hut circle' in input2:
				simplelist.append(tempstr + 'C')
				found = 1
			if 'longhouse' in input2 or 'long house' in input2:
				simplelist.append(tempstr + 'D')
				found = 1
			if 'farmstead' in input2 or 'farmhouse' in input2 or 'farm enclosure' in input2:
				simplelist.append(tempstr + 'E')
				found = 1
			if 'ringwork' in input2:
				simplelist.append(tempstr + 'F')
				found = 1
			if 'd-shaped enclosure' in input2 or 'd shaped enclosure' in input2:
				simplelist.append(tempstr + 'G')
				found = 1
			if 'sub-rectangular enclosure' in input2 or 'subrectangular enclosure' in input2 or 'sub rectangular enclosure' in input2:
				simplelist.append(tempstr + 'H')
				found = 1
			if 'banjo enclosure' in input2:
				simplelist.append(tempstr + 'I')
				found = 1
			if 'aisled' in input2:
				simplelist.append(tempstr + 'J')
				found = 1
			if 'rectilinear building' in input2:
				simplelist.append(tempstr + 'K')
				found = 1
			if 'burnt mound' in input2:
				simplelist.append(tempstr + 'L')
				found = 1
			if 'grubenhaus' in input2 or ' sfb ' in input2 or 'sunken feature building' in input2:
				simplelist.append(tempstr + 'M')
				found = 1
			if found == 0:
				simplelist.append(tempstr)
	for x in set5:
		if x in input2:
			if input2 != ' quarry ditch ' and input2 != ' road quarry ':
				tempstr = period + "05"
				found = 0
				if 'metal working' in input2 or 'metalworking' in input2 or ' forge ' in input2 or 'smith' in input2 or 'bronze working' in input2 or 'iron working' in input2 or 'furnace' in input2 or 'bloomery' in input2 or ' slag ' in input2 or 'silver working' in input2 or ' lead working' in input2:
					simplelist.append(tempstr + 'A')
					found = 1
				if 'bronze working' in input2 or 'copper working' in input2:
					simplelist.append(tempstr + 'B')
					found = 1
				if 'iron working' in input2:
					simplelist.append(tempstr + 'C')
					found = 1
				if ' mine ' in input2 or 'streamworks' in input2 or 'mining' in input2:
					simplelist.append(tempstr + 'D')
					found = 1
				if 'quarry' in input2 and 'quarry ditch' not in input2 and 'road quarry' not in input2:
					simplelist.append(tempstr + 'E')
					found = 1
				if 'pottery kiln' in input2 or 'pottery production' in input2 or 'pottery manufact' in input2 or 'pottery works' in input2:
					simplelist.append(tempstr + 'F')
					found = 1
				if 'tile kiln' in input2 or 'tile works' in input2:
					simplelist.append(tempstr + 'G')
					found = 1
				if 'lime kiln' in input2:
					simplelist.append(tempstr + 'H')
					found = 1
				if 'salt work' in input2 or 'saltern' in input2 or 'salt pan' in input2 or ' salt production' in input2 or ' red hill' in input2:
					simplelist.append(tempstr + 'I')
					found = 1
				if ' mint ' in input2:
					simplelist.append(tempstr + 'J')
					found = 1
				if 'textile production' in input2 or 'textile manufact' in input2:
					simplelist.append(tempstr + 'K')
					found = 1
				if found == 0:
					simplelist.append(tempstr)
	for x in set6:
		if x in input2:
			tempstr = period + "06"
			found = 0
			if (' road ' in input2 or 'pavement' in input2) and ' drove road ' not in input2:
				simplelist.append(tempstr + 'A')
				found = 1
			if ' track ' in input2 or 'trackway' in input2:
				simplelist.append(tempstr + 'B')
				found = 1
			if 'hollow way' in input2 or 'hollowway' in input2 or 'ridgeway' in input2 or 'ridge way' in input2:
				simplelist.append(tempstr + 'C')
				found = 1
			if ' drove' in input2:
				simplelist.append(tempstr + 'D')
				found = 1
			if 'quay' in input2 or 'jetty' in input2 or 'harbour' in input2 or ' port ' in input2 or 'ferry terminal' in input2:
				simplelist.append(tempstr + 'E')	
				found = 1
			if ' bridge ' in input2:
				simplelist.append(tempstr + 'F')
				found = 1
			if ' canal ' in input2 or 'canalised' in input2:
				simplelist.append(tempstr + 'G')
				found = 1
			if 'aqueduct' in input2:
				simplelist.append(tempstr + 'H')
				found = 1
			if 'causeway ' in input2:
				simplelist.append(tempstr + 'I')
				found = 1
			if found == 0:
				simplelist.append(tempstr)
	for x in set7:
		if x in input2 and input2 != ' sea defences ' and ' flood defences ' not in input2:
			tempstr = period + "07"
			found = 0
			if 'hillfort' in input2 or 'hill-fort' in input2 or 'hill fort' in input2:
				simplelist.append(tempstr + 'A')
				found = 1
			if ' fort ' in input2 or 'castellum' in input2 or "cliff castle" in input2:
				simplelist.append(tempstr + 'B')
				found = 1
			if 'fortress' in input2 or 'castrum' in input2 or 'legionary' in input2:
				simplelist.append(tempstr + 'C')
				found = 1
			if 'fortlet' in input2:
				simplelist.append(tempstr + 'D')
				found = 1
			if 'burh' in input2 or 'burgh' in input2:
				simplelist.append(tempstr + 'E')
				found = 1
			if 'ringwork' in input2:
				simplelist.append(tempstr + 'F')
				found = 1
			if found == 0:
				simplelist.append(tempstr)
	for x in set8:
		if x in input2:
			tempstr = period + "08"
			found = 0
			if ' mound ' in input2 or ' mounds ' in input2:
				simplelist.append(tempstr + 'A')
				found = 1
			if ' ditch ' in input2 or 'ditches' in input2 or ' ditched' in input2:
				simplelist.append(tempstr + 'B')
				found = 1
			if ' pit ' in input2 or 'pits' in input2:
				simplelist.append(tempstr + 'C')
				found = 1
			if ' find ' in input2 or ' finds ' in input2 or 'findspot' in input2:
				simplelist.append(tempstr + 'D')
				found = 1
			if 'hoard' in input2:
				simplelist.append(tempstr + 'E')
				found = 1
			if 'metalwork ' in input2:
				simplelist.append(tempstr + 'F')
				found = 1
			if ' boat ' in input2 or ' ship ' in input2 or 'canoe' in input2 or 'coastal transport' in input2 or ' wreck' in input2:
				simplelist.append(tempstr + 'G')
				found = 1
			if 'flood defence' in input2:
				simplelist.append(tempstr + 'H')
				found = 1
			if 'enclosure' in input2 or 'viereckschanzen' in input2:
				simplelist.append(tempstr + 'I')
				found = 1
			if 'gully' in input2 or 'gullies' in input2:
				simplelist.append(tempstr + 'J')
				found = 1
			if 'building' in input2:
				simplelist.append(tempstr + 'K')
				found = 1
			if 'midden' in input2:
				simplelist.append(tempstr + 'L')
				found = 1
			if 'linear earthwork' in input2:
				simplelist.append(tempstr + 'M')
				found = 1
			if 'boundar' in input2 or "land division" in input2:
				simplelist.append(tempstr + 'N')
				found = 1
			if 'timber' in input2 or 'wooden' in input2 or 'post built' in input2:
				simplelist.append(tempstr + 'O')
				found = 1
			if 'manor' in input2:
				simplelist.append(tempstr + 'P')
				found = 1
			if ' dyke ' in input2:
				simplelist.append(tempstr + 'Q')
				found = 1
			if ' ring ditch' in input2 or ' ringditch' in input2:
				simplelist.append(tempstr + 'R')
				found = 1
			if 'post alignment' in input2:
				simplelist.append(tempstr + 'S')
				found = 1
			if found == 0:
				simplelist.append(tempstr)
	for x in set9:
		if x in input2 and 'barrow' not in input2 and 'working site' not in input2 and 'production site' not in input2 and 'manufacturing site' not in input2 and ' kiln ' not in input2 and ' cup and ring ' not in input2 and ' cup marked ' not in input2 and 'ring ditch' not in input2 and 'ring cairn' not in input2 and 'tree ring' not in input2 and 'ring bank' not in input2 and 'enclosure ring' not in input2 and 'ring bank' not in input2 and 'ring gull' not in input2:
			tempstr = period + "08D"
			simplelist.append(tempstr)
			templist = thPAS.createsimple(input2,'N')
			for i in templist:
				if i != 'UN':
					tempstr = period + '-' + i
					simplelist.append(tempstr)
	if len(simplelist) == 0:
		simplelist.append(period + "-UN")
	simpleset = set(simplelist)
	return simpleset