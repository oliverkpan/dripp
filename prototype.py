import streamlit as st
from PIL import Image
from image_utils import image_to_byte_array, localize_objects, create_boundaries
from data_utils import write_results_to_df, product_catalog_columns
from search import google_lens, reverse_image_search
import os
import cv2

def prototype():
    # User uploads image
    image = st.file_uploader("Upload image")

    if image is not None:
        image = Image.open(image)

        image.save('images/selected.png')

        st.subheader("Uploaded image")

        st.image(image, width=400)

        if st.button("Detect objects"):
            image_to_byte = image_to_byte_array(image)
            num_entities, coordinates_dict = localize_objects(image_to_byte)
            
            # Need to write a path here
            st.subheader("Detected Items")
            items, encryption = create_boundaries(coordinates_dict)

            # Makes each image public, so that we can perform searches
            os.system('gsutil -m acl set -R -a public-read gs://dripp_images_test2')
        
            keys = list(items.keys())

            if len(keys) == 3:    
                tab1, tab2, tab3 = st.tabs(items.keys())
            else:
                tab1, tab2 = st.tabs(items.keys())
        
            try:
                with tab1:

                    results = google_lens(f'temp_images/{keys[0].lower()}_{encryption}.png')

                    try:
                        with st.expander("See results"):
                            df1 = write_results_to_df(results)

                        with st.expander("Product catalog"):
                            product_catalog_columns(df1)

                    except:
                        try:
                            results = reverse_image_search(f'temp_images/{keys[0].lower()}_{encryption}.png')
                            st.write(results)
                        except:
                            st.write("No product matches")
            except:
                st.write("?")

            try:
                with tab2:

                    results = google_lens(f'temp_images/{keys[1].lower()}_{encryption}.png')

                    try:
                        with st.expander("See results"):
                            df2 = write_results_to_df(results)

                        with st.expander("Product catalog"):
                            product_catalog_columns(df2)

                    except:
                        st.write("No product matches")
            except:
                st.write("?")

            try:
                with tab3:

                    results = google_lens(f'temp_images/{keys[2].lower()}_{encryption}.png')

                    try:
                        with st.expander("See results"):
                            df3 = write_results_to_df(results)

                        with st.expander("Product catalog"):
                            product_catalog_columns(df3)

                    except:
                        st.write("No product matches")
            except:
                st.write("?")