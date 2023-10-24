import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
import pycountry_convert as pc
import xml.etree.ElementTree as ET
import re

"""
    reads the viaf XML dataset containing marc21 formatted records
    looks for relevant xml fields based on author and countries that will extend
    to what the user selects and prepares the data for being described.

    Author: Jacob Reid
    Date: 8/03/2023
    Compatibilities:
    This program is recommended to run on Python 3.10.x
    Some packages may fail if they are run on older versions or run with unpredictable
    results. 

    The packages required will be provided in a requirements.txt
"""


def iso2_loop(list1):
    """
        reduces a list by removing its null values
        both list sizes will be equivalent based on the function calling this loop.
    """
    other_list = CountryCodeConverter(list1).convert_to_iso2()
    for i in range(len(other_list)):
        if (other_list[i]) != "NULL":
            list1[i] = other_list[i]
    return list1


class CountryCodeConverter:
    """
    Converts country names to the country code appends null if not to keep shape of list consistent.
    """

    def __init__(self, countries_data):
        self.countries_data = countries_data

    def convert_to_iso2(self):
        iso2_codes_list = []
        """Convert ISO3 codes to ISO2 Codes"""
        for country_name in self.countries_data:
            try:
                code = pc.country_name_to_country_alpha2(country_name)
                iso2_codes_list.append(code)
            except:
                iso2_codes_list.append('NULL')
        return iso2_codes_list


def dictionary_matches(dict1, re_list):
    """Uses Regex to find dictionary matches"""
    temp_dict = {}
    for line in dict1.keys():
        matches = re.findall(re_list, line)
        if matches:
            for match in matches:
                if match[0] not in temp_dict.keys():
                    temp_dict[match[0]] = dict1.get(match)
                else:
                    temp_dict[match[0]] += dict1.get(match)
    return temp_dict


class NationalityXMLIterator:
    def __init__(self, search_term, file_name):
        self.file_name = file_name
        self.search_term = search_term

    def iterate(self):
        viaf_dict = {}
        for event, elem in ET.iterparse(self.file_name, events=("start", "end")):
            if elem.tag == "{http://viaf.org/viaf/terms#}viafID" and event == "start":
                v_text = ET.tostring(elem)

            if elem.tag == "{http://viaf.org/viaf/terms#}text" and event == "start":
                nationality_text = elem.text

            if event == "start" and elem.tag == "work":
                viaf_dict = self.process_records(elem, v_text, nationality_text, viaf_dict)
            elem.clear()
        return viaf_dict

    def process_records(self, elem, v_text, nationality_text, v_dict):
        for data_elem in elem:
            record = []
            if data_elem.tag == "{http://viaf.org/viaf/terms#}title":
                record.append(ET.tostring(data_elem))
                ans = self.find_word(self.search_term)(f'{data_elem.text}')
                if ans and v_text not in v_dict:
                    v_dict[v_text] = nationality_text
        return v_dict

    def find_word(self, w):
        """Find whole word"""
        return re.compile(r'\b({0})\b'.format(w), flags=re.IGNORECASE).search

    def process_nationality(self, elem):
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
        with open(self.target_file, 'a+', encoding='utf-8') as file:
            file.write(line)


def dictionary_counter(dict_items):
    """returns Dictionary count of how many times a value appears in a key"""
    temp_count_dict = {}
    for line in dict_items:
        if line and len(line) == 2:
            line = line.upper()
            if line not in temp_count_dict:
                temp_count_dict[line] = 1
            else:
                temp_count_dict[line] += 1
    return temp_count_dict


def plot_map(df):
    """Prints the map """
    col, title, source = 'code_count', 'World Map', 'Source: Jacob Reid COSC480'
    vmin, vmax = df[col].min(), df[col].max()
    cmap = 'gnuplot'
    fig, ax = plt.subplots(1, figsize=(20, 8))
    ax.axis('off')
    df.plot(column=col, ax=ax, edgecolor='0.8', linewidth=1, cmap=cmap, missing_kwds={'color': 'lightgrey'})
    ax.set_title(title, fontdict={'fontsize': '25', 'fontweight': '3'})
    ax.annotate(source, xy=(0.1, .08), xycoords='figure fraction', horizontalalignment='left',
                verticalalignment='bottom', fontsize=10)
    sm = plt.cm.ScalarMappable(norm=plt.Normalize(vmin=vmin, vmax=vmax), cmap=cmap)
    cbaxes = fig.add_axes([0.15, 0.25, 0.01, 0.4])
    fig.colorbar(sm, cax=cbaxes)
    plt.show(block=False)
    plt.pause(5)
    plt.close()
    fig.savefig(f'fig_export\\{cmap}_map_export.png', dpi=300)
    plt.close(fig)


def set_country_permutations():
    """Returns permutations for list items"""
    permutations = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T",
                    "U",
                    "V", "W", "X", "Y", "Z"]

    num_print = 3
    count = 1
    list_slice = 0
    new_list = []
    next_list_item = permutations[0 + list_slice:num_print * count]
    list_item = "na"
    while list_item and next_list_item:
        list_item = permutations[0 + list_slice:num_print * count]
        temp_strings = ""
        for x in list_item:
            temp_strings += x
        new_list.append(f"{temp_strings}")
        list_slice = num_print * count
        count += 1
        next_list_item = permutations[0 + list_slice:num_print * count]
    return new_list


def sort_dictionary(dict_to_sort):
    """ Function to sort dictionary"""
    new_dict = {}
    for key in sorted(dict_to_sort.keys()):
        new_dict[key] = dict_to_sort[key]
    return new_dict


def plot_country_count(temp_dict):
    """Plots the country dictionary by """
    temp_dict = sort_dictionary(temp_dict)
    counts = temp_dict.values()
    country_codes = list(temp_dict.keys())
    if len(country_codes) > 1:
        xs = range(len(counts))
        axes = plt.axes()
        axes.bar(xs, counts)
        axes.set_title(f"Count of countries from {country_codes[0]} to {country_codes[-1]}")
        axes.set_ylabel('Number in country')
        axes.set_xticks(xs)
        axes.set_xticklabels(country_codes)
        plt.show(block=False)
        plt.pause(3)
        plt.savefig(f'fig_export\\{country_codes[0]}_to_{country_codes[-1]}_map_export.png', dpi=300)
        plt.close()


def get_country_count(data):
    """A plot of authors by first country letter"""
    my_reg_strings = set_country_permutations()
    full_count = ""
    for line in my_reg_strings:
        temp_dict = dictionary_matches(data, f"^[{line}].*")
        if temp_dict:
            plot_country_count(temp_dict)
            full_count += line
    full_count = dictionary_matches(data, f"^[{full_count}].*")
    plot_country_count(full_count)


def merge_data(left_data, right_data):
    """
    Merges the data from left and right to a dataframe that would then
    be compatible for plotting.
    """
    if right_data:
        right_data = pd.DataFrame(right_data.items(), columns=['Country', 'code_count'])
        merged_df = pd.merge(left=left_data, right=right_data, how='left', left_on='iso2_code', right_on='Country')
        plot_map(merged_df)


def read_shapefile(shape_data):
    """
        Reads the world shape data
        code retrieved from
        https://www.relataly.com/visualize-covid-19-data-on-a-geographic-heat-maps/291/
    """
    # Setting the path to the shapefile
    shape_file = f'data/shapefiles/worldmap/{shape_data}.shp'
    # Read shapefile using Geopandas
    geo_df = gpd.read_file(shape_file)[['ADMIN', 'ADM0_A3', 'geometry']]
    # Rename columns.
    geo_df.columns = ['country', 'country_code', 'geometry']
    # Drop row for 'Antarctica'. It takes a lot of space in the map and is not of much use
    geo_df = geo_df.drop(geo_df.loc[geo_df['country'] == 'Antarctica'].index)
    geo_df['iso2_code'] = CountryCodeConverter(geo_df['country'].to_list()).convert_to_iso2()
    # There are some countries for which the converter could not find a country code.
    # We will drop these countries.
    geo_df = geo_df.drop(geo_df.loc[geo_df['iso2_code'] == 'NULL'].index)
    return geo_df


class ProcessCountryInfo:
    """Process country information for authors"""

    def __init__(self, f_name, search_terms):
        self.f_name = f_name
        self.search_terms = search_terms

    def search_book_title(self):
        """ Look for book titles based on the details"""
        nationality_iter = NationalityXMLIterator(self.search_terms, self.f_name)
        temp_codes_1 = nationality_iter.iterate()
        temp_codes = [code for code in temp_codes_1.values()]
        return dictionary_counter(iso2_loop(temp_codes))


def jre141_output_g():
    """The program """
    print('*' * 30)
    print(
        "The plots will be saved under 'Fig_Export' \n "
        "you may leave this running if you wish to carry on with other processes.")
    print('*' * 30)

    lookup_value = "Autism"
    # file_name = "Data\\viaf-autism.xml"
    # file_name = "Data\\viaf-20230306-clusters_nationalities_backup.xml"
    file_name = "Data\\viaf-autism.xml"
    # Create an instance of ProcessCountryInfo
    country_info = ProcessCountryInfo(file_name, lookup_value)
    # Call the search_book_title method
    countries = country_info.search_book_title()
    shape = 'ne_10m_admin_0_countries'
    g_df = read_shapefile(shape)
    merge_data(g_df, countries)
    get_country_count(countries)
    print("The plots were saved under 'Fig_Export'")
    print("Finished!")

