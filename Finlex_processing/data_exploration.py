import os
import csv
import pandas as pd

def detect_word(word, text):
	"""detect a part of a word in a text
	"""
	
	if word in text:
		return True
	return False
def read_csv(csv_file):
	""" Read a csv
	"""
	with open(csv_file,  newline='', encoding='utf-8') as file:
		reader = csv.reader(file)
		print(reader)
		for row in reader:
			print(', '.join(row))
def test():
	pass


def main():

	
	detect_word("asu", "asuyeruhgeskudihgsuirtuhg")
	read_csv("Finlex_processing/2015_output.csv")

main()
