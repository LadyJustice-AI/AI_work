
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

Important note : The file, in the path file 1994\asd19940635.xml , was removed because in the original data, it was empty so, to avoid errors, it was better to remove it.

## Generating a CSV

If you want to generate CSV, you need to launch the Processing.py file and uncomment the part, in the main function, that you want to generate. 

You can see some examples of the generation for just one year (The file *2015_output.csv* and *2016_output.csv*)