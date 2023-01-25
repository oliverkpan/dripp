import pandas as pd
import json
import streamlit as st
from random import randint

def write_results_to_df(results):
    
    columns = ['title', 'link', 'source', 'price', 'image_link']

    df = pd.DataFrame(pd.np.empty((0, 5)))
    df.columns = columns
    catalog = results['visual_matches']

    for i in catalog:
        try:
            title = i['title']
        except:
            title = None

        try:
            link = i['link']
        except:
            link = None

        try:
            source = i['source']
        except:
            source = None

        try:
            price = i['price']['value']
        except:
            price = None

        try:
            thumbnail = i['thumbnail']  
        except:
            thumbnail = None
        
        new_data = pd.DataFrame([[title, link, source, price, thumbnail]], columns=columns)
        df = pd.concat([df, new_data])
    
    st.write(df)
    return df

def read_api_key():

    with open('serpi_key.json') as json_file:
        json_decoded = json.load(json_file)

    return json_decoded['API_KEY']


def product_catalog_columns(df):
    col1, col2, col3 = st.columns(3)

    with col1:
        st.image(df.iloc[0, 4])
        st.header(df.iloc[0, 0])
        st.subheader(df.iloc[0, 3])
        st.write(f'[link]({df.iloc[0, 1]})')

    with col2:
        st.image(df.iloc[1, 4])
        st.header(df.iloc[1, 0])
        st.subheader(df.iloc[1, 3])
        st.write(f'[link]({df.iloc[1, 1]})')


    with col3:
        st.image(df.iloc[2, 4])
        st.header(df.iloc[2, 0])
        st.subheader(df.iloc[2, 3])
        st.write(f'[link]({df.iloc[2, 1]})')

    col1, col2, col3 = st.columns(3)

    with col1:
        st.image(df.iloc[3, 4])
        st.header(df.iloc[3, 0])
        st.subheader(df.iloc[3, 3])
        st.write(f'[link]({df.iloc[3, 1]})')

    with col2:
        st.image(df.iloc[4, 4])
        st.header(df.iloc[4, 0])
        st.subheader(df.iloc[4, 3])
        st.write(f'[link]({df.iloc[4, 1]})')


    with col3:
        st.image(df.iloc[5, 4])
        st.header(df.iloc[5, 0])
        st.subheader(df.iloc[5, 3])
        st.write(f'[link]({df.iloc[5, 1]})')

    col1, col2, col3 = st.columns(3)

    with col1:
        st.image(df.iloc[6, 4])
        st.header(df.iloc[6, 0])
        st.subheader(df.iloc[6, 3])
        st.write(f'[link]({df.iloc[6, 1]})')

    with col2:
        st.image(df.iloc[7, 4])
        st.header(df.iloc[7, 0])
        st.subheader(df.iloc[7, 3])
        st.write(f'[link]({df.iloc[7, 1]})')


    with col3:
        st.image(df.iloc[7, 4])
        st.header(df.iloc[7, 0])
        st.subheader(df.iloc[7, 3])
        st.write(f'[link]({df.iloc[7, 1]})')

def random_with_N_digits(n):
    range_start = 10**(n-1)
    range_end = (10**n)-1
    return randint(range_start, range_end)