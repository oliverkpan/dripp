from serpapi import GoogleSearch
from data_utils import read_api_key
import streamlit as st

def reverse_image_search(path):

    params = {
        "engine": "google_reverse_image",
        "image_url": f"https://storage.googleapis.com/dripp_images_test2/{path}",
        "api_key": read_api_key()
    }

    search = GoogleSearch(params)
    results = search.get_dict()
    return results

def google_lens(path):

    params = {
        "engine": "google_lens",
        "url": f"https://storage.googleapis.com/dripp_images_test2/{path}",
        "api_key": read_api_key()
    }

    search = GoogleSearch(params)
    results = search.get_dict()
    return results
