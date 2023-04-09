import streamlit as st
import pandas as pd
import numpy as np
from prophet import Prophet
from prophet.diagnostics import performance_metrics
from prophet.diagnostics import cross_validation
from prophet.plot import plot_cross_validation_metric
import base64
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader
from streamlit.source_util import _on_pages_changed, get_pages
import json
from pathlib import Path

st.set_page_config(page_title="Main", page_icon=None, layout="wide", initial_sidebar_state="collapsed", menu_items=None)

DEFAULT_PAGE = "Main.py"
isLogged = False #global variable to check if user is logged in

def get_all_pages():
    default_pages = get_pages(DEFAULT_PAGE)

    pages_path = Path("pages.json")

    if pages_path.exists():
        saved_default_pages = json.loads(pages_path.read_text())
    else:
        saved_default_pages = default_pages.copy()
        pages_path.write_text(json.dumps(default_pages, indent=4))

    return saved_default_pages


def clear_all_but_first_page():
    current_pages = get_pages(DEFAULT_PAGE)

    if len(current_pages.keys()) == 1:
        return

    get_all_pages()

    # Remove all but the first page
    key, val = list(current_pages.items())[0]
    current_pages.clear()
    current_pages[key] = val

    _on_pages_changed.send()


def show_all_pages():
    current_pages = get_pages(DEFAULT_PAGE)

    saved_pages = get_all_pages()

    missing_keys = set(saved_pages.keys()) - set(current_pages.keys())

    # Replace all the missing pages
    for key in missing_keys:
        current_pages[key] = saved_pages[key]

    _on_pages_changed.send()



clear_all_but_first_page()


with open('style.css') as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)


# --- USER AUTHENTICATION ---
# load hashed passwords

hashed_passwords = stauth.Hasher(['abc', 'def']).generate()

with open('config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['preauthorized']
)

name, authentication_status, username = authenticator.login("Login", "main")

if authentication_status == False:
    st.error("Username/password is incorrect")

elif authentication_status == None:
    st.warning("Please enter your username and password")

elif authentication_status:
    isLogged=True
    show_all_pages()
    authenticator.logout("Logout", "sidebar")
    
    st.sidebar.title(f"Welcome {name}")
    #link rel css stylesheet
    col1,col2= st.columns([2,1])


    col1,col2= st.columns([2,1], gap="medium")


    with col1:
        with st.container():
            col3,col4 = st.columns(2)
            with col3:
                # st.image("https://pbs.twimg.com/profile_images/1544722618275827713/9-aMN_Wb_400x400.jpg")
                video_html = """
                    <iframe src="https://drive.google.com/file/d/1EiD7UCM2La2etEva7fF8uSNAivfZ6DjA/preview" width="320" height="240" allow="autoplay"></iframe>
                    
                """
                col3.markdown(video_html, unsafe_allow_html=True)
            with col4:
                data = np.random.randn(20,1)
                st.bar_chart(data)

        df = pd.DataFrame(
        np.random.randn(10, 5),
        columns=('col %d' % i for i in range(5)))
        #st.table(df)
        ndata = np.random.randn(100,10)
        ndata = abs(ndata)
        st.bar_chart(ndata)



    with col2:
        with st.container():
            st.markdown("#      Recommendations")
