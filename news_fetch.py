import requests
from bs4 import BeautifulSoup
import streamlit as st

@st.cache_data
def fetch_news():
    url = "https://cen.acs.org/sections/markets.html"

    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "lxml")

        headlines = [a.text.strip() for a in soup.select(".teaser-title a")[:5]]
        links = [a["href"] for a in soup.select(".teaser-title a")[:5]]

        return list(zip(headlines, links))

    except Exception as e:
        st.error(f"⚠️ News Fetch Error: {e}")
        return []
