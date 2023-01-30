import streamlit as st
from streamlit_imagegrid import streamlit_imagegrid
import requests
from PIL import Image
from io import BytesIO
import pandas as pd

def imgrid(username):
    zoom_val = st.sidebar.slider('Zoom',500,600)

    df = pd.read_csv('application_posts.csv')
    df = df[df['username'] == username]

    urls = []

    for link in df['img_link']:
        urls.append(
            {
                "src": link
            }
        )

    return_value = streamlit_imagegrid(urls=urls,zoom=zoom_val,height=1000)

    if return_value is not None:
        response = requests.get(return_value)
        st.sidebar.markdown('<img src={} width=240px></img>'.format(return_value),unsafe_allow_html=True)