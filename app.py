import streamlit as st
import requests
import arrow
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("api_key")
query = "CoinGecko"

url = f'https://newsapi.org/v2/everything?q={query}&apiKey={api_key}&language=en&sortBy=publishedAt&searchIn=title,content'

response = requests.get(url)
data = response.json()

st.header(query)
for article in data["articles"]:

  with st.container():
    
    left, right = st.columns([2,1])
    
    with left:
      st.markdown(f'#### {article["title"]}')
      st.markdown(f"""
        Author: {article["author"]}, *published {arrow.get(article["publishedAt"]).humanize()}*
        \n{article["description"]}
      """)
      st.markdown(f'Source: {article["url"]} `{article["source"]["name"]}`')
      
    with right:  
      st.image(article["urlToImage"], caption=f'Image by {article["source"]["name"]}')
      
  st.write("-----")