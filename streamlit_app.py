import requests
from bs4 import BeautifulSoup
import streamlit as st
from urllib.parse import urljoin, urlparse
import time

# Function to scrape website content and preserve context
def scrape_website_with_context(url, visited):
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
      
      # Find all links on the page
      links = set()
      for a_tag in soup.find_all('a', href=True):
          href = a_tag.get('href')
          full_url = urljoin(url, href)
          if urlparse(full_url).netloc == urlparse(url).netloc:
              links.add(full_url)
      
      return ''.join(content), links
  except requests.exceptions.RequestException as e:
      st.error(f"Error fetching the URL: {e}")
      return None, set()

# Function to crawl the entire website
def crawl_website(start_url):
  visited = set()
  to_visit = {start_url}
  all_content = []

  while to_visit:
      current_url = to_visit.pop()
      if current_url not in visited:
          st.write(f"Scraping {current_url}")
          content, links = scrape_website_with_context(current_url, visited)
          if content:
              all_content.append(content)
          visited.add(current_url)
          to_visit.update(links - visited)
          time.sleep(1)  # Be polite and avoid overloading the server

  return '\n'.join(all_content)

# Streamlit app
def main():
  st.title("Web Scraping Tool for Entire Website")
  url = st.text_input("Enter the URL of the website you want to scrape:")
  
  if st.button("Scrape"):
      if url:
          content = crawl_website(url)
          if content:
              with open("scraped_full_website_content.txt", "w", encoding="utf-8") as file:
                  file.write(content)
              st.success("Content scraped and saved to scraped_full_website_content.txt")
              st.download_button("Download Scraped Content", content, "scraped_full_website_content.txt")
      else:
          st.warning("Please enter a valid URL.")

if __name__ == "__main__":
  main()
