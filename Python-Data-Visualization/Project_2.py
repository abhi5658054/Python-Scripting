"""
Project for Week 4 of "Python Data Visualization".
Unify data via common country codes.
Be sure to read the project description page for further information
about the expected behavior of the program.
"""

import csv
import math
import pygal

def read_csv_as_nested_dict(filename, keyfield, separator, quote):
    """
    Inputs:
      filename  - name of CSV file
      keyfield  - field to use as key for rows
      separator - character that separates fields
      quote     - character used to optionally quote fields
    Output:
      Returns a dictionary of dictionaries where the outer dictionary
      maps the value in the key_field to the corresponding row in the
      CSV file.  The inner dictionaries map the field names to the
      field values for that row.
    """
    table ={}
    with open(filename, "rt", newline='') as csvfile:
        csvreader = csv.DictReader(csvfile,
                                   delimiter=separator,
                                   quotechar=quote)
        for row in csvreader:
            table[row[keyfield]] = row
    return table

def build_country_code_converter(codeinfo):
    """
    Inputs:
      codeinfo      - A country code information dictionary
    Output:
      A dictionary whose keys are plot country codes and values
      are world bank country codes, where the code fields in the
      code file are specified in codeinfo.
    """
    the_dic = {}
    the_dic_of_countries = read_csv_as_nested_dict(codeinfo['codefile'], codeinfo['plot_codes'] ,
                                                   codeinfo['separator'] , codeinfo['quote'])
    the_dic_of_countries_keys = list(the_dic_of_countries.keys())
    #print(the_dic_of_countries_keys)
    for item in the_dic_of_countries_keys:
        #print(item)
        the_value_of_item = the_dic_of_countries[item]
        #print(the_value_of_item)
        the_dic[item] = the_value_of_item[codeinfo['data_codes']]


    return the_dic


def reconcile_countries_by_code(codeinfo, plot_countries, gdp_countries):
    """
    Inputs:
      codeinfo       - A country code information dictionary
      plot_countries - Dictionary whose keys are plot library country codes
                       and values are the corresponding country name
      gdp_countries  - Dictionary whose keys are country codes used in GDP data
    Output:
      A tuple containing a dictionary and a set.  The dictionary maps
      country codes from plot_countries to country codes from
      gdp_countries.  The set contains the country codes from
      plot_countries that did not have a country with a corresponding
      code in gdp_countries.
      Note that all codes should be compared in a case-insensitive
      way.  However, the returned dictionary and set should include
      the codes with the exact same case as they have in
      plot_countries and gdp_countries.
    """
    the_dic = {}
    the_list = []
    the_relatio_dic = build_country_code_converter(codeinfo)

    for item in plot_countries:
        the_upper_item = item.upper()
        #print(the_upper_item)
        the_value_of_uppitem = the_relatio_dic[the_upper_item]
        #print(the_value_of_uppitem)
        #print(the_value_of_uppitem in gdp_countries)
        if the_value_of_uppitem in gdp_countries:
            the_inf_of_country = gdp_countries[the_value_of_uppitem]
            #print(the_inf_of_country)
            the_dic[item] = the_inf_of_country['Country Code']
        else:
            the_list.append(item)


    return the_dic, set(the_list)


def build_map_dict_by_code(gdpinfo, codeinfo, plot_countries, year):
    """
    Inputs:
      gdpinfo        - A GDP information dictionary
      codeinfo       - A country code information dictionary
      plot_countries - Dictionary mapping plot library country codes to country names
      year           - String year for which to create GDP mapping
    Output:
      A tuple containing a dictionary and two sets.  The dictionary
      maps country codes from plot_countries to the log (base 10) of
      the GDP value for that country in the specified year.  The first
      set contains the country codes from plot_countries that were not
      found in the GDP data file.  The second set contains the country
      codes from plot_countries that were found in the GDP data file, but
      have no GDP data for the specified year.
    """
    the_dic = {}
    the_list1 = []
    the_list2 = []
    the_code_dic = read_csv_as_nested_dict(codeinfo['codefile'], codeinfo['plot_codes'],
                                           codeinfo['separator'], codeinfo['quote'])
    the_info_dic_ordinary = read_csv_as_nested_dict(gdpinfo['gdpfile'], gdpinfo['country_code'],
                                           gdpinfo['separator'], gdpinfo['quote'])
    the_info_dic = {}
    for code in the_info_dic_ordinary:
        the_info_dic[code.lower()] = the_info_dic_ordinary[code]

    #print("the_code_dic",the_code_dic)
    #print("the_info_dic",the_info_dic)

    for item in plot_countries:
        #print("item",item)
        if plot_countries[item] in the_code_dic:
            the_country_code = the_code_dic[plot_countries[item]][codeinfo['data_codes']]
            #print("the_country_code",the_country_code)
            #print(the_country_code.lower())
            if (the_country_code.lower()) in the_info_dic:
                if year in the_info_dic[the_country_code.lower()]:
                    the_gdp = the_info_dic[the_country_code.lower()][year]
                    if the_gdp != "":
                        the_gdp_log = math.log10(int(the_gdp))
                        the_dic[item] = the_gdp_log
                    else:
                        the_list2.append(item)
            else:
                the_list1.append(item)
        else:
            the_list1.append(item)

    return the_dic, set(the_list1), set(the_list2)

def render_world_map(gdpinfo, codeinfo, plot_countries, year, map_file):
    """
    Inputs:
      gdpinfo        - A GDP information dictionary
      codeinfo       - A country code information dictionary
      plot_countries - Dictionary mapping plot library country codes to country names
      year           - String year of data
      map_file       - String that is the output map file name
    Output:
      Returns None.
    Action:
      Creates a world map plot of the GDP data in gdp_mapping and outputs
      it to a file named by svg_filename.
    """
    return


def test_render_world_map():
    """
    Test the project code for several years
    """
    gdpinfo = {
        "gdpfile": "isp_gdp.csv",
        "separator": ",",
        "quote": '"',
        "min_year": 1960,
        "max_year": 2015,
        "country_name": "Country Name",
        "country_code": "Country Code"
    }

    codeinfo = {
        "codefile": "isp_country_codes.csv",
        "separator": ",",
        "quote": '"',
        "plot_codes": "ISO3166-1-Alpha-2",
        "data_codes": "ISO3166-1-Alpha-3"
    }

    # Get pygal country code map
    pygal_countries = pygal.maps.world.COUNTRIES

    # 1960
    render_world_map(gdpinfo, codeinfo, pygal_countries, "1960", "isp_gdp_world_code_1960.svg")

    # 1980
    render_world_map(gdpinfo, codeinfo, pygal_countries, "1980", "isp_gdp_world_code_1980.svg")

    # 2000
    render_world_map(gdpinfo, codeinfo, pygal_countries, "2000", "isp_gdp_world_code_2000.svg")

    # 2010
    render_world_map(gdpinfo, codeinfo, pygal_countries, "2010", "isp_gdp_world_code_2010.svg")