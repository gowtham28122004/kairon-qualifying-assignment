import requests
from bs4 import BeautifulSoup
from langchain.tools import tool

@tool("web_scraper_tool")
def scraper_tool(url: str) -> str:
    """
    Scrapes the text content of a given URL.
    Returns the text content or an error message if the page cannot be fetched or parsed.
    """
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # Raise an exception for bad status codes
        
        soup = BeautifulSoup(response.content, "html.parser")
        
        # Remove script and style elements
        for script_or_style in soup(["script", "style"]):
            script_or_style.decompose()
            
        # Get text and clean it up
        text = soup.get_text()
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = "\n".join(chunk for chunk in chunks if chunk)
        
        return text[:5000] # Return the first 5000 characters to keep it manageable
    except requests.RequestException as e:
        return f"Error fetching URL {url}: {e}"
    except Exception as e:
        return f"An error occurred while scraping {url}: {e}"