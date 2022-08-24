url = '''https://www.digitalcitiesph.com/location-profiles/provinces/cebu'''
start_of_json = '''{"provinces":'''
end_of_json = ''',"siteData"'''

def jsonExtractor():
    """

    Inputs
    ------
    None

    Returns
    -------
    None

    Description
    -----------
    > Ignores SSL certificate errors to access a URL in the global scope 'url'.
    > Extracts the 'unclean_json' based on the parameters set in "soup.findAll()".
    > Writes the unclean_json into a file called "jsonExtracted.json" with the UTF-8 format.

    """
    from urllib.request import urlopen
    from bs4 import BeautifulSoup
    import ssl

    # Ignore SSL certificate errors
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    html = urlopen(url, context=ctx).read()

    soup = BeautifulSoup(html, "html.parser")

    unclean_json = soup.findAll('script')[1]

    fh = open('jsonExtracted.json', 'w', encoding='UTF-8')
    fh.write(str(unclean_json))
    fh.close()

    return None

def jsonTrimmer():
    """

    Inputs
    ------
    None

    Returns
    -------
    A trimmed .json str based on the specifications of 'start_of_json' & 'end_of_json' using the file "jsonExtracted.json".

    Description
    -----------
    > This reads the file "jsonExtracted.json" then uses Regular Expressions to extract the useful data by trimming the 'start_of_json' & 'end_of_json'.
    > It then returns the useful json as a string for "jsonPrettyPrinter()".
    > This depends on the previous function "jsonExtractor()" execution to work.

    """
    import re

    fh = open('jsonExtracted.json', 'r', encoding='UTF-8')
    unclean_json_file = fh.read()
    fh.close()
    
    regex_trim = re.findall(f'.*({start_of_json}.*){end_of_json}', unclean_json_file)

    trimmed_json = str(regex_trim[0])
    
    return trimmed_json

def jsonPrettyPrinter():
    """

    Inputs
    ------
    None

    Returns
    -------
    None

    Description
    -----------
    > It uses the string found in the function "jsonTrimmer()" then formats it with indentation as 'formatted_json'.
    > It then creates a file called "jsonCleaned.json" and writes the 'formatted_json' data.
    > This depends on the previous function "jsonTrimmer()" to be executed first.
    > This creates a cleaned .json data file, called "jsonCleaned.json", to be loaded as a Python dictionary data structure.

    """
    import json

    loaded_json = json.loads(jsonTrimmer())
    formatted_json = json.dumps(loaded_json, indent=2)

    fh = open('jsonCleaned.json', 'w', encoding='UTF-8')
    fh.write(str(formatted_json))
    fh.close()

    return None

def __main__():
    """

    (!!!) THIS IS DISFUNCTIONAL (!!!) REFER TO MY OLD CODE BELOW (!!!)
    > The output contains HTML tags and is very messy. It's unusable for easy MS Excel processing.
    
    """
    import json

    fh = open('jsonCleaned.json', 'r', encoding='UTF-8')
    data = fh.read()
    data = json.loads(data)
    fh.close()

    # creates a file handle 'newFile' to write the .json's data into .csv named 'ScrapedRawData.csv' for MS Excel to read
    new_csv = open('rawData.csv', 'w', encoding='UTF-8')

    # navigates to the 'cities' key in the 'data' dictionary, which is a list of cities where their values are dictionary key-value pairs
    cities_data = data['cities']

    # creates list containing valid data fields
    valid_fields = []
    for field in cities_data[0]:
        valid_fields.append(field)

    # writes the headers on a single row on the .csv file
    for field in valid_fields:
        new_csv.write(f'{field},')
    new_csv.write('\n')

    # iterate through all the (field,values) for each city, print the values under the headings of the .csv
    for city in cities_data:
        for field,value in city.items():
            if field in valid_fields:
                new_csv.write(f'{value}',)
        new_csv.write('\n')

    new_csv.close()

__main__()

# (!!!) ORIGINAL CODE TO MAKE "ScrapedRawData.csv" (!!!)
"""

-----
This was the code I used to automate the extraction of the manually extracted .json file.
> I downloaded the .html file of the URL to get the raw .json file.
> I used jsonformatter.org to clean the json file for processing & to download it as "Province of Cebu.json"
> This code uses "Province of Cebu.json" to create a .csv for MS Excel to process.
-----

import json
import csv

# opens a .json file, parses it as a str, then parses the .json str into a Python dictionary: 'data'
jsonFile = open('Province of Cebu.json', 'r', encoding = 'UTF-8')
data = json.loads(jsonFile.read())

# navigates to the 'cities' key in the 'data' dictionary, which is a list of cities where their values are dictionary key-value pairs
citiesData = data['cities']

# creates a file handle 'newFile' to write the .json's data into .csv named 'ScrapedRawData.csv' for MS Excel to read
newFile = open('ScrapedRawData.csv', 'w', encoding = 'UTF-8')

# writes the headers on a single row, once
for header in citiesData[0].keys():
    newFile.write(f'{header},')
newFile.write('\n')

# writes the values on consecutive rows, per city entry
for entry in citiesData:
    for values in entry.values():
        newFile.write(f'{values},')
    newFile.write('\n')

# closes the files to prevent data corruption
newFile.close()
jsonFile.close()
"""