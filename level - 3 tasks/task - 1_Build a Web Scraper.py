import requests
from bs4 import BeautifulSoup
import csv
import json
import time
import random
from urllib.parse import urljoin, urlparse
import logging
from typing import List, Dict, Optional
import re

class WebScraper:
    """
    A flexible web scraper class that can extract data from websites
    """
    
    def __init__(self, delay_range=(1, 3), headers=None):
        """
        Initialize the scraper with optional delay and headers
        
        Args:
            delay_range: Tuple of (min, max) seconds to wait between requests
            headers: Dictionary of HTTP headers to use
        """
        self.delay_range = delay_range
        self.session = requests.Session()
        
        # Default headers to mimic a real browser
        default_headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
        }
        
        if headers:
            default_headers.update(headers)
        
        self.session.headers.update(default_headers)
        
        # Setup logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
    
    def get_page(self, url: str, timeout: int = 10) -> Optional[BeautifulSoup]:
        """
        Fetch a webpage and return BeautifulSoup object
        
        Args:
            url: URL to scrape
            timeout: Request timeout in seconds
            
        Returns:
            BeautifulSoup object or None if failed
        """
        try:
            # Add random delay to be respectful
            if self.delay_range:
                delay = random.uniform(*self.delay_range)
                time.sleep(delay)
            
            response = self.session.get(url, timeout=timeout)
            response.raise_for_status()
            
            # Parse with BeautifulSoup
            soup = BeautifulSoup(response.content, 'html.parser')
            self.logger.info(f"Successfully scraped: {url}")
            return soup
            
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Error scraping {url}: {e}")
            return None
    
    def extract_text(self, soup: BeautifulSoup, selector: str) -> List[str]:
        """
        Extract text from elements matching CSS selector
        
        Args:
            soup: BeautifulSoup object
            selector: CSS selector string
            
        Returns:
            List of text content
        """
        elements = soup.select(selector)
        return [elem.get_text(strip=True) for elem in elements]
    
    def extract_attributes(self, soup: BeautifulSoup, selector: str, attribute: str) -> List[str]:
        """
        Extract specific attributes from elements
        
        Args:
            soup: BeautifulSoup object
            selector: CSS selector string
            attribute: Attribute name to extract
            
        Returns:
            List of attribute values
        """
        elements = soup.select(selector)
        return [elem.get(attribute, '') for elem in elements if elem.get(attribute)]
    
    def extract_links(self, soup: BeautifulSoup, base_url: str = None) -> List[Dict[str, str]]:
        """
        Extract all links from the page
        
        Args:
            soup: BeautifulSoup object
            base_url: Base URL for relative links
            
        Returns:
            List of dictionaries with 'url' and 'text' keys
        """
        links = []
        for link in soup.find_all('a', href=True):
            url = link['href']
            if base_url:
                url = urljoin(base_url, url)
            
            links.append({
                'url': url,
                'text': link.get_text(strip=True)
            })
        
        return links
    
    def extract_images(self, soup: BeautifulSoup, base_url: str = None) -> List[Dict[str, str]]:
        """
        Extract all images from the page
        
        Args:
            soup: BeautifulSoup object
            base_url: Base URL for relative URLs
            
        Returns:
            List of dictionaries with image info
        """
        images = []
        for img in soup.find_all('img'):
            src = img.get('src', '')
            if base_url and src:
                src = urljoin(base_url, src)
            
            images.append({
                'src': src,
                'alt': img.get('alt', ''),
                'title': img.get('title', '')
            })
        
        return images
    
    def scrape_table(self, soup: BeautifulSoup, selector: str = 'table') -> List[List[str]]:
        """
        Extract data from HTML tables
        
        Args:
            soup: BeautifulSoup object
            selector: CSS selector for table
            
        Returns:
            List of rows, each row is a list of cell values
        """
        table = soup.select_one(selector)
        if not table:
            return []
        
        rows = []
        for tr in table.find_all('tr'):
            cells = tr.find_all(['td', 'th'])
            row = [cell.get_text(strip=True) for cell in cells]
            if row:  # Skip empty rows
                rows.append(row)
        
        return rows
    
    def scrape_news_articles(self, url: str) -> List[Dict[str, str]]:
        """
        Example: Scrape news articles from a news website
        This is a generic example - you'll need to adapt selectors for specific sites
        
        Args:
            url: URL of the news website
            
        Returns:
            List of article dictionaries
        """
        soup = self.get_page(url)
        if not soup:
            return []
        
        articles = []
        
        # Common selectors for news articles (adapt as needed)
        article_selectors = [
            'article',
            '.article',
            '.news-item',
            '.post',
            '.story'
        ]
        
        for selector in article_selectors:
            article_elements = soup.select(selector)
            if article_elements:
                break
        
        for article in article_elements[:10]:  # Limit to first 10 articles
            title_elem = article.find(['h1', 'h2', 'h3', 'h4'])
            title = title_elem.get_text(strip=True) if title_elem else 'No title'
            
            # Try to find link
            link_elem = article.find('a', href=True)
            link = urljoin(url, link_elem['href']) if link_elem else ''
            
            # Try to find summary/excerpt
            summary_elem = article.find(['p', '.summary', '.excerpt'])
            summary = summary_elem.get_text(strip=True) if summary_elem else ''
            
            articles.append({
                'title': title,
                'link': link,
                'summary': summary[:200] + '...' if len(summary) > 200 else summary
            })
        
        return articles
    
    def scrape_ecommerce_products(self, url: str) -> List[Dict[str, str]]:
        """
        Example: Scrape product information from e-commerce sites
        This is a generic example - adapt selectors for specific sites
        
        Args:
            url: URL of the e-commerce page
            
        Returns:
            List of product dictionaries
        """
        soup = self.get_page(url)
        if not soup:
            return []
        
        products = []
        
        # Common selectors for products (adapt as needed)
        product_selectors = [
            '.product',
            '.item',
            '.product-item',
            '[data-product]'
        ]
        
        for selector in product_selectors:
            product_elements = soup.select(selector)
            if product_elements:
                break
        
        for product in product_elements:
            name_elem = product.find(['h1', 'h2', 'h3', 'h4', '.product-name', '.title'])
            name = name_elem.get_text(strip=True) if name_elem else 'No name'
            
            # Try to find price
            price_elem = product.find(['.price', '.cost', '.amount'])
            price = price_elem.get_text(strip=True) if price_elem else 'No price'
            
            # Try to find image
            img_elem = product.find('img')
            image = img_elem.get('src', '') if img_elem else ''
            if image:
                image = urljoin(url, image)
            
            products.append({
                'name': name,
                'price': price,
                'image': image
            })
        
        return products
    
    def save_to_csv(self, data: List[Dict], filename: str):
        """
        Save scraped data to CSV file
        
        Args:
            data: List of dictionaries
            filename: Output filename
        """
        if not data:
            self.logger.warning("No data to save")
            return
        
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = data[0].keys()
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            writer.writeheader()
            for row in data:
                writer.writerow(row)
        
        self.logger.info(f"Data saved to {filename}")
    
    def save_to_json(self, data: List[Dict], filename: str):
        """
        Save scraped data to JSON file
        
        Args:
            data: List of dictionaries
            filename: Output filename
        """
        with open(filename, 'w', encoding='utf-8') as jsonfile:
            json.dump(data, jsonfile, indent=2, ensure_ascii=False)
        
        self.logger.info(f"Data saved to {filename}")


# Example usage and demonstrations
def main():
    """
    Demonstrate the web scraper with various examples
    """
    scraper = WebScraper(delay_range=(1, 2))
    
    # Example 1: Scrape quotes from a test site
    print("=== Example 1: Scraping Quotes ===")
    quotes_url = "http://quotes.toscrape.com/"
    soup = scraper.get_page(quotes_url)
    
    if soup:
        # Extract quotes
        quotes = scraper.extract_text(soup, '.quote .text')
        authors = scraper.extract_text(soup, '.quote .author')
        
        quotes_data = []
        for i, quote in enumerate(quotes):
            if i < len(authors):
                quotes_data.append({
                    'quote': quote,
                    'author': authors[i]
                })
        
        print(f"Found {len(quotes_data)} quotes")
        for quote_data in quotes_data[:3]:  # Show first 3
            print(f"Quote: {quote_data['quote']}")
            print(f"Author: {quote_data['author']}\n")
        
        # Save to files
        scraper.save_to_csv(quotes_data, 'quotes.csv')
        scraper.save_to_json(quotes_data, 'quotes.json')
    
    # Example 2: Extract all links from a page
    print("=== Example 2: Extracting Links ===")
    if soup:
        links = scraper.extract_links(soup, quotes_url)
        print(f"Found {len(links)} links")
        for link in links[:5]:  # Show first 5
            print(f"Text: {link['text']}")
            print(f"URL: {link['url']}\n")
    
    # Example 3: Custom data extraction
    print("=== Example 3: Custom Data Extraction ===")
    if soup:
        # Extract tags from quotes
        tags_elements = soup.select('.quote .tags a')
        all_tags = [tag.get_text(strip=True) for tag in tags_elements]
        unique_tags = list(set(all_tags))
        
        print(f"Found {len(unique_tags)} unique tags:")
        print(", ".join(unique_tags))


if __name__ == "__main__":
    main()