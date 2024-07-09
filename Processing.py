import xml.etree.ElementTree as ET
import os
import csv
import pandas as pd

def create_csv(output_csv):
	"""Create a csv with specified column name
	Arguments : 
	output_csv : The name of the new csv, must be a str
	"""
	with open(output_csv, mode='a', newline='', encoding='utf-8') as file:
		writer = csv.writer(file)

		writer.writerow(['Document Type', 'Eduskunta ID', 'Date', 'Law Title', 'Section ID', 'Section Title', 'Section Content', 'Position_first', 'Name_first','Position_second','Name_second'])


def remove_newlines(text_list):
  return [[s.replace('\n', '') if s else s for s in sublist] for sublist in text_list]

# Fonction pour diviser le texte autour de la virgule centrale
# Fonction pour diviser le texte autour de la première virgule
def split_text_around_comma(text):
    parts = text.split(', ', 1)  # Diviser en deux parties autour de la première virgule
    return parts

def collect_text(tag_name, lst_of_content):
	#Collect the text between a precise tag
	for momentti in tag_name:
						if momentti is not None and momentti.text is not None:
							lst_of_content.append(momentti.text.strip())
		 
def show_xml_info(xml_file, output_csv):
	"""Load and Analysze the XML files
	Arguments : 
	output_csv : The csv that have been previously created, must be str
	xml_file : The xml file  with the data, we want to extract
	"""

	tree = ET.parse(xml_file)
	root = tree.getroot()
	namespaces = {
			'vah': 'http://www.vn.fi/skeemat/vahvistettavalaki/2010/04/27',
			'sdk': 'http://www.finlex.fi/skeemat/edita/sdk/2010/04/27',
			'saa': 'http://www.vn.fi/skeemat/saadoskooste/2010/04/27',
			'saa1': 'http://www.vn.fi/skeemat/saadoselementit/2010/04/27',
			'met': 'http://www.vn.fi/skeemat/metatietokooste/2010/04/27',
			'met1': 'http://www.vn.fi/skeemat/metatietoelementit/2010/04/27',
			'asi': 'http://www.vn.fi/skeemat/asiakirjakooste/2010/04/27',
			'asi1': 'http://www.vn.fi/skeemat/asiakirjaelementit/2010/04/27',
			'org': 'http://www.vn.fi/skeemat/organisaatiokooste/2010/02/15',
			'org1': 'http://www.vn.fi/skeemat/organisaatioelementit/2010/02/15',
			'tau': 'http://www.vn.fi/skeemat/taulukkokooste/2010/04/27',
			'sis': 'http://www.vn.fi/skeemat/sisaltokooste/2010/04/27',
			'sis1': 'http://www.vn.fi/skeemat/sisaltoelementit/2010/04/27'
		}
	#Initialisation of the variables
	document_type_text = eduskunta_id_text = date_id_text = law_title_text = 'N/A'
	section_id = section_title_text = section_content_text = 'N/A'
	position_text = name_text = 'N/A'
	
	with open(output_csv, mode='a', newline='', encoding='utf-8') as file:
		writer = csv.writer(file)
		
		#Extract the identifications informations
		identification = root.find('asi:IdentifiointiOsa', namespaces)
		if identification is not None:
			document_type = identification.find('met1:AsiakirjatyyppiNimi', namespaces)
			if document_type is not None:
					document_type_text = document_type.text
					print(f'Document Type: {document_type_text}')
			
			eduskunta_id = identification.find('asi:EduskuntaTunniste/asi1:AsiakirjaNroTeksti', namespaces)
			if eduskunta_id is not None:
					eduskunta_id_text = eduskunta_id.text
					print(f'Eduskunta ID: {eduskunta_id_text}')
			#for the date
			date_id = identification.find('asi:EduskuntaTunniste/asi1:ValtiopaivavuosiTeksti', namespaces)
			if date_id is not None:
				date_id_text = date_id.text
				print(f'Date : {date_id_text}')
				
		# Extract the name of the text Law
		saados = root.find('saa:SaadosOsa/saa:Saados', namespaces)
		lst_of_signatories = []
		if saados is not None:
				law_title = saados.find('saa:SaadosNimeke/saa:SaadosNimekeKooste', namespaces)
				law_title_text = law_title.text if law_title is not None else 'N/A'
				print(f'Law Title: {law_title_text}')

				#extract the signatories of the document
				signatures = root.find('asi:AllekirjoitusOsa', namespaces)
				if signatures is not None:
					for signer in signatures.findall('asi:Allekirjoittaja', namespaces):
						position = signer.find('org:Henkilo/org1:AsemaTeksti', namespaces)
						name = signer.find('org:Henkilo/org1:SukuNimi', namespaces)
						
						position_text = position.text if position is not None else 'N/A'
						name_text = name.text if name is not None else 'N/A'

						lst_of_signatories.append([position_text,name_text])
						lst_of_signatories = remove_newlines(lst_of_signatories)
						#The list will be like this  [[postion_first, name_first], [position_second,name_second]]
						print(f'{position_text}: {name_text}')
				else:
					lst_of_signatories = [['N/A','N/A'],['N/A','N/A']]
				
				#Extract the section of the law
				sections = saados.findall('saa:Pykalisto/saa:Pykala', namespaces)
				if sections ==[]:
					sections = saados.findall('saa:Pykalisto/saa:Luku/saa:Pykala', namespaces)
				#print(sections)
				for section in sections:
					#Search all the information about a section
		
					section_id = section.get('{http://www.vn.fi/skeemat/saadoselementit/2010/04/27}identifiointiTunnus')
					section_title = section.find('saa:SaadosOtsikkoKooste', namespaces)
					section_title_text = section_title.text if section_title is not None else 'N/A'
				
					#Concat the content of the tag MomenttiKooste
					section_content_parts = []
					momentti_kooste = section.findall('saa:MomenttiKooste', namespaces)
					collect_text(momentti_kooste, section_content_parts)
					
					khodat_momentti = section.findall('saa:KohdatMomentti', namespaces)
					for division in khodat_momentti:
						momentti_johdanto_kooste = division.findall('saa:MomenttiJohdantoKooste', namespaces)
						collect_text(momentti_johdanto_kooste , section_content_parts)
					
						momentti_kohta_kooste = division.findall('saa:MomenttiKohtaKooste', namespaces)
						for momentti in momentti_kohta_kooste:
							if momentti is not None and momentti.text is not None:
								print(f'{momentti.text} Ceci est un texte')
								text = momentti.text
								section_content_parts.append(str(text).strip())	
								print(section_content_parts)
						#get the data in Luku Tag
				
										# Extract sections and chapters
					for luku in saados.findall('saa:Luku', namespaces):
							luku_id = luku.get('{http://www.vn.fi/skeemat/saadoselementit/2010/04/27}identifiointiTunnus', 'N/A')
							luku_title = luku.findtext('saa:SaadosOtsikkoKooste', default='N/A', namespaces=namespaces)

							for section in luku.findall('saa:Pykala', namespaces):
									section_id = section.get('{http://www.vn.fi/skeemat/saadoselementit/2010/04/27}identifiointiTunnus', 'N/A')
									section_title_text = section.findtext('saa:SaadosOtsikkoKooste', default='N/A', namespaces=namespaces)
									
									# Concat the content of the tag MomenttiKooste
									#section_content_parts = []
									momentti_kooste = section.findall('saa:MomenttiKooste', namespaces)
									collect_text(momentti_kooste, section_content_parts)
									#Test print
									print(chapter_content_parts, "zehtgequirghvsudgfhestuhgbudfghvdufhbqiufdhg")	   
					section_content_text = ' '.join(section_content_parts) if section_content_parts else 'N/A'
					print(type(section_content_text))
					print(section_content_text)
					section_content_text =  section_content_text.replace(";", "")
					#Sometimes there is no section title, so we juste print the id and the text
					if section_title_text == 'N/A':
						print(f'{section_id}: {section_content_text}')
					else:
						print(f'{section_id}: {section_title_text} - {section_content_text}')
					print([document_type_text, eduskunta_id_text, date_id_text, law_title_text, section_id, section_title_text, section_content_text, lst_of_signatories[0][0], lst_of_signatories[0][1],lst_of_signatories[1][0],lst_of_signatories[1][1]])
					writer.writerow([document_type_text, eduskunta_id_text, date_id_text, law_title_text, section_id, section_title_text, section_content_text, lst_of_signatories[0][0], lst_of_signatories[0][1],lst_of_signatories[1][0],lst_of_signatories[1][1]])
			
		



def main():

	#Part for the creation of a CSV of one particular year data
	
	year_id= '2015'
	count = 0 
	#in case, we want to debug
	create_csv(year_id+"_output.csv")
	for file in os.listdir(year_id):
		#if count < 5: #debug line to just stop at the fifth XML files
		file_path = os.path.join(year_id,file)
		print(file_path)
		show_xml_info(file_path, year_id+"_output.csv")
			#count+=1 
		
	
	#Part for the creation of a data csv that contain all the data between 1917 and 2023
	
	"""create_csv("output.csv")
	for number in range(1918,2024):
		print(number)
		number_str = str(number)
		for file in os.listdir(number_str):
			file_path = os.path.join(number_str,file)
			print(file_path)
			show_xml_info(file_path, "output.csv")
	
	"""
	show_xml_info("2015/asd20150052.xml", "2015_52_output.csv")

	
#MAIN PROGRAM

main()

#df = pd.read_csv('output.csv', low_memory=False)