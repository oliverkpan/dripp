import streamlit as st
from PIL import Image
from image_utils import image_to_byte_array, localize_objects, create_boundaries
from data_utils import write_results_to_df
from search import google_lens
import os
from prototype import prototype
from yaml import SafeLoader
import yaml
import streamlit_authenticator as stauth
import pickle
from pathlib import Path
import pandas as pd

# Page configs
st.set_page_config(layout="wide")
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

    # Lookup username in database and show current profile

    # user_df = user_df[user_df['username'] == username]



    # Create sidebar
    with st.sidebar:
        st.image('images/dripp.png')
        select_option = st.radio("Select", ("App Prototype", "How to use", "FAQ"))
        authenticator.logout('Logout', 'main')

    if select_option == "App Prototype":
        prototype()
    
elif authentication_status is False:
    st.error('Username/password is incorrect')
elif authentication_status is None:
    st.warning('Please enter your username and password')

    
