
# Processing the data from Finlex

Last collection date : 21/05/2024

First, all the data in this folder provide from the Finlex website (Semantic Finlex data service developed by the Ministry of Justice, Aalto University and Edita Publishing Ltd at http://data.finlex.fi). 

## Retrieving the document

In this folder, you can find the data from Finlex that have been downloaded by this link https://data.finlex.fi/en/download on the last collection date. 
If you want to collect the data by your own, follow the instructions below : 
When you are on the website, you need to choose *"Original statutes"* just under *"Original XML files as ZIP packages"*. After you can choose between swedish and finnish. Here the XML documents are in **finnish**.

## Exploring the data

You can find one python file.

*Processing.py* 

With Processing.py, you can have the data in a CSV file for any years or just have all the data from the year 1917.

Important note : 
- The file, in the path file 1994\asd19940635.xml , was removed because in the original data, it was empty so, to avoid errors, it was better to remove it.
- The file *1991/asd19911526.xml* and *1991/asd19911594.xml* have been modified with the addition of the date with the same tags of the other files because it wasn't in this specific two files.


## Generating a CSV

If you want to generate CSV, you need to launch the Processing.py file and uncomment the part, in the main function, that you want to generate. 

You can see some examples of the generation for just one year (The file *2015_output.csv* and *2016_output.csv*).

## Some explanation of the structure of one CSV file

Each CSV file will have this header in ordre : 'Document Type', 'Eduskunta ID', 'Date', 'Law Title', 'Section ID', 'Section Title', 'Section Content', 'Position_first', 'Name_first','Position_second','Name_second'. 

You have the "Document Type" that is the same for every lines.

"Eduskunta_ID" is the document number text.

The "date" is just the year of the text.

"Law Title" is the title of the law. It can be undefined, if so it's write as "N/A"

"Section ID", "Section Title", "Section Content" are to describe the specific section of an article with its ID, Title and Content.

'Position_first', 'Name_first','Position_second','Name_second' are to describe the signatories and their positions in the government. In general, they are two that's why it has two name and position.
