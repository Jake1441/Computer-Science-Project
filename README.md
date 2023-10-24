JRE141- COSC480 Project readme

# Output
![[gnuplot_map_export.png | 300]]
![[A_to_C_map_export.png| 200]] ![[A_to_U_map_export.png | 200]] ![[G_to_I_map_export.png | 200]]

> [!Variation 26/05/2023]
> *IMPORTANT*:
> A new program named open-library.py was added. If the document is in error then please accept that open-library.py is now the recommended procedure to run this program.
# The project
This project is designed to read the open-library data set and look for valid VIAF entries by authors, the structure is designed to attempt to not 'throw away' any data, though only database records are kept simulating a level of consistency in redundancy and industry standards.

## Rationale
This is project aimed at giving the user the option to search for titles and display a world map where authors matching a title are located, presenting a bunch of bar graphs so the user can look at the numbers and a total bar graph at the end to show how the data was presented on the world map.

## Installation
all of the files provided are in a zipped file, should you have issues there is a requirements file to install the required python packages.

you can run this file by using:
```
python -m pip install -r requirements.txt
```
do you need to install python?
check this link here https://realpython.com/installing-python/

There are no additional configuration steps required to use python, just install the python interpreter, make sure you use venv,
check this link here https://docs.python.org/3/library/venv.html
Python version and venv example code your exact usage may vary.
```
#check version!
python -V
python -m venv enviroment
source /environment/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

The python details are as follows
1. All the files are under a folder called Codebase
2. The program expects the following structure
```
codebase (Main folder)
├── Data
│   ├── Filtered
│   │   └── invalidData
│   ├── schemata
│   ├── Scraped
│   └── shapefiles
│       └── worldmap
├── fig_export
```
Raw data such as authors.tar would be placed directory inside the Data directory for processing.
you will need to extract these to the directory they are in, if it asks to overwrite files, it is ok to overwrite the files.
The program will re-fetch any necessary information lost as long as the files are where they are required.
## Usage
You can use the following command (no user input is required at this stage)
```
python open-library.py
```
### running the packages step by step
```
python process_data.py
python viaf_xml_parser.py
python read_marc21_countrycodes.py
```
At the end your graphs will be saved under the following folder structure below.
```
codebase (Main folder)
├── fig_export
```
## Demonstration Data
Due to limitations in time, file sizes and speed,
Ideally viaf_xml_parser.py would have been set up to run seamlessly it is safe to ignore all files and just run the final python file, 
```
	python open-library.py
```

## 1. Process_data
The unclean or unprocessed CSV files are placed under Data for the open-library authors.
process_data uses these to clean the data.

## 2. viaf_xml_parser
run viaf_xml_parser.py after process_data.py 

Each set of filtered, valid or invalid CSV file following the beginning lines,
described in process_data.py as 
names_to_call = ["authors", "works", "editions"]
picks up on the valid file names beginning with each word that are CSV files.

Next, viaf_xml_parser.py is run to get the valid information from the files collected and ensure the plotter can perform the required tasks.

the last and file python file is 
## 3. read_marc21_countrycodes.py 
run read_marc21_countrycodes.py last.
this file reads the new xml file created and prepares a worldmap and plot based on the emulation of a search string from a book title.

## issues encountered
both the open-library and VIAF data sets contained information that was not in an acceptable format to python code,
this supposedly originates from dealing with text based strings containing characters python has difficulty in escaping out or interprets as important built in functions such as new lines or @ symbols being read as python decorators.

## data loss
the frequency of data captured was highly unlikely to match the total frequency of data in the original data set, each time the data was iterated through, the loss of more data was apparent as the captured data was supposedly thrown away in an attempt to reduce load on trying to re represent the data appropriately.

## successful outcomes
the model of the program was written with the intent of allowing the user to prompt for author data, during the process of preparing the dataset for reading and the mock world map loading it was quickly discovered the functions were written in such a way that the requirement for a mock unit test surrounding searching for key tiles named "Autism" was trivial. 

The inferred meaning from this is that during the phase of system analysis and design, the intended implementation a user driven program is also relatively trivial from a code re factoring perspective.

# Code map
There are three main python files included, these are
1. 	open-library.py
2.  process_data.py
3.  read_marc21_countrycodes.py
4.  viaf_xml_parser.py
# open-library
Executes each python program in the steps required.

# Process Data
## Synopsis
Process Data is used to clean and shape the open-library dataset to prepare the VIAF lines for use in the viaf_xml_parser file. These lines ensure that the author dataset is only retained when analysing the viaf dataset.

## Usage
## Process Data 
the following functions or classes:
	write_data
	clean_file
	validate_json
	if_keys_exist
	read_json_file
	load_data
	call_load_data
	main

Globals:
INPUTPATH = {  
"base": "Data",  
"Filtered": "Data\\Filtered",  
"Valid_Json": "Data\\Filtered",  
"Scraped": "Data\\Scraped",  
"Invalid_Data": "Data\\Filtered\\InvalidData"  
}
Dictionary to aid with where files can be saved based on what state they are in.

<b>main</b> the beginning of the program, 
names_to_call contains names that target files begin with and the function <b>call_load_data</b> searches through each of the names looking for any files that begin with the word but may have other words or text after the name.
each csv file contains valid and invalid json, marked by whether python can read the line or not. Although invalid json is not read after the point of failure it is saved and is not recognised anymore. The valid json that python finds means the program could read the line successfully, this is saved but is referenced in <b>viaf_xml_parser</b> at which point it is no longer used. The valid json line are used to get the VIAF ID out of the file which is tested against the VIAF cluster used in viaf_xml_parser to make sure the VIAF IDs originate from the open library dataset.

## viaf_xml_parser
the following functions or classes:
	find_word
	ViafLineComposer
	NationalityXMLIterator
	LargeXmlIterator
	main

Globals:
FILE_NAME = 'Data\\viaf-20230306-clusters_nationalities.xml'  
NEW_FILE = "Data\\autism_nationalities.xml"  
VIAF_LIST = ""

<b>main</b> the beginning of the program, this program was used many times and has had most of its lines changed as intended for testing purposes.

viaf_composer uses globals and its own set of file names to scrape valid VIAF IDs from an VIAF XML cluster file and writes it to viaf_lines.txt, this function checks if the line exists in its records but does not intuitively check the line file for names

the purpose behind viaf_xml_parser is to fing a tag with a particular word or entry inside the tag for example under Data the file 'viaf-20230306-clusters_nationalities.xml' originates from this function where all the valid lines of code found in viaf_lines text file were tested against the main viaf-20230306-clusters.xml file. 

## read_marc21_countrycodes
the following functions or classes:
	iso2_loop
	CountryCodeConverter
	dictionary_matches
	NationalityXMLIterator
	dictionary_counter
	plot_map
	set_country_permutations
	sort_dictionary
	plot_country_count
	get_country_count
	merge_data
	read_shapefile
	ProcessCountryInfo
	main

Globals: None

<b>main</b> the beginning of the program, this program takes the 'viaf-20230306-clusters_nationalities.xml' and processes it for search terms for example preloaded was the search term 'autism' when ever a xml file has the title autism, this xml line will contain a VIAF ID and a country code, the functionality works as follows.

Each viaf id matching the search term in its book title is appended to a dictionary along side its gathered country code. A check to make sure the VIAF ID is not in the directory is done, after this only codes are required and are passed through a country checker to make sure valid codes are passed to the map plotter and the country list counter. 

## Graph locations
It is expected that the dataset may take a while to load, to save waiting for it to finish, the world map and each plot is saved under fig_export found underneath codebase.

## Appendix
The material came from open library dataset and VIAF clusters xml.
the original intent was to just use the open library dataset but an unexpected consequence was that inconsistencies between both of the datasets were present before the data cleaning process was initiated.

This lead to ~30GB of Open library dataset being scraped to less than 5GB
and the VIAF Cluster being shaped from 162GB to 9GB then reduced to 345MB for the final project.

The open library dataset was discarded in favour of using the VIAF clusters. Just the VIAF IDs in open library were used to match with the VIAF cluster.

An observation made was that neither datasets appeared to have succinct information, a possible consideration would be that the authors nationality was not present in the viaf cluster and the impact of this is the author is not successfully retrieved. 

# Further considerations
## Cleanliness
At this point the project does not do anything with XML lines that do have a valid viaf id found in the VIAF lines but it can not find the nationality
a way of handling this would be to output these to invalid files, in case something switched the order of the nationality and caused the country of origin to be missed.

This could be captured with a try catch flag as no error may occur the best tackle is if it is not found, try this way, if it is still not found,
skip and save flagged as unable to find this line in a file for further investigation.

## Other datasets
There are other records that may contain country of origin for a author, such that their dataset may include a readable and translatable country
code or name, a ranked test would work out quite sufficiently which country codes from each dataset apply to the particular author, if not,
simply choose the first valid country of origin found.

## Database
A SQL database would be more useful for searching large sets, as views can be pre-processed before the user searches allowing for a program to present a list of valid search terms and caution longer search times for those that are not yet presently pre-compiled for the user to view.

## Classes
Class based functions and modularity of program would allow for less duplication of modules whilst allowing each python program to have a level of interdependence. 

## Misc user handling

### Dashboard
An admin dashboard is one way of handling a functional way of providing users with a report based system that can pull pre-processed views from the sql database and trigger statistical analysis to save the user time, each sql view can be saved as a smaller summary of facts that can be loaded to help reduce time spent preparing information and provide a faster response time for the user

### Progress
Progress bars for reading files would be useful for users but the complexity behind some processes was found to be significantly more than just reading a file and reporting to the user that it will take time to read the file.

## File types
Alongside providing material like this some other more advanced extensions of this program would be allowing for particular templates for json, xml or csv data.
The program could present the user with how to format their data, read it in and present it back with the world map and graphs. 
Essentially this is beyond the scope of the project but is another way of attacking program usage and longevity so users can make use of the program in many other projects.
