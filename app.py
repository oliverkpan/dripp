import streamlit as st
from PIL import Image
from image_utils import image_to_byte_array, localize_objects, create_boundaries
from data_utils import write_results_to_df
from search import google_lens
import os
from prototype import prototype
from st_imgrid import imgrid
from yaml import SafeLoader
import yaml
import streamlit_authenticator as stauth
import pickle
from pathlib import Path
import pandas as pd

# Page configs
im = Image.open("favicon.ico")
st.set_page_config(layout="wide",
                   page_title="dripp",
                   page_icon=im)
st.set_option('deprecation.showPyplotGlobalUse', False)

if 'item_search' not in st.session_state:
    st.session_state.item_search = None

names = ['John Smith','Rebecca Briggs','Oliver Pan']
usernames = ['jsmith','rbriggs','oliverkpan']

file_path = Path(__file__).parent / "hashed_pw.pkl"
with file_path.open("rb") as file:
    hashed_passwords = pickle.load(file)

authenticator = stauth.Authenticate(names, usernames, hashed_passwords, 'cookie', 'key', cookie_expiry_days=0)
name, authentication_status, username = authenticator.login('Login', 'main')

if authentication_status:

    # Create sidebar
    with st.sidebar:
        dripp_logo = st.image('images/dripp.png')
        select_option = st.radio("Select", ("Outfit Detection", "Profile", "Search", "How to use"))
        authenticator.logout('Logout', 'main')

    if select_option == "Outfit Detection":
        prototype(username)

    elif select_option == "Profile":  
        st.subheader(f"@{username}")
        imgrid(username)

    elif select_option == "Search":  
        celeb = st.text_input('Search Username')
        imgrid(celeb)
    
elif authentication_status is False:
    st.error('Username/password is incorrect')
elif authentication_status is None:
    st.warning('Please enter your username and password')

    
