import streamlit as st
from ultralytics import YOLO
import pandas as pd
import numpy as np
import threading
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
from object_detection import test
import asyncio
from streamlit.runtime.scriptrunner import add_script_run_ctx

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



async def page1():
    col1, col2= st.columns([2,1])


    col1, col2= st.columns([2,1], gap="medium")

    
    with col1:
        with st.container():
            col3,col4 = st.columns(2)
            with col3:
                # st.subheader("Stream")
                # # st.image("https://pbs.twimg.com/profile_images/1544722618275827713/9-aMN_Wb_400x400.jpg")
                # video_html = """     
                # <iframe src="https://drive.google.com/file/d/1EiD7UCM2La2etEva7fF8uSNAivfZ6DjA/preview" width="320" height="240" allow="autoplay"></iframe>
                # """
                # col3.markdown(video_html, unsafe_allow_html=True)  
                await test.people_counter()

            with col4:
                await st.subheader("Number of clients")
                data = np.random.randn(20,1)
                
                st.bar_chart(abs(data))
        await st.subheader("Current number of products")

        # dataframe of number of products in market
        df = pd.DataFrame(
            np.random.randn(20, 5) * 20 + 100,
            columns=['Apple', 'Banana', 'Cherry', 'Date', 'Elderberry'])
        await st.bar_chart(df)


    with col2:
        with st.container():
            # analyze the data and provide some sugggest some useful insights
            await st.subheader("Recommendations")
            if df['Apple'].mean() > 100:
                st.write("Apple is doing well")
            else:
                st.write("Apple is not doing well. Need to refill")
            if df['Banana'].mean() > 100:
                st.write("Banana is doing well")
            else:
                st.write("Banana is not doing well. Need to refill")
            if df['Cherry'].mean() > 100:
                st.write("Cherry is doing well")
            else:
                st.write("Cherry is not doing well. Need to refill")
            if df['Date'].mean() > 100:
                st.write("Date is doing well")
            else:
                st.write("Date is not doing well. Need to refill")
            if df['Elderberry'].mean() > 100:
                st.write("Elderberry is doing well")
            else:
                st.write("Elderberry is not doing well. Need to refill")


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

    # asyncio.run(page1())
    isLogged=True
    show_all_pages()
    authenticator.logout("Logout", "sidebar")
    
    st.sidebar.title(f"Welcome {name}")
    #link rel css stylesheet
    col1, col2= st.columns([2,1])


    col1, col2= st.columns([2,1], gap="medium")

    frame = st.empty()
    with col1:
        with st.container():
            col3,col4 = st.columns(2)
            with col3:
                # st.subheader("Stream")
                # # st.image("https://pbs.twimg.com/profile_images/1544722618275827713/9-aMN_Wb_400x400.jpg")
                # video_html = """     
                # <iframe src="https://drive.google.com/file/d/1EiD7UCM2La2etEva7fF8uSNAivfZ6DjA/preview" width="320" height="240" allow="autoplay"></iframe>
                # """
                # col3.markdown(video_html, unsafe_allow_html=True)
                startAnalysis = st.button("Analyze")
                if startAnalysis:
                    thread = threading.Thread(target=test.people_counter())
                    #add_script_run_ctx(thread)
                    thread.start()
                
            with col4:
                st.subheader("Number of clients")
                data = np.random.randn(20,1)
                
                st.bar_chart(abs(data))
        st.subheader("Current number of products")

        # dataframe of number of products in market
        df = pd.DataFrame(
            np.random.randn(20, 5) * 20 + 100,
            columns=['Apple', 'Banana', 'Cherry', 'Date', 'Elderberry'])
        st.bar_chart(df)


    with col2:
        with st.container():
            # analyze the data and provide some sugggest some useful insights
            st.subheader("Recommendations")
            data = pd.read_csv("values.csv") #path folder of the data file
            st.write(data) #displays the table of data
            # if df['Apple'].mean() > 100:
            #     st.write("Apple is doing well")
            # else:
            #     st.write("Apple is not doing well. Need to refill")
            # if df['Banana'].mean() > 100:
            #     st.write("Banana is doing well")
            # else:
            #     st.write("Banana is not doing well. Need to refill")
            # if df['Cherry'].mean() > 100:
            #     st.write("Cherry is doing well")
            # else:
            #     st.write("Cherry is not doing well. Need to refill")
            # if df['Date'].mean() > 100:
            #     st.write("Date is doing well")
            # else:
            #     st.write("Date is not doing well. Need to refill")
            # if df['Elderberry'].mean() > 100:
            #     st.write("Elderberry is doing well")
            # else:
            #     st.write("Elderberry is not doing well. Need to refill")