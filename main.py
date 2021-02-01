import os
import pandas as pd
from typing import List, Optional
from pandas import read_excel
from fastapi import FastAPI
from pydantic import BaseModel, EmailStr


#Get xlsx path
BASE_DIR = os.path.dirname(os.path.abspath(__file__)) 
DATA_DIR = os.path.join(BASE_DIR, 'data')
dataset = os.path.join(DATA_DIR, 'plants-reduced.xlsx')

app = FastAPI()

#simple test
@app.get('/')
def read_root():
    return {"Hello": "World"}

# GET list of all plants loaded from Excel file
@app.get("/plant/")
async def read_plant_data(order: str = None, limit: int = None, state: str = None):
    #read/parse excel file
    xl_file  = pd.ExcelFile(dataset)
    #create dataframe with only 5 columns needed
    df = pd.read_excel(dataset, index_col=0,usecols=\
        ['eGRID2016 Plant file sequence number',\
         'Plant state abbreviation', 'Plant name',\
         'Plant latitude' ,\
         'Plant longitude' ,\
         'Plant annual net generation (MWh)'])

    #get top 5 in the head
    print(df.head()) 
    #get column name list
    print(df.columns.ravel())
    
    #if state query parameter is defined, then filter based on state
    if state:
        df = df[df['Plant state abbreviation'].str.match(state)]
    
    #if limit query parameter is defined, then limit dataframe
    if limit:
        print(df.sort_values(by='Plant annual net generation (MWh)', ascending=False ).head(limit))
        df = df.sort_values(by='Plant annual net generation (MWh)', ascending=False ).head(limit)

    #replace NaN value with empty char or 0 (giving error)
    df = df.fillna('')

    #return df.to_json(orient='records')
    return df.to_dict(orient='record')


# GET list of all State and their NET MWh and %
@app.get("/state/")
async def read_state_data():
    #read/parse excel file
    xl_file  = pd.ExcelFile(dataset)
    #create dataframe with only 5 columns needed
    df = pd.read_excel(dataset, index_col=0,usecols=\
        ['eGRID2016 Plant file sequence number',\
         'Plant state abbreviation', 'Plant name',\
         'Plant latitude' ,\
         'Plant longitude' ,\
         'Plant annual net generation (MWh)'])

    #get top 5 in the head
    print(df.head()) 
    #get column name list
    print(df.columns.ravel())

    #grouby dataframe based on state
    grouped = df.groupby(["Plant state abbreviation"])\
                                            .agg({'Plant name':'count', 'Plant annual net generation (MWh)': 'sum'})\
                                            .reset_index().rename(columns={'Plant name':'Plant Count'})
    
    #add new % column to the dataframe
    grouped['state_pcts'] = (grouped['Plant annual net generation (MWh)'] / 
                  grouped['Plant annual net generation (MWh)'].sum()) * 100
    
    #print(state_pcts)
    #replace NaN value with empty char or 0 (giving error)
    grouped = grouped.fillna('')
    print(grouped.head())
    return grouped.to_dict(orient='record')
