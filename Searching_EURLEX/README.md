# AI_work

On this file, we focus on  the collection of the European data from EURLEX  https://eur-lex.europa.eu/homepage.html

## Exemple for one TSV file

### 1) Creation of a TSV file

The TSV file Search results 20240722.tsv is the result of a research on the advanced search system of the EURLEX websites available on this link https://eur-lex.europa.eu/advanced-search-form.html

The parameters are _Domain: All, Date of publication: 2023, Date of publication: 2023, Results containing: Housing In title and text, Search language: English_

### 2) Choose your export settings

When the searching is finish, you can export the legal act that has been found and choose the data that you want to keep in the export settings 
For the "Search results 20240722.tsv" , the parameters are :
_Title, Subtitle, CELEX number, Adopted acts,	Latest consolidated version,	ECLI identifier,	Transposed legal act(s),	Date of document_

![alt text](images/image.png)

Title and Subtitle couldn't be remove to the export.

### 3) Loading the file in a CSV format
After that you have a file in TSV format. In my work, I loaded it with excel and obtain a CSV. I named it with the same name than the TSV file. You can find a screen with the tool, i used below.

<img src="images/first_step_in_excel.png" alt="first excel step" width="750"/>

After that , you need to choose your file in your documents. 
You will have a preview of the data transfer, If the column displays well, you can click on "load".

And it's done.

You can do the same steps to have much data with many different topics.

### Other way

The EURLEX website have others options to collect data. We can use SparQL request but this work didn't use this for now.