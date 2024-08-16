import requests
from bs4 import BeautifulSoup
import csv
import re

# Dict with the specifities of CELEXID (See the PDF with the explanation of how to interpret it, Searching_EURLEX\eur-lex-celex-infographic-A3.pdf)
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
	""" 
	Argument :

	OJ : must be str, It's the OJ identifier
	"""

	url = "https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=OJ:L:2022:152:FULL"+OJ
	#alternatives_url = "http://publications.europa.eu/resource/celex/"+CELEX_ID
	# Send a request to the page
	response = requests.get(url)

	#check if the request works 
	response.raise_for_status() 
	

	# Parsing the HTML content
	soup = BeautifulSoup(response.content, 'html.parser')

	# Extract the directive of the text
	text = soup.get_text()

	# Remove the unnecessary spaces
	cleaned_text = ' '.join(text.split())


	# print  the cleaned text
	#print(cleaned_text)
	#Print the text without processing it
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

	# Parsing the content HTML
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

		print(f"Associated Text: {text}\nLink: https://eur-lex.europa.eu{link}\n")
		#print("keep")


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
	paragraphs = soup.find_all('p', class_="oj-note")

	# This line is for debugging and it shows the number of paragraph 
	print(f"Number of paragraphs in the extract: {len(paragraphs)}")
	for i, p in enumerate(paragraphs, 1):
			print(f"Paragraph {i}: {p}")

	#-------------------THIS PART DOESN'T WORK WELL-------------------------------------

	# Filtering and extracting the text of the paragraphs that contain the directives mention 
	directive_pattern = re.compile(r'Directive \((?:EU|EC|EEC|Euratom)\) \d{4}/\d{2,4}|Regulation \((?:EU|EC|EEC|Euratom)\) No \d{2,4}/\d{2,4}')
	#directive_pattern = re.compile(r'(Directive /(?:EU|EC|EEC|Euratom)\d{4}/\d{2,4}/(?:EU|EC|EEC|Euratom)|Regulation \((?:EU|EC|EEC|Euratom)\) \d{4}/\d{2,4})')
		
	references = []
	test = "(7)Including the assessment referred to in Article 15 (7) of Directive (EU) 2019/2001."    

	count = 0 
	for p in paragraphs:
		text = p.get_text(strip=True)

		# Debug: Print the text of the paragraph
		print(f"Paragraph text: {text}")
		print(type(text))
		if "Directive" in text: 
			count+=1
		if directive_pattern.search(text):

			print(directive_pattern.search(text))
			match = directive_pattern.search(text)
			if match:
				directive_text = match.group(0)
				print(f"{directive_text} TEXT CROP")
				references.append(directive_text)
			
	print(count)
	print("Finding References:")
	for ref in references:
		print(f"Associated Texts: {ref}\n")


def test():
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

	# Debug: Assurez-vous que les paragraphes sont bien extraits
	print(f"Nombre de paragraphes extraits : {len(paragraphs)}")
	for i, p in enumerate(paragraphs, 1):
			print(f"Paragraphe {i}: {p}")

	# Filtrer et extraire les textes des paragraphes contenant des mentions de directives
	directive_pattern = re.compile(r'Directive \((?:EU|EC|EEC|Euratom)\) \d{4}/\d{2,4}|Regulation \((?:EU|EC|EEC|Euratom)\) No \d{2,4}/\d{2,4}')
	#directive_pattern = re.compile(r'(Directive /(?:EU|EC|EEC|Euratom)\d{4}/\d{2,4}/(?:EU|EC|EEC|Euratom)|Regulation \((?:EU|EC|EEC|Euratom)\) \d{4}/\d{2,4})')
		
	references = []
	test2 = "(7)Including the assessment referred to in Article 15 (7) of Directive (EU) 2019/2001."      
	test = "(49)Regulation (EU) No 575/2013 of the European Parliament and of the Council of 26 June 2013 on prudential requirements for credit institutions and amending Regulation (EU) No 648/2012 (OJ L 176, 27.6.2013, p. 1)."             
	 
	# Debug: Vérifiez le contenu de la liste des références
	if directive_pattern.search(test):
		references.append(test)
		print(directive_pattern.search(test))
		match = directive_pattern.search(test)
		if match:
			directive_text = match.group(0)
			print(f"{directive_text} TEXT CROP")
			references.append(directive_text)
	print("Références trouvées:")
	for ref in references:
			print(f"Texte associé: {ref}\n")

#MAIN PART 

main()
