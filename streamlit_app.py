# Import necessary libraries
import requests
from bs4 import BeautifulSoup
import streamlit as st

# Function to scrape website content and preserve context
def scrape_website_with_context(url):
  try:
      response = requests.get(url)
      response.raise_for_status()  # Check for request errors
      soup = BeautifulSoup(response.text, 'html.parser')
      
      # Extract content with context
      content = []
      for element in soup.find_all(['h1', 'h2', 'h3', 'p', 'ul', 'ol', 'li']):
          if element.name in ['h1', 'h2', 'h3']:
              content.append(f"\n{element.get_text(strip=True)}\n")
          elif element.name == 'p':
              content.append(f"{element.get_text(strip=True)}\n")
          elif element.name in ['ul', 'ol']:
              for li in element.find_all('li'):
                  content.append(f" - {li.get_text(strip=True)}\n")
      
      return ''.join(content)
  except requests.exceptions.RequestException as e:
      st.error(f"Error fetching the URL: {e}")
      return None

# Streamlit app
def main():
  st.title("Web Scraping Tool with Context Preservation")
  url = st.text_input("Enter the URL of the website you want to scrape:")
  
  if st.button("Scrape"):
      if url:
          content = scrape_website_with_context(url)
          if content:
              with open("scraped_content_with_context.txt", "w", encoding="utf-8") as file:
                  file.write(content)
              st.success("Content scraped and saved to scraped_content_with_context.txt")
              st.download_button("Download Scraped Content", content, "scraped_content_with_context.txt")
      else:
          st.warning("Please enter a valid URL.")

if __name__ == "__main__":
  main()
