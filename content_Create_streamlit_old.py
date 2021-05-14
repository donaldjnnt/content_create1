#!/usr/bin/env python
# coding: utf-8

# In[6]:


import streamlit as st
import pandas as pd
import numpy as np
import pathlib
import base64
#import plotly.express as px
#from plotly.subplots import make_subplots
#import plotly.graph_objects as go
#import matplotlib.pyplot as plt

import requests
import urllib
import pandas as pd
from requests_html import HTML
from requests_html import HTMLSession

st.title("Content Creation for the Given Topic using Web Scraping and NLP")
st.sidebar.title("Content Creation for the Given Topic using Web Scraping and NLP")
#st.markdown("This application is to extract URLs and text content related to the given topic:")
st.markdown("***")
st.sidebar.markdown("This application is to extract URLs and text content for the given topic")

def get_source(url):
    """Return the source code for the provided URL. 

    Args: 
        url (string): URL of the page to scrape.

    Returns:
        response (object): HTTP response object from requests_html. 
    """

    try:
        session = HTMLSession()
        response = session.get(url)
        return response

    except requests.exceptions.RequestException as e:
        print(e)
        
def scrape_google(query):

    query = urllib.parse.quote_plus(query)
    response = get_source("https://www.google.co.in/search?q=" + query)

    links = list(response.html.absolute_links)
    google_domains = ('https://www.google.', 
                      'https://google.', 
                      'https://webcache.googleusercontent.', 
                      'http://webcache.googleusercontent.', 
                      'https://policies.google.',
                      'https://support.google.',
                      'https://maps.google.',
                      'https://www.youtube.')

    for url in links[:]:
        if url.startswith(google_domains):
            links.remove(url)

    return links

def download_link(object_to_download, download_filename, download_link_text):
    """
    Generates a link to download the given object_to_download.

    object_to_download (str, pd.DataFrame):  The object to be downloaded.
    download_filename (str): filename and extension of file. e.g. mydata.csv, some_txt_output.txt
    download_link_text (str): Text to display for download link.

    Examples:
    download_link(YOUR_DF, 'YOUR_DF.csv', 'Click here to download data!')
    download_link(YOUR_STRING, 'YOUR_STRING.txt', 'Click here to download your text!')

    """
    if isinstance(object_to_download,pd.DataFrame):
        object_to_download = object_to_download.to_csv(index=False)

    # some strings <-> bytes conversions necessary here
    b64 = base64.b64encode(object_to_download.encode("UTF-8")).decode()

    return f'<a href="data:file/txt;base64,{b64}" download="{download_filename}">{download_link_text}</a>'


Topic = st.text_input('Input the topic here:')
def Extract_urls():
    if len(Topic)>0:
        if st.button("Extract URLs"):
    #    if text is not None:
            with st.spinner("Extracting..."):
                df = pd.DataFrame(scrape_google(Topic), columns = ['link'])
                #df1 = pd.DataFrame(scrape_google(Topic + ' ' + word), columns = ['link'])
#                df = df1[~df1['link'].str.contains('cours', na=False)]
                if st.button('Download Output as a text file'):
                    tmp_download_link = download_link(df, 'Your_Output.txt', 'Click here to download your output!')
                    st.markdown(tmp_download_link, unsafe_allow_html=True)
                st.write("Below are the top URLs to extract content:")
                for x in df['link']:
                    st.write(x)
#    else:
#        st.error("Please input the topic again")
Extract_urls()

