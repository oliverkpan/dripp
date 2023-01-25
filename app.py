import streamlit as st
from PIL import Image
from image_utils import image_to_byte_array, localize_objects, create_boundaries
from data_utils import write_results_to_df
from search import google_lens
import os
from prototype import prototype

# Page configs
st.set_page_config(layout="wide")
st.set_option('deprecation.showPyplotGlobalUse', False)

if 'item_search' not in st.session_state:
    st.session_state.item_search = None

# Create sidebar
with st.sidebar:
    st.image('images/dripp.png')
    select_option = st.radio("Select", ("App Prototype", "How to use", "FAQ"))

if select_option == "App Prototype":
    prototype()
