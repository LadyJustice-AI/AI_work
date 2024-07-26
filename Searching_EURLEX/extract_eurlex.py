import requests
from bs4 import BeautifulSoup
import csv

import re

# Dict with the specifities of CELEXID (See the PDF with the explanation of how to interpret it)
dict_of_sector = {1 : "Treaties", 2: "International agreements",3:"Legislation", 4:"Complementary legislation", 5: "Preparatory acts and working documents", 6:" Case-Law",7 : "National transposition measures", 8 :"References to national case-law", 9: "Parliamentary questions", 0:"Consolidated acts", 'C':"Other documents published in the Official Journal C series", 'E':"EFTA documents"}
dict_of_letter = {'L':"DIrectives", 'R': "Regulation", 'D': "Decisions"}

def open_csv(csv_file):
	"""
	Read a csv from a request on EURLEX
	Return a list with the CELEXID in the CSV
	Argument :
	csv_file : must be a str, it's the ,name of the csv file, you need to read

	"""
	lst_of_CELEXID = []
		
	with open(csv_file, 'r') as file:
			reader = csv.reader(file, delimiter=';')
			for row in reader:                               
					#print(row)
					lst_of_CELEXID.append(row[2])#The index of the column in row can change depending on the parameters of your request on the EURLEX website


	return lst_of_CELEXID

def retrieve_OJ_content(OJ):

	url = "https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=OJ:L:2022:152:FULL"+OJ
	#alternatives_url = "http://publications.europa.eu/resource/celex/"+CELEX_ID
	# Envoyer une requête à la page
	response = requests.get(url)

	response.raise_for_status()  # Vérifier que la requête s'est bien passée

	# Parser le contenu HTML
	soup = BeautifulSoup(response.content, 'html.parser')

	# Extraire le texte de la directive
	text = soup.get_text()

	# Enlever les espaces superflus
	cleaned_text = ' '.join(text.split())

	# Afficher ou traiter le texte nettoyé
	#print(cleaned_text)
	# Afficher ou traiter le texte
	#print(text)

	return soup

def retrieve_CELEX_content(CELEX_ID):
	""" From the CELEXID, retrieve the data of the pages that correspond to this CELEXID
	Return the content with the HTML tag with the BeautifulSoup package
	Argument :

	CELEXID : must be str, It's the CELEXID that correspond to a precise article, see the link in the READ.me
	"""
	url = "https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:"+CELEX_ID
	#alternatives_url = "http://publications.europa.eu/resource/celex/"+CELEX_ID
	#Send a request to the Webpage
	response = requests.get(url)

	response.raise_for_status()  # Check if the request went fine

	# Parsing of the content HTMM
	soup = BeautifulSoup(response.content, 'html.parser')

	# Extract the text of the Directives
	text = soup.get_text()

	#Remove the excess of space
	cleaned_text = ' '.join(text.split())

	# print  the cleaned text
	#print(cleaned_text)
	# Print the text without processing it
	#print(text)

	return soup




def main():

	# Retrieve all the CELEXID of the CSV
	CELEXID = open_csv("Searching_housing_2023_EU.csv")

	print(CELEXID)
	#Store the content associated to the CELEXID that we want
	soup = retrieve_CELEX_content(CELEXID[1])

	# Search all the 'a' tag in the HTML
	references = soup.find_all('a')
	print(references)

	# Extract the useful informations
	texts_associated = []
	for ref in references:
		text = ref.get_text()
		#from the 'a' tag, collect the link in the href attribute
		link = ref['href']
		#Create a list with a tuple that contains the text between the tag and the link
		texts_associated.append((text, link))

	# Print the text and the link
	for text, link in texts_associated:

		#print(f"Associated Text: {text}\nLink: https://eur-lex.europa.eu{link}\n")
		print("keep")


	# Extract the textual references
	"""references = soup.find_all('div')  # This may vary depending on the exact structure of the page

	# Extract the text from the references that we collect previously
	texts_associated = []
	for ref in references:
		paragraphs = ref.find_all('p')
		for p in paragraphs:
			text = p.get_text(strip=True)
			if 'Position of the European Parliament' in text or 'decision of the Council' in text or 'Regulation' in text or '/' in text:
				texts_associated.append(text)"""


	# Extract all the paragraph
	paragraphs = soup.find_all('p', class_= "oj-note")


	directive_pattern = re.compile(r'(Directive \d{4}/\d{2,4}/(?:EU|EC|EEC|Euratom)|Regulation \((?:EU|EC|EEC|Euratom)\) \d{4}/\d{2,4})')
	# Filtrer et extraire les textes des paragraphes contenant des mentions de directives
	references = []
	for p in paragraphs:
		text = p.get_text(strip=True)
		#print(text)
		if directive_pattern.search(text):
			references.append(text)

	# print the associated text
	for ref in references:
		print(f"Texte associé: {ref}\n")
	
	print()
	"""
	for text in texts_associated:
		print(f"Texte associé: {text}\n")"""
	#MAIN PART 

main()