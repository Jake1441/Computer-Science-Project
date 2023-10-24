import glob
import re
import xml.etree.ElementTree as ET
import json
import os

"""
    Provides xml parsing functions to get data from VIAF cluster xml files

    Author: Jacob Reid
    Date: 8/03/2023
    Compatibilities:
    This program is recommended to run on Python 3.10.x
    Some packages may fail if they are run on older versions or run with unpredictable
    results. 

    The packages required will be provided in a requirements.txt
"""
# Define the target text


# Used for large_xml_iterator()
LARGE_XML_FILE = 'Data\\viaf-20230306-clusters-new.xml'  # 162GB file!
FILE_NAME = 'Data\\viaf-20230306-clusters-scraped.xml'
NEW_FILE = "Data\\viaf-20230306-clusters_nationalities_snip.xml"  # default file writeline saves to if not overridden

VIAF_LIST = ""
REMOTE_ID = "remote_ids"
VIAF_NAME = "viaf"

INPUTPATH = {
    "base": "Data",
    "Scraped": "Data\\Scraped"
}


def find_word(w):
    """
        Find whole word
    """
    return re.compile(r'\b({0})\b'.format(w), flags=re.IGNORECASE).search


class ViafLineComposer:
    def __init__(self, viaf_file):
        self.viaf_file = viaf_file

    def initiate_composer(self):
        """
        Get current VIAF data if its avaliable
        append records to the viaf line list,
        """
        line_dedup = []
        target_file = "scraped_authors*"
        target_location = glob.glob(os.path.join(INPUTPATH["Scraped"], (f"{target_file}" + ".csv")))
        try:
            infile = open(self.viaf_file, 'r')
            line_dedup = infile.read().splitlines()
            infile.close()
        except FileNotFoundError:
            print(f"{self.viaf_file} not yet found will try to create from scratch.")
        self.process_viaf_data(target_location, line_dedup)

    def process_viaf_data(self, t_location, l_dedup):
        """
        Process the data and ensure no duplicates are created
        """
        enc = "utf-8"
        for data in t_location:
            with open(data, 'r', encoding=enc) as file:
                for line in file:
                    line = line.strip()
                    json_data = json.loads(line)
                    try:
                        json_data = json_data.get(REMOTE_ID)[VIAF_NAME]
                    except LookupError:
                        print(f"Skipped {line}, could not find valid VIAF record!")
                    else:
                        if json_data not in l_dedup:
                            l_dedup.append(json_data)
                            self.writeline(json_data)
                            self.writeline("\n")

    def writeline(self, line):
        """writes the line to file."""
        with open(self.viaf_file, 'a+', encoding='utf-8') as file:
            file.write(line)


class NationalityXMLIterator:
    """
    Designed to get nationality and other
    relevant data from a scraped large xml file
    """

    def __init__(self, file_name, target_file):
        self.file_name = file_name
        self.target_file = target_file

    def commit_elements(self, viaf_e, nat_e, titles_e):
        """ Commit elements to disk so the element can be cleared."""
        self.process_viaf_id(viaf_e)
        self.process_nationality(nat_e)
        self.process_titles(titles_e)
    def iterate(self):
        """ Iterates through the xml elements """
        for event, elem in ET.iterparse(self.file_name, events=("start", "end")):

            if elem.tag == "{http://viaf.org/viaf/terms#}viafID" and event == "start":
                viaf_elem = elem

            if elem.tag == "{http://viaf.org/viaf/terms#}nationalityOfEntity" and event == "start":
                nationality_elem = elem

            if event == "start" and elem.tag == "{http://viaf.org/viaf/terms#}titles":
                print(viaf_elem.text)
                print(nationality_elem.text)
                print(elem.text)
                self.commit_elements(viaf_elem, nationality_elem, elem)
                # self.process_viaf_id(viaf_elem)
                # self.process_nationality(nationality_elem)
                # self.process_titles(elem)
            elem.clear()

    def process_viaf_id(self, viaf_ele):
        """ Collects VIAF ID"""
        self.writeline(f'<viafCluster id="{viaf_ele.text}">')
        v_text = ET.tostring(viaf_ele)
        v_line = [v_text]
        line = b"".join(v_line).decode("utf-8")
        self.writeline(line)

    def process_titles(self, elem):
        """Finds the title elements under work (book titles)"""
        self.writeline("<work>")
        for data_elem in elem:
            if data_elem.tag == "{http://viaf.org/viaf/terms#}work":
                self.process_title(data_elem)
        self.writeline("</work>")
        self.writeline('</viafCluster>')

    def process_title(self, data_elem):
        """When it finds the title it will write the lines containg the xml data."""
        for elm in data_elem:
            if elm.tag == "{http://viaf.org/viaf/terms#}title":
                record = [ET.tostring(elm)]
                line = b"".join(record).decode("utf-8")
                self.writeline(line)

    def process_nationality(self, elem):
        """Initiate the lines for the nationality of the author"""
        v_line = []
        v_text = ET.tostring(elem)
        if elem and v_text:
            v_line.append(v_text)
            for data_elem in elem[0]:
                if data_elem.tag == "{http://viaf.org/viaf/terms#}text":
                    record = [ET.tostring(data_elem)]
                    line = b"".join(record).decode("utf-8")
                    self.writeline(line)

    def writeline(self, line):
        """Commits lines back to the file"""
        with open(self.target_file, 'a+', encoding='utf-8') as file:
            file.write(line)


class LargeXmlIterator:
    """Designed to iterate through a large xml file"""

    def __init__(self, f_name, target_file):
        """Init program"""
        self.f_name = f_name
        self.target_file = target_file
        # ensure the root xml is appended

    def large_xml_data_write(self, viaf_string, element_data):
        """
        Writes xml data from the original dataset to a new scraped file
        This scraped file contains only authors matching from openlibrary viaf ids.
        """
        self.writeline(f'<viafCluster id="{viaf_string}">')
        for data in element_data:
            record = [ET.tostring(data)]
            line = b"".join(record).decode("utf-8")
            self.writeline(line)
            self.writeline("\n")
        VIAF_LIST.remove(viaf_string)
        self.writeline(f'</viafCluster>')
        print(len(VIAF_LIST))

    def xml_iter(self, elem):
        """
        This function breaks up and finds if the viafID matches
        for processing this allows for the main function to clear the element and not lose its progress.
        """
        if elem and elem[0].tag == "{http://viaf.org/viaf/terms#}viafID" and self.check_inlist(elem[0].text):
            viaf_id = elem[0].text
            #tag_term = "{http://viaf.org/viaf/terms#}nationalityOfEntity"
            #if elem.findall(tag_term):
            self.large_xml_data_write(viaf_id, elem)

    def initiate_xml_instance(self):
        """
            Iterate through the xml file finding where the cluster starts.
        """
        for event, elem in ET.iterparse(self.f_name, events=("start", "end")):
            if event == "start" and elem.tag == "{http://viaf.org/viaf/terms#}VIAFCluster":
                self.xml_iter(elem)
            elem.clear()

    def check_inlist(self, viaf_id):
        """
        Finds if VIAF ID is in the list
        """
        if viaf_id in VIAF_LIST:
            return viaf_id
        else:
            return False

    def writeline(self, line):
        """writes the line to file."""
        with open(self.target_file, 'a+', encoding='utf-8') as file:
            file.write(line)


def jre141_run_xml_parse():
    """
    Run program
    """
    print("Processing valid authors, please wait!")
    viaf_file = "Data\\viaf_lines.txt"
    # compose_viaf = ViafLineComposer(viaf_file)
    # compose_viaf.initiate_composer()

    global VIAF_LIST
    with open("Data\\viaf_lines.txt", 'r') as infile:
        VIAF_LIST = infile.read().splitlines()

    xml_iterator = LargeXmlIterator(LARGE_XML_FILE, FILE_NAME)
    xml_iterator.writeline("<xml>")
    xml_iterator.initiate_xml_instance()
    xml_iterator.writeline("</xml>")

    nationality_iter = NationalityXMLIterator(FILE_NAME, NEW_FILE)
    nationality_iter.writeline("<xml>")
    nationality_iter.iterate()
    nationality_iter.writeline("</xml>")

    print(f"created {NEW_FILE} for use with graphs!")
    print("Finished!")