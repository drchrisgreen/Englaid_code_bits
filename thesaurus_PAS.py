# Module to define simple classification terms
import csv

def process(infile, outfile, missing):
	f1 = open(infile, 'rU')
	f2 = open(outfile, 'wb')
	reader = csv.reader(f1)
	writer = csv.writer(f2)
	missing_items = open(missing, 'wb')
	
	rownum = 0
	missed = []
	desc_pos = 0
	type_pos = 0
	period_pos = 0
	eid_pos = 0
	for row in reader:
		if rownum == 0:
			header = ['eid','term']
			writer.writerow(header)
			colnum = 0
			for col in row:
				if col == 'find_description':
					desc_pos = colnum
				if col == 'find_type':
					type_pos = colnum
				if col == 'englaid_period':
					period_pos = colnum
				if col == 'eid':
					eid_pos = colnum	
				colnum += 1
			junk = createsimple('junk','Y')
		else:
			eid = row[eid_pos]
			period = row[period_pos]
			type = row[type_pos]
			desc = row[desc_pos]
			if 'EMC FINDSPOT' in desc:
				type = 'COIN'
			if 'Uncertain' in period:
				shortper = 'UN'
				output = createsimple(type,'N')
				for i in output:
					if 'UN' in i:
						missed.append(type.lower())
					term = shortper + '-' + i
					outrow = [eid,term]
					writer.writerow(outrow)
			if 'Prehistoric' in period:
				shortper = 'PR'
				output = createsimple(type,'N')
				for i in output:
					if 'UN' in i:
						missed.append(type.lower())
					term = shortper + '-' + i
					outrow = [eid,term]
					writer.writerow(outrow)
			if 'Bronze Age' in period:
				shortper = 'BA'
				output = createsimple(type,'N')
				for i in output:
					if 'UN' in i:
						missed.append(type.lower())
					term = shortper + '-' + i
					outrow = [eid,term]
					writer.writerow(outrow)
			if 'Iron Age' in period:
				shortper = 'IA'
				output = createsimple(type,'N')
				for i in output:
					if 'UN' in i:
						missed.append(type.lower())
					term = shortper + '-' + i
					outrow = [eid,term]
					writer.writerow(outrow)
			if 'Roman' in period:
				shortper = 'RO'
				output = createsimple(type,'N')
				for i in output:
					if 'UN' in i:
						missed.append(type.lower())
					term = shortper + '-' + i
					outrow = [eid,term]
					writer.writerow(outrow)
			if 'Early medieval' in period:
				shortper = 'EM'
				output = createsimple(type,'N')
				for i in output:
					if 'UN' in i:
						missed.append(type.lower())
					term = shortper + '-' + i
					outrow = [eid,term]
					writer.writerow(outrow)
		rownum += 1
		
	setMissed = set(missed)
	missed = list(setMissed)
	missed.sort()
	
	for i in missed:
		missing_items.write(str(i) + '\n')
	
	f1.close()
	f2.close()
	missing_items.close()
	
# This module defines simplified type terms:
def createsimple(input,generate):
	simplelist = []
	input = " " + input.lower() + " "
	if generate == 'Y':
		f3 = open('thesaurus_terms.txt','wb')
	
	# Coins
	simple_set = set([" coin "," coins "])
	tempstr = "CO"
	for x in simple_set:
		if x in input and "coin die" not in input and "coin mould" not in input and "coin pendant" not in input and "coin weight" not in input:
			simplelist.append(tempstr)
	if generate == 'Y':
		set_list = list(simple_set)
		set_list.sort()
		f3.write(tempstr + ':\n\n')
		for i in set_list:
			f3.write(i.lstrip().rstrip() + '\n')
		f3.write('\n\n')
	
	# Other currency items
	simple_set = set([" ingot "," miniature object "," weight "," balance "," hack-metal "," ring-money "," ring money "," brockage "," currency bar "," token "])
	tempstr = "CU"
	for x in simple_set:
		if x in input and "steelyard weight" not in input:
			simplelist.append(tempstr)
	if generate == 'Y':
		set_list = list(simple_set)
		set_list.sort()
		f3.write(tempstr + ':\n\n')
		for i in set_list:
			f3.write(i.lstrip().rstrip() + '\n')
		f3.write('\n\n')
	
	# Structural items
	simple_set = set([" tile "," roof tile "," floor tile "," flue tile "," tegula "," nail "," staple "," fire dog "," window "," daub "," wattle "," hearth lining "," fired clay "," brick "," tessera "," architectural "," architectural element "," architectural fragment "," building material "," dressed stone "," imbrex "," mosaic "," pile "," wall plaster "])
	tempstr = "SI"
	for x in simple_set:
		if x in input and "nail cleaner" not in input:
			simplelist.append(tempstr)
	if generate == 'Y':
		set_list = list(simple_set)
		set_list.sort()
		f3.write(tempstr + ':\n\n')
		for i in set_list:
			f3.write(i.lstrip().rstrip() + '\n')
		f3.write('\n\n')
	
	# Personal decorative items
	simple_set = set([" hair ring "," girdle "," crown "," neck ring "," penannular "," bracteate "," brooch "," pin "," finger ring "," bracelet "," belt fitting "," bead "," ear ring "," strap end "," necklace "," buckle "," buckle pin "," cloak-fastening "," button "," button and loop fastener "," fastening "," hooked tag "," pendant "," amulet case "," comb "," stud "," shoe "," toggle "," pennanular ring "," torc "," thor's hammer "," cross-pendant "," bell "," girdle hanger "," amulet "," arm band "," armlet "," badge "," baldric "," belt "," belt attachment "," belt plate "," belt slide "," chatelaine "," clothes fastener "," clothing accessory "," clothing tag "," diadem "," dress accessory "," dress and personal accessories "," dress component "," dress fastener (dress) "," dress fastener (unknown) "," dress fitting "," clasp "," fastener "," hairpin "," intaglio "," jewellery "," jewellery fitting "," lunula "," medallion "," pectoral "," personal accessory "," personal ornament "," religious personal accessory "," sleeve clasp "," spangle "," wrist band "," wrist clasp "," gemstone "," purse "," strap-end "," strapend "])
	tempstr = "PD"
	for x in simple_set:
		if x in input and "linch pin" not in input and "harness pendant" not in input:
			simplelist.append(tempstr)
	if input == " ring ":
		tempstr = "PD"
		simplelist.append(tempstr)
	simple_set.add("ring")
	if generate == 'Y':
		set_list = list(simple_set)
		set_list.sort()
		f3.write(tempstr + ':\n\n')
		for i in set_list:
			f3.write(i.lstrip().rstrip() + '\n')
		f3.write('\n\n')
	
	# Personal toilet items
	simple_set = set([" ligula"," cosmetic spoon "," nail cleaner "," cosmetic mortar "," cosmetic pestle "," tweezers "," toilet article "," mirror "," cosmetic set "," comb "," cosmetic article "," cosmetic implement "," cosmetic tool "," dental implement "," ear scoop "," manicure implement "," manicure set "," personal grooming and hygiene item "," razor "," scoop "," strigil "," toilet implement "," tooth pick "," tweezer "," twezzers "])
	tempstr = "PT"
	for x in simple_set:
		if x in input:
			simplelist.append(tempstr)
	if generate == 'Y':
		set_list = list(simple_set)
		set_list.sort()
		f3.write(tempstr + ':\n\n')
		for i in set_list:
			f3.write(i.lstrip().rstrip() + '\n')
		f3.write('\n\n')
	
	# Domestic items
	simple_set = set([" brazier "," bell "," candle holder "," tripod "," lamp hanger "," lamp hook "," lamp "," hanging bowl "," aquamanile "," bucket "," candelabrum "," candlestick "," cauldron "," box "," casket "," chair "," container "," furniture "," heating and lighting "," lantern "," storage container "," toy "])
	tempstr = "DI"
	for x in simple_set: 
		if x in input and "kiln furniture" not in input and "seal box" not in input and " food " not in input:
			simplelist.append(tempstr)
	if generate == 'Y':
		set_list = list(simple_set)
		set_list.sort()
		f3.write(tempstr + ':\n\n')
		for i in set_list:
			f3.write(i.lstrip().rstrip() + '\n')
		f3.write('\n\n')
	
	# Cooking / eating / drinking equipment
	simple_set = set([" quernstone "," pot boiler "," pitcher "," ladle "," mortarium "," spoon "," vessel "," knife "," fork "," amphora "," beaker "," bottle "," bowl "," colander "," cup "," dish "," drinking horn "," flagon "," flask "," food and drink serving container "," food and liquid storage container "," food gathering and preparation container "," food preparation container "," food serving container "," frying pan "," goblet "," jar "," jug "," pan "," plate "," platter "," saucepan "," sieve "," skillet "," spatula "," spigot "," strainer "," tankard "," trivet "," mortar "," pestle "," millstone "])
	tempstr = "FD"
	for x in simple_set: 
		if x in input and "cosmetic" not in input and "belt plate" not in input and "plate brooch" not in input:
			simplelist.append(tempstr)
	if generate == 'Y':
		set_list = list(simple_set)
		set_list.sort()
		f3.write(tempstr + ':\n\n')
		for i in set_list:
			f3.write(i.lstrip().rstrip() + '\n')
		f3.write('\n\n')
	
	# Locking devices
	simple_set = set([" key "," latchlifter "," padlock "," lock-plate "," bolt (lock) "," catch "," escutcheon "," hasp "," lock "," lock bar "," lock bolt "," lock fitting "," locking mechanism "])
	tempstr = "LD"
	for x in simple_set:
		if x in input:
			simplelist.append(tempstr)
	if generate == 'Y':
		set_list = list(simple_set)
		set_list.sort()
		f3.write(tempstr + ':\n\n')
		for i in set_list:
			f3.write(i.lstrip().rstrip() + '\n')
		f3.write('\n\n')
	
	# Tools
	simple_set = set([" spokeshave "," saw "," pitchfork "," plane "," pick "," mallet "," hoe "," harrow "," file "," crowbar "," anvil "," mortarium "," chisel "," dividers "," hook "," bucket handle "," bucket band "," shears "," ferrule "," tools and equipment "," hammer "," punch "," awl "," rake "," ox-goad "," peg "," steelyard "," steelyard weight "," weighing scale "," weight "," needle "," cleaver "," scraper "," axe "," socketed axehead "," axehead "," knife "," burin "," blade "," ard "," scythe "," rubber "," hammerstone "," rotary quern "," quern "," spud "," weaving implement "," gouge "," loomweight "," spindle whorl "," palstave "," whetstone "," potters tool "," mortar "," pestle "," adze "," auger "," bodkin "," borer "," burnisher "," drill bit "," engraving tool "," graver "," grindstone "," hone "," igniting accessory "," lever "," linen smoother "," millstone "," muller "," net sinker "," plough "," plumb bob "," probe "," pulley "," sickle "," smoothing equipment "," spade "," thimble "," weaving batten "," weft beater "," workbox "," collar "])
	tempstr = "TO"
	for x in simple_set: 
		if x in input and "lamp hook" not in input and "thor's hammer" not in input and "cosmetic" not in input:
			simplelist.append(tempstr)
	if generate == 'Y':
		set_list = list(simple_set)
		set_list.sort()
		f3.write(tempstr + ':\n\n')
		for i in set_list:
			f3.write(i.lstrip().rstrip() + '\n')
		f3.write('\n\n')
	
	# Production material
	simple_set = set([" furnace lining "," bloom ","manufacturing"," kiln lining "," crucible "," wasters "," ingot "," coin die "," metal working debris "," weight "," balance "," trial piece "," metalworking waste "," slag "," briquetage "," cast waste "," casting gate "," casting waste "," clamp "," glass working debris "," industrial by product "," jeweller's test piece "," kiln furniture "," kiln waste "," manufacture and processing "," manufacture debris "," mould "," potters stamp "," rivet "," spill "," stamp "," tack "," textile equipment "," washer "," waste "," wire "])
	tempstr = "PM"
	for x in simple_set: 
		if x in input and "steelyard weight" not in input:
			simplelist.append(tempstr)
	if generate == 'Y':
		set_list = list(simple_set)
		set_list.sort()
		f3.write(tempstr + ':\n\n')
		for i in set_list:
			f3.write(i.lstrip().rstrip() + '\n')
		f3.write('\n\n')
	
	# WEAPONS!!!!  WOOP!!!
	simple_set = set([" javelin "," bow (weapon) "," halberd "," battleaxe "," bow strengthener "," spearhead "," scabbard "," sword "," scabbard fitting "," catapult "," dolabra sheath "," bolthead "," lance "," pilum "," caltrop "," weapon "," arrowhead "," shield "," knife "," axe "," axehead "," arrow "," baldric "," ballista ball "," ballista bolt "," chape "," chape object "," dagger "," dagger frog "," dagger hilt "," dirk "," mace "," pommel "," pommel cap "," projectile "," shot "," sling shot "," socketed spear "," spear "," spear butt "," seax "," rapier "])
	tempstr = "WN"
	for x in simple_set: 
		if x in input:
			simplelist.append(tempstr)
	if generate == 'Y':
		set_list = list(simple_set)
		set_list.sort()
		f3.write(tempstr + ':\n\n')
		for i in set_list:
			f3.write(i.lstrip().rstrip() + '\n')
		f3.write('\n\n')
	
	# Writing equipment
	simple_set = set([" seal box "," stylus "," stylus case "," book fitting "," seal "," seal matrix "," tablet "," lead tablet "," aestel "])
	tempstr = "WE"
	for x in simple_set:
		if x in input:
			simplelist.append(tempstr)
	if generate == 'Y':
		set_list = list(simple_set)
		set_list.sort()
		f3.write(tempstr + ':\n\n')
		for i in set_list:
			f3.write(i.lstrip().rstrip() + '\n')
		f3.write('\n\n')
	
	# Representational objects
	simple_set = set([" celtic head "," anthropomorphic "," statuette "," statue "," figurine "," miniature object "," bust "," figurehead "," sculpture "])
	tempstr = "FO"
	for x in simple_set: 
		if x in input:
			simplelist.append(tempstr)
	if generate == 'Y':
		set_list = list(simple_set)
		set_list.sort()
		f3.write(tempstr + ':\n\n')
		for i in set_list:
			f3.write(i.lstrip().rstrip() + '\n')
		f3.write('\n\n')
	
	# Horse equipment
	simple_set = set([" strap mount "," horse bit "," bridle bit "," bridle fitting "," harness fitting "," cart fitting "," terret "," linch pin "," strap fitting "," strap union "," prick spur "," stirrup "," hipposandal "," bell "," harness pendant "," bridle "," harness "," harness link "," horse harness "," horse trapping "," horseshoe "," spur "," strap distributor "," swivel ", " stirrup-strap ", " strap slide "])
	tempstr = "HE"
	for x in simple_set: 
		if x in input:
			simplelist.append(tempstr)
	if generate == 'Y':
		set_list = list(simple_set)
		set_list.sort()
		f3.write(tempstr + ':\n\n')
		for i in set_list:
			f3.write(i.lstrip().rstrip() + '\n')
		f3.write('\n\n')
	
	# Military (non weapons)
	simple_set = set([" centurial stone "," helmet "," lorica segment "," cuirass "," apron-mount "," arm guard "," armour "," artillery mechanism "," cheek piece "," cheekpiece "," military standard ", " tie ring "])
	tempstr = "MI"
	for x in simple_set: 
		if x in input:
			simplelist.append(tempstr)
	if generate == 'Y':
		set_list = list(simple_set)
		set_list.sort()
		f3.write(tempstr + ':\n\n')
		for i in set_list:
			f3.write(i.lstrip().rstrip() + '\n')
		f3.write('\n\n')
	
	# Gaming equipment
	simple_set = set([" gaming chip "," die "," gaming counter "," gaming piece "," counter "," gaming board "," token "])
	tempstr = "GE"
	for x in simple_set: 
		if x in input and 'coin die' not in input:
			simplelist.append(tempstr)
	if generate == 'Y':
		set_list = list(simple_set)
		set_list.sort()
		f3.write(tempstr + ':\n\n')
		for i in set_list:
			f3.write(i.lstrip().rstrip() + '\n')
		f3.write('\n\n')
	
	# Fixtures and fittings
	simple_set = set(["fixture","fitting"," cleat "," hook "," stud "," furniture fitting "," chest fitting "," strip "," terminal "," hinge "," plaque  "," chain "," junction loop "," box fitting "," box knob "," bracket "," catch "," clasp "," clip "," disc "," door fitting "," finial "," fitting(s) "," fixture(s) and fitting(s) "," foot "," stand "," split spike loop "])
	tempstr = "FF"
	for x in simple_set: 
		if x in input and "sleeve clasp" not in input and "wrist clasp" not in input and "lamp hook" not in input and "belt fitting" not in input and "harness fitting" not in input and "scabbard fitting" not in input and "bridle fitting" not in input and "book fitting" not in input and "jewellery fitting" not in input and "dress fitting" not in input and "strap fitting" not in input and "cart fitting" not in input and "sword fitting" not in input:
			simplelist.append(tempstr)
	if generate == 'Y':
		set_list = list(simple_set)
		set_list.sort()
		f3.write(tempstr + ':\n\n')
		for i in set_list:
			f3.write(i.lstrip().rstrip() + '\n')
		f3.write('\n\n')
	
	# Medical
	simple_set = set([" lancet "," medical implement "," forceps "," phial "," scalpel "," surgical instrument "])
	tempstr = "ME"
	for x in simple_set: 
		if x in input:
			simplelist.append(tempstr)
	if generate == 'Y':
		set_list = list(simple_set)
		set_list.sort()
		f3.write(tempstr + ':\n\n')
		for i in set_list:
			f3.write(i.lstrip().rstrip() + '\n')
		f3.write('\n\n')
	
	# Specific votive / religious
	simple_set = set([" lachrymatory "," incense burner "," incense holder "," ceremonial object "," miniature object "," caduceus "," censer "," \'votive\' plaque "," urn "," votive model "," curse tablet "," divinational object "," grave assemblage "," thor's hammer "," cross-pendant "," altar "," bull "," bulla "," cross "," cross staff "," crucifix "," crystal ball "," font "," memorial stone "," phallera "," phallic object "," religion or ritual "," religious personal accessory "," reliquary "," sceptre "," lead tablet "," grave assemblages "," grave contents "])
	tempstr = "VR"
	for x in simple_set: 
		if x in input:
			simplelist.append(tempstr)
	if generate == 'Y':
		set_list = list(simple_set)
		set_list.sort()
		f3.write(tempstr + ':\n\n')
		for i in set_list:
			f3.write(i.lstrip().rstrip() + '\n')
		f3.write('\n\n')
	
	# Sherds etc.
	simple_set = set([" sherd "," sherds "," sherd(s) "," vessel "," pottery "," potsherd "," potsherds "," potsherd(s) "])
	tempstr = "SH"
	for x in simple_set: 
		if x in input:
			simplelist.append(tempstr)
	if generate == 'Y':
		set_list = list(simple_set)
		set_list.sort()
		f3.write(tempstr + ':\n\n')
		for i in set_list:
			f3.write(i.lstrip().rstrip() + '\n')
		f3.write('\n\n')
		
	# Hoards
	simple_set = set([" hoard "])
	tempstr = "HO"
	for x in simple_set: 
		if x in input:
			simplelist.append(tempstr)
	if generate == 'Y':
		set_list = list(simple_set)
		set_list.sort()
		f3.write(tempstr + ':\n\n')
		for i in set_list:
			f3.write(i.lstrip().rstrip() + '\n')
		f3.write('\n\n')
			
	# Anchors
	simple_set = set([" anchor "," anchors "])
	tempstr = "AN"
	for x in simple_set: 
		if x in input:
			simplelist.append(tempstr)
	if generate == 'Y':
		set_list = list(simple_set)
		set_list.sort()
		f3.write(tempstr + ':\n\n')
		for i in set_list:
			f3.write(i.lstrip().rstrip() + '\n')
	
	if generate == 'Y':
		f3.close()
	
	if len(simplelist) == 0:
		simplelist.append("UN")
	simpleset = set(simplelist)
	simplelist = list(simpleset)
	simplelist.sort()
	return simplelist