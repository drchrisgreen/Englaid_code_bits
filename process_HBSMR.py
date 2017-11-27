import xml.etree.ElementTree as ET
import csv
import glob
from copy import deepcopy as dc

def bulk_process(folder, start_eid, her_name):
	searchstr = folder + '*.xml'
	
	cur_eid = dc(start_eid)
	
	for filename in glob.glob(searchstr):
		print filename
		next = process(filename, cur_eid, her_name)
		cur_eid = dc(next) + 1

def process(filename, start_eid, her_name):
	
	eid = int(start_eid)
	
	pos = filename.rfind('.')
	filename_stub = filename[:pos]
	
	f1 = open(filename_stub+'_metadata.csv','wb')
	f2 = open(filename_stub+'_admins.csv','wb')
	f3 = open(filename_stub+'_bibliography.csv','wb')
	f4 = open(filename_stub+'_events.csv','wb')
	f5 = open(filename_stub+'_finds.csv','wb')
	f6 = open(filename_stub+'_identifiers.csv','wb')
	f7 = open(filename_stub+'_location.csv','wb')
	f8 = open(filename_stub+'_montypes.csv','wb')
	f9 = open(filename_stub+'_monument.csv','wb')
	f10 = open(filename_stub+'_related.csv','wb')
	f11 = open(filename_stub+'_statuses.csv','wb')
	
	w_eng = csv.writer(f1)
	w_adm = csv.writer(f2)
	w_bib = csv.writer(f3)
	w_eve = csv.writer(f4)
	w_fin = csv.writer(f5)
	w_ide = csv.writer(f6)
	w_loc = csv.writer(f7)
	w_mty = csv.writer(f8)
	w_mon = csv.writer(f9)
	w_rel = csv.writer(f10)
	w_sta = csv.writer(f11)
	
	h_eng = ['eid','source','her_ref','format','person','accessed','case_study']
	h_adm = ['eid','admin_type','admin_name']
	h_bib = ['eid','sourceID','source_type','source_author','source_date','source_title','source_description']
	h_eve = ['eid','eventID','event_name','event_type','event_description','event_start','event_end']
	h_fin = ['eid','findID','find_type','find_quantity','find_from','find_to','find_description','find_materials']
	h_ide = ['eid','id_type','id_value']
	h_loc = ['eid','osgb','easting','northing','precision']
	h_mty = ['eid','mon_term','mon_from','from_confidence','mon_to','to_confidence','mon_evidence','mon_period','sd_date','sd_stdev','sd_method']
	h_mon = ['eid','name','broad_type','summary','description']
	h_rel = ['eid','related_eid','related_ID','related_name','relation_type']
	h_sta = ['eid','status_type','status_value']
	
	w_eng.writerow(h_eng)
	w_adm.writerow(h_adm)
	w_bib.writerow(h_bib)
	w_eve.writerow(h_eve)
	w_fin.writerow(h_fin)
	w_ide.writerow(h_ide)
	w_loc.writerow(h_loc)
	w_mty.writerow(h_mty)
	w_mon.writerow(h_mon)
	w_rel.writerow(h_rel)
	w_sta.writerow(h_sta)
	
	tree = ET.parse(filename)
	root = tree.getroot()
	
	for mon in root:
		r_eng = [eid,her_name,'','','','','']
		w_eng.writerow(r_eng)
		r_mon = [eid,'','','','']
		for sub_tag in mon:
			if sub_tag.tag == 'monumentName':
				r_mon[1] = sub_tag.text
			if sub_tag.tag == 'type':
				r_mon[2] = sub_tag.text
			if sub_tag.tag == 'summary':
				r_mon[3] = sub_tag.text
			if sub_tag.tag == 'description':
				r_mon[4] = sub_tag.text
			if sub_tag.tag == 'identifiers':
				for id in sub_tag:
					r_ide = [eid,id.tag,id.text]
					w_ide.writerow(r_ide)
			if sub_tag.tag == 'location':
				for loc in sub_tag:
					if loc.tag == 'osCoordinates':
						r_loc = [eid,'','','','']
						for sub_loc in loc:
							if sub_loc.tag == 'easting':
								r_loc[2] = sub_loc.text
							if sub_loc.tag == 'northing':
								r_loc[3] = sub_loc.text
							if sub_loc.tag == 'precision':
								r_loc[4] = sub_loc.text
						w_loc.writerow(r_loc)
					if loc.tag == 'adminArea':
						r_adm = [eid,'','']
						for sub_loc in loc:
							if sub_loc.tag == 'type':
								r_adm[1] = sub_loc.text
							if sub_loc.tag == 'name':
								r_adm[2] = sub_loc.text
						inum = 0
						for i in r_adm:
							try:
								r_adm[inum] = i.encode('utf-8')
							except AttributeError:
								pass
							inum += 1
						w_adm.writerow(r_adm)
			if sub_tag.tag == 'statuses':
				for status in sub_tag:
					r_sta = [eid,'','']
					for sta_sub in status:
						if sta_sub.tag == 'statusType':
							r_sta[1] = sta_sub.text
						if sta_sub.tag == 'statusValue':
							r_sta[2] = sta_sub.text
					w_sta.writerow(r_sta)
			if sub_tag.tag == 'monumentTypes':
				for mon in sub_tag:
					r_mty = [eid,'','','','','','','','','','']
					for mon_sub in mon:
						if mon_sub.tag == 'term':
							r_mty[1] = mon_sub.text
						if mon_sub.tag == 'from':
							r_mty[2] = mon_sub.text
						if mon_sub.tag == 'to':
							r_mty[4] = mon_sub.text
						if mon_sub.tag == 'evidence':
							r_mty[6] = mon_sub.text
						if mon_sub.tag =='scientificDating':
							for scid in mon_sub:
								if scid.tag == 'scientificDate':
									if r_mty[8] == '':
										r_mty[8] = str(scid.text)
									else:
										r_mty[8] += '; ' + str(scid.text)
								if scid.tag == 'standardDeviation':
									if r_mty[9] == '':
										r_mty[9] = str(scid.text)
									else:
										r_mty[9] += '; ' + str(scid.text)
								if scid.tag == 'method':
									if r_mty[10] == '':
										r_mty[10] = scid.text
									else:
										r_mty[10] += '; ' + scid.text
					w_mty.writerow(r_mty)
			if sub_tag.tag == 'events':
				for event in sub_tag:
					r_eve = [eid,'','','','','','']
					for sub_eve in event:
						if sub_eve.tag == 'eventID':
							r_eve[1] = sub_eve.text
						if sub_eve.tag == 'eventName':
							r_eve[2] = sub_eve.text
						if sub_eve.tag == 'eventType':
							r_eve[3] = sub_eve.text
						if sub_eve.tag == 'eventDescription':
							r_eve[4] = sub_eve.text
						if sub_eve.tag == 'startDate':
							r_eve[5] = sub_eve.text
						if sub_eve.tag == 'endDate':
							r_eve[6] = sub_eve.text
					inum = 0
					for i in r_eve:
						try:
							r_eve[inum] = i.encode('utf-8')
						except AttributeError:
							pass
						inum += 1
					w_eve.writerow(r_eve)
			if sub_tag.tag == 'finds':
				for find in sub_tag:
					r_fin = [eid,'','','','','','','']
					for sub_fin in find:
						if sub_fin.tag == 'findID':
							r_fin[1] = sub_fin.text
						if sub_fin.tag == 'findType':
							r_fin[2] = sub_fin.text
						if sub_fin.tag == 'quantity':
							r_fin[3] = sub_fin.text
						if sub_fin.tag == 'dateFrom':
							r_fin[4] = sub_fin.text
						if sub_fin.tag == 'dateTo':
							r_fin[5] = sub_fin.text
						if sub_fin.tag == 'description':
							r_fin[6] = sub_fin.text
						if sub_fin.tag == 'findMaterials':
							for mat in sub_fin:
								if mat.tag == 'material':
									if r_fin[7] == '':
										r_fin[7] = mat.text
									else:
										r_fin[7] += '; ' + mat.text
					inum = 0
					for i in r_fin:
						try:
							r_fin[inum] = i.encode('utf-8')
						except AttributeError:
							pass
						inum += 1
					w_fin.writerow(r_fin)
			if sub_tag.tag == 'bibliography':
				for source in sub_tag:
					r_bib = [eid,'','','','','','']
					for sub_bib in source:
						if sub_bib.tag == 'sourceID':
							r_bib[1] = sub_bib.text
						if sub_bib.tag == 'sourceType':
							r_bib[2] = sub_bib.text
						if sub_bib.tag == 'author':
							r_bib[3] = sub_bib.text
						if sub_bib.tag == 'date':
							r_bib[4] = sub_bib.text
						if sub_bib.tag == 'title':
							r_bib[5] = sub_bib.text
					inum = 0
					for i in r_bib:
						try:
							r_bib[inum] = i.encode('utf-8')
						except AttributeError:
							pass
						inum += 1
					w_bib.writerow(r_bib)
			if sub_tag.tag == 'relatedMonuments':
				for relmon in sub_tag:
					r_rel = [eid,'','','','']
					for sub_rel in relmon:
						if sub_rel.tag == 'relatedMonUID':
							r_rel[2] = sub_rel.text
						if sub_rel.tag == 'relatedMonName':
							r_rel[3] = sub_rel.text
						if sub_rel.tag == 'relationshipType':
							r_rel[4] = sub_rel.text
					inum = 0
					for i in r_rel:
						try:
							r_rel[inum] = i.encode('utf-8')
						except AttributeError:
							pass
						inum += 1
					w_rel.writerow(r_rel)
		inum = 0
		for i in r_mon:
			try:
				r_mon[inum] = i.encode('utf-8')
			except AttributeError:
				pass
			inum += 1
		w_mon.writerow(r_mon)
		eid += 1
	
	f1.close()
	f2.close()
	f3.close()
	f4.close()
	f5.close()
	f6.close()
	f7.close()
	f8.close()
	f9.close()
	f10.close()
	f11.close()
	
	return eid