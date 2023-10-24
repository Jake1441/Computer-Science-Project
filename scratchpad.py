import xml.etree.ElementTree as ET


class NationalityXMLIterator:
    def __init__(self, file_name):
        self.file_name = file_name

    def iterate(self):
        for event, elem in ET.iterparse(self.file_name, events=("start", "end")):
            if elem.tag == "{http://viaf.org/viaf/terms#}viafID" and event == "start":
                self.process_viaf_id(elem)

            if elem.tag == "{http://viaf.org/viaf/terms#}titles" and event == "start":
                self.process_titles(elem)

            if elem.tag == "{http://viaf.org/viaf/terms#}nationalityOfEntity" and event == "start":
                self.process_nationality(elem)

            elem.clear()

    def process_viaf_id(self, elem):
        self.writeline(f'<viafCluster> id="{elem.text}"')
        v_text = ET.tostring(elem)
        v_line = [v_text]
        line = b"".join(v_line).decode("utf-8")
        self.writeline(line)

    def process_titles(self, elem):
        self.writeline("<work>")
        for data_elem in elem:
            if data_elem.tag == "{http://viaf.org/viaf/terms#}work":
                self.process_title(data_elem)
        self.writeline("</work>")
        self.writeline('</viafCluster>')

    def process_title(self, data_elem):
        for elm in data_elem:
            if elm.tag == "{http://viaf.org/viaf/terms#}title":
                record = [ET.tostring(elm)]
                line = b"".join(record).decode("utf-8")
                self.writeline(line)

    def process_nationality(self, elem):
        v_line = []
        v_text = None
        if elem and v_text:
            v_line.append(v_text)
            for data_elem in elem[0]:
                if data_elem.tag == "{http://viaf.org/viaf/terms#}text":
                    record = [ET.tostring(data_elem)]
                    line = b"".join(record).decode("utf-8")
                    self.writeline(line)

    def writeline(self, line):
        # Implement your own logic for writing the line to a file or any other output
        print(line)  # Example implementation: Print the line


# Usage example
FILE_NAME = 'Data\\viaf-20230306-clusters-emulated.xml'

iterator = NationalityXMLIterator(FILE_NAME)
iterator.iterate()
