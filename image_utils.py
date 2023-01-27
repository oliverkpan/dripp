from PIL import Image
import io
import streamlit as st
import spacy
import os
import cv2
import matplotlib.pyplot as plt
from google.cloud import vision
from gcs_utils import write_read
from data_utils import random_with_N_digits

nlp = spacy.load('en_core_web_sm')

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'vision_key.json'

def image_to_byte_array(image: Image) -> bytes:
    # BytesIO is a file-like buffer stored in memory
    imgByteArr = io.BytesIO()
    # image.save expects a file-like as a argument
    image.save(imgByteArr, format=image.format)
    # Turn the BytesIO object back into a bytes object
    imgByteArr = imgByteArr.getvalue()
    return imgByteArr

def localize_objects(content):
    """Localize objects in the local image.

    Args:
    path: The path to the local file.
    """
    from google.cloud import vision
    client = vision.ImageAnnotatorClient()

    image = vision.Image(content=content)

    objects = client.object_localization(
        image=image).localized_object_annotations

    object_coordinates = {}
    for object_ in objects:
        vertex_list = []
        for vertex in object_.bounding_poly.normalized_vertices:
            vertex_list.append([vertex.x, vertex.y])
        object_coordinates[object_.name] = vertex_list
        object_coordinates[object_.name.lower() + "_score"] = object_.score
        
    return len(objects), object_coordinates

def create_boundaries(object_coordinates):

    # Count how many items we get, max at 3 highest scores
    top_items_dict = {}
    encryption = str(random_with_N_digits(15))

    # BRUTE FORCE METHOD to dynamically creat streamlit columns
    item_count = 0
    
    for key in object_coordinates.keys():
        if key in ['Pants', 'Hat', 'Top', 'Outerwear', 'Shoes']:
            item_count += 1

    if item_count == 1:
        col1 = st.columns(1)
    
    elif item_count == 2:
        col1, col2 = st.columns(2)

    elif item_count == 3:
        col1, col2, col3 = st.columns(3)

    column_count = 1
    for key in object_coordinates.keys():
        if key in ['Pants', 'Hat', 'Top', 'Outerwear', 'Shoes'] and column_count < 4:
            
            with locals()['col' + str(column_count)]:
                data = object_coordinates[key]
                st.write(key)
                st.write(object_coordinates[key.lower() + "_score"])
                img = cv2.imread('images/selected.png')
                img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

                (number_of_rows, number_of_columns) = img.shape[:2]
                points = [(data[0][0],data[0][1]),(data[1][0],data[1][1]),
                        (data[2][0],data[2][1]),(data[3][0],data[3][1])]

                first_point_y = round(points[0][0] * number_of_columns)
                first_point_x = round(points[0][1] * number_of_rows)
                second_point_y  = round(points[2][0] * number_of_columns)
                second_point_x = round(points[2][1] * number_of_rows)

                fig, ax = plt.subplots(1, 1, figsize=(5, 5))
                ax.set_axis_off()
                cropped_image = img[first_point_x:second_point_x, first_point_y:second_point_y]
                im = Image.fromarray(cropped_image)
                im.save("temp_images/testy.png")

                path = f"temp_images/{key.lower()}_{encryption}.png"
                im.save(path)
                write_read('dripp_images_test2', path)

                im = ax.imshow(cropped_image)
                st.pyplot()
                image_localizer('temp_images/testy.png')

                # Write image to GCS
                top_items_dict[key] = f"https://storage.googleapis.com/dripp_images_test2/{path}"
                column_count += 1

    return top_items_dict, encryption

def image_localizer(path):

    client = vision.ImageAnnotatorClient()

    with io.open(path, 'rb') as image:
        content = image.read()

    image = vision.Image(content=content)

    response = client.label_detection(image=image)

    attributes = ""

    for label in response.label_annotations:
        
        attributes = attributes + label.description + " "

    attributes = attributes.rstrip()
    # st.subheader(attributes)
