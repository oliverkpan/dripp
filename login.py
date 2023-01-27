import streamlit as st
import streamlit_authenticator as stauth
from yaml import SafeLoader
import yaml

# hashed_passwords = stauth.Hasher(['123', '456']).generate()

with st.sidebar:
    st.image('images/dripp.png')

# with open('test.yaml') as file:
#     config = yaml.load(file, Loader=SafeLoader)

# authenticator = stauth.Authenticate(
# config['credentials'],
# config['cookie']['name'],
# config['cookie']['key'],
# config['cookie']['expiry_days'],
# config['preauthorized'])

names = ['John Smith','Rebecca Briggs']
usernames = ['jsmith','rbriggs']
passwords = ['123','456']

hashed_passwords = stauth.hasher(passwords).generate()

authenticator = stauth.authenticate(names,usernames,passwords,'cookie_name', 'signature_key',cookie_expiry_days=30)

name, authentication_status, username = authenticator.login('Login', 'main')

if authentication_status:
    authenticator.logout('Logout', 'main')
    st.write(f'Welcome *{name}*')
    st.title('Some content')
elif authentication_status is False:
    st.error('Username/password is incorrect')
elif authentication_status is None:
    st.warning('Please enter your username and password')
