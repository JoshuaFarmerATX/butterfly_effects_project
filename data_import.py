import requests
import pandas as pd
import json
import pprint
import matplotlib as plt
import numpy as np
import country_converter as coco
import warnings
import logging


def get_rest_countries():
    r = requests.get("https://restcountries.eu/rest/v2/all")
    raw_data = r.json()

    def extract_block(field_name, d):
        try:
            return d[field_name][0]["name"]
        except:
            pass

    def get_lat_lon(int, d):
        try:
            return d['latlng'][int]
        except:
            pass

    df =  pd.DataFrame([{
        "country": d["name"],
        "ISO3": d['alpha3Code'],
#         "Capital": d['capital'],
        "region": d['region'],
        "sub-region": d['subregion'],
#         "Population": d['population'],
        "latitude": get_lat_lon(0,d),
        "longitude": get_lat_lon(1,d),
#         "Area": d['area'],
#         "Timezone": d['timezones'][0],
        "borders": d['borders'],
#         "Currencies": extract_block('currencies', d),
        "regional_bloc": extract_block('regionalBlocs', d)
        } for d in raw_data])
    
    df = df.append({
        'country':'World',
        'ISO3': 'World',
        'region': 'World',
        'sub-region': 'World',
        'latitude': 'World',
        'longitude': 'World',
        'borders': 'World',
        'regional_bloc': 'World'
              }, ignore_index=True)
    return df

def get_cia_data():
    with open('factbook.json', encoding='utf-8') as json_file:
        data = json.load(json_file)
    
    data_list = []
    data_list = []
    for country_name in data["countries"].keys():
        country_data = data["countries"][country_name]["data"]

        try:
            name = country_data["name"]
        except:
            name = np.nan

        try:
            government_type = country_data["government"]["government_type"]
        except:
            government_type = np.nan

        try:
            population = country_data["people"]["population"]["total"]
        except:
            population = np.nan

        try:
            internet_users = country_data["communications"]["internet"]["users"]["total"]
        except:
            internet_users = np.nan   

        try:
            internet_users_percent = country_data["communications"]["internet"]["users"]["percent_of_population"]
        except:
            internet_users_percent = np.nan     

        try:
            internet_users_rank = country_data["communications"]["internet"]["users"]["global_rank"]
        except:
            internet_users_rank = np.nan     

        try:
            telephones_fixed = country_data["communications"]["telephones"]["fixed_lines"]["total_subscriptions"]
        except:
            telephones_fixed = np.nan    

        try:
            telephones_fixed_rank = country_data["communications"]["telephones"]["fixed_lines"]["global_rank"]
        except:
            telephones_fixed_rank = np.nan 

        try:
            telephones_mobile = country_data["communications"]["telephones"]["mobile_cellular"]["total_subscriptions"]
        except:
            telephones_mobile = np.nan    

        try:
            telephones_mobile_rank = country_data["communications"]["telephones"]["mobile_cellular"]["global_rank"]
        except:
            telephones_mobile_rank = np.nan 

        try:
            median_age = country_data["people"]["median_age"]["total"]["value"]
        except:
            median_age = np.nan

        try:
            gdp_purchasing = ((country_data["economy"]['gdp']["purchasing_power_parity"]["annual_values"])[0])["value"]
        except:
            gdp_purchasing = np.nan

        try:
            gdp_rank = country_data["economy"]['gdp']["purchasing_power_parity"]["global_rank"]
        except:
            gdp_rank = np.nan

        try:
            education_expen = country_data["people"]["education_expenditures"]["percent_of_gdp"]
        except:
            education_expen = np.nan

        try:
            education_rank = country_data["people"]["education_expenditures"]["global_rank"]
        except:
            education_rank = np.nan

        data_list.append({
            "country": name,
#             "Government Type": government_type,
            "population": population,
            "internet_users": internet_users,
            "internet_%_of_population": internet_users_percent,
            "internet_global_rank": internet_users_rank,
            "telephones_fixed_lines": telephones_fixed,
#             "Telephones Fixed Lines Global Rank": telephones_fixed_rank,
            "telephone_mobile_cellular": telephones_mobile,
#             "Telephone Mobile Cellular Global Rank": telephones_mobile_rank,
            "median_age": median_age,
            "gdp_purchasing_power_parity": gdp_purchasing,
            "gdp_global_rank": gdp_rank,
            "education_expenditures": education_expen,
            "education_expeditures_global_rank": education_rank,


        })
        
    df = pd.DataFrame(data_list)
    
    logger = logging.getLogger()
    logger.disabled = True
    
    some_names = list(df.country)
    standard_names = coco.convert(names=some_names, to='name_short', not_found=None)
    iso3_codes = coco.convert(names=standard_names, to='ISO3', not_found=None)
    
    logger.disabled = False

    
    
    df['ISO3'] = iso3_codes
    df = df.dropna(subset=['internet_users'])
    
    return df
