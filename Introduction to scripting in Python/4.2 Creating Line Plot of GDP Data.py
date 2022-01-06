#!/usr/bin/env python
# coding: utf-8

# In[1]:


"""
Project for Week 2 of "Python Data Visualization".
Read World Bank GDP data and create some basic XY plots.
Be sure to read the project description page for further information
about the expected behavior of the program.
"""

import csv
import pygal

def read_csv_as_nested_dict(filename, keyfield, separator, quote):
    """
    Inputs:
      filename  - Name of CSV file
      keyfield  - Field to use as key for rows
      separator - Character that separates fields
      quote     - Character used to optionally quote fields
    Output:
      Returns a dictionary of dictionaries where the outer dictionary
      maps the value in the key_field to the corresponding row in the
      CSV file.  The inner dictionaries map the field names to the
      field values for that row.
    """
    row_dict = dict()
    with open(filename, mode='r', newline='') as csvfile:
        csv_reader = csv.DictReader(csvfile,delimiter=separator,quotechar=quote)
        for row in csv_reader:
            row_dict[row[keyfield]] = row
    return row_dict


def build_plot_values(gdpinfo, gdpdata):
    """
    Inputs:
      gdpinfo - GDP data information dictionary
      gdpdata - A single country's GDP stored in a dictionary whose
                keys are strings indicating a year and whose values
                are strings indicating the country's corresponding GDP
                for that year.
    Output: 
      Returns a list of tuples of the form (year, GDP) for the years
      between "min_year" and "max_year", inclusive, from gdpinfo that
      exist in gdpdata.  The year will be an integer and the GDP will
      be a float.
    """
    gdp_list = list()
    for stat in gdpdata.items():
        try:
            if int(stat[0]) in range(gdpinfo['min_year'],gdpinfo['max_year']+1):
                gdp_list.append((int(stat[0]),float(stat[1])))
        except ValueError:
            continue
    gdp_list.sort(key=lambda stat: stat[0], reverse=False)
    return gdp_list


def build_plot_dict(gdpinfo, country_list):
    """
    Inputs:
      gdpinfo      - GDP data information dictionary
      country_list - List of strings that are country names
    Output:
      Returns a dictionary whose keys are the country names in
      country_list and whose values are lists of XY plot values 
      computed from the CSV file described by gdpinfo.
      Countries from country_list that do not appear in the
      CSV file should still be in the output dictionary, but
      with an empty XY plot value list.
    """
    dict_xy = dict()
    filename = gdpinfo["gdpfile"]
    keyfield = gdpinfo['country_name']
    separator = gdpinfo['separator']
    quote = gdpinfo['quote']
    nested_dict = read_csv_as_nested_dict(filename,keyfield,separator,quote)
    
    for country_name in country_list:
        if country_name in nested_dict.keys():
            country_data_row = list(nested_dict[country_name].items())
            country_data_dict = dict(country_data_row)
            dict_xy[country_name] = build_plot_values(gdpinfo, country_data_dict)
        else:
            dict_xy[country_name] = []
    return dict_xy


def render_xy_plot(gdpinfo, country_list, plot_file):
    """
    Inputs:
      gdpinfo      - GDP data information dictionary
      country_list - List of strings that are country names
      plot_file    - String that is the output plot file name
    Output:
      Returns None.
    Action:
      Creates an SVG image of an XY plot for the GDP data
      specified by gdpinfo for the countries in country_list.
      The image will be stored in a file named by plot_file.
    """
    xy_plot = pygal.XY()
    xy_plot.title = 'Plot of GDP for select countries spanning 1960 to 2015'
    xy_plot.x_title = 'Year'
    xy_plot.y_title = 'GDP in current US dollars'
    
    plot_data = build_plot_dict(gdpinfo, country_list)
    for c_name, gdp in plot_data.items():
        xy_plot.add(c_name,gdp)
        
    xy_plot.render_to_file(plot_file)


def test_render_xy_plot():
    """
    Code to exercise render_xy_plot and generate plots from
    actual GDP data.
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

    render_xy_plot(gdpinfo, [], "isp_gdp_xy_none.svg")
    render_xy_plot(gdpinfo, ["China"], "isp_gdp_xy_china.svg")
    render_xy_plot(gdpinfo, ["United Kingdom", "United States"],"isp_gdp_xy_uk+usa.svg")


# Make sure the following call to test_render_xy_plot is commented out
# when submitting to OwlTest/CourseraTest.

test_render_xy_plot()


# In[ ]:




