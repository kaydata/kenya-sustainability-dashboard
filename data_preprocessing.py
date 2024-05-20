import pandas as pd
import os

def load_and_clean_data(folder='data'):
    combined_data = pd.DataFrame()
    for file in os.listdir(folder):
        if file.endswith('.csv'):
            name = file.split('.')[0].replace('_', ' ')
            df = pd.read_csv(os.path.join(folder, file))
            df = df[['date', 'value']]
            df.columns = ['Year', name]
            if combined_data.empty:
                combined_data = df
            else:
                combined_data = pd.merge(combined_data, df, on='Year', how='outer')
    
    # Convert 'Year' to string to extract the last 4 digits
    combined_data['Year'] = combined_data['Year'].astype(str).str[-4:].astype(int)
    combined_data['Year'] = pd.to_datetime(combined_data['Year'], format='%Y')

    # Drop rows with missing values for simplicity
    combined_data.dropna(inplace=True)
    
    return combined_data

if __name__ == '__main__':
    data = load_and_clean_data()
    data.to_csv('combined_data.csv', index=False)
