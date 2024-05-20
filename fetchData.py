import os
import requests
import pandas as pd

# Define the indicators
indicators = {
    'CO2 Emissions (metric tons per capita)': 'EN.ATM.CO2E.PC',
    'Forest Area (% of land area)': 'AG.LND.FRST.ZS',
    'Access to Electricity (% of population)': 'EG.ELC.ACCS.ZS',
    'Renewable Energy Consumption (% of total final energy consumption)': 'EG.FEC.RNEW.ZS'
}

def fetch_data(country_code='KE'):
    data = {}
    for name, indicator in indicators.items():
        url = f'http://api.worldbank.org/v2/country/{country_code}/indicator/{indicator}?format=json&per_page=1000'
        response = requests.get(url)
        json_data = response.json()
        data[name] = pd.json_normalize(json_data[1])
    return data

def save_data(data, folder='data'):
    if not os.path.exists(folder):
        os.makedirs(folder)
    for name, df in data.items():
        # Replace spaces and parentheses in filenames for better compatibility
        filename = f'{folder}/{name.replace(" ", "_").replace("(", "").replace(")", "")}.csv'
        df.to_csv(filename, index=False)

if __name__ == '__main__':
    data = fetch_data()
    save_data(data)
