# Import necessary libraries
import requests
from bs4 import BeautifulSoup
import streamlit as st

# Function to scrape website content
def scrape_website(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Check for request errors
        soup = BeautifulSoup(response.text, 'html.parser')
        return soup.get_text()
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching the URL: {e}")
        return None

# Streamlit app
def main():
    st.title("Web Scraping Tool")
    url = st.text_input("Enter the URL of the website you want to scrape:")
    
    if st.button("Scrape"):
        if url:
            content = scrape_website(url)
            if content:
