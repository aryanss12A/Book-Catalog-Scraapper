import requests
from bs4 import BeautifulSoup
import pandas as pd
import openpyxl
def scrape_books_page(url):
    """
    Scrapes book information from a single page.

    Args:
        url: URL of the page to scrape.

    Returns:
        A list of dictionaries, where each dictionary represents a book with keys 
        'Title', 'Link', 'Price', and 'Stock'. 
    """
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for bad status codes
    except requests.exceptions.RequestException as e:
        print(f"Error fetching page: {e}")
        return []

    soup = BeautifulSoup(response.text, "html.parser")

    books = []
    for book in soup.find_all("li", class_="col-xs-6 col-sm-4 col-md-3 col-lg-3"):
        item = {}
        item['Title'] = book.find("img").attrs["alt"]
        item['Link'] = "https://books.toscrape.com/catalogue/" + book.find("a").attrs["href"]
        item['Price'] = book.find("p", class_="price_color").text[2:]
        item['Stock'] = book.find("p", class_="instock availability").text.strip()
        books.append(item)

    return books

def main():
    base_url = "https://books.toscrape.com/catalogue/page-{}.html"
    current_page = 1
    all_books = []

    while True:
        url = base_url.format(current_page)
        print(f"Scraping page: {current_page}")
        books = scrape_books_page(url)

        if not books:  # No books found (likely end of pages)
            break

        all_books.extend(books)
        current_page += 1

    df = pd.DataFrame(all_books)
    df.to_excel("books.xlsx", index=False)
    df.to_csv("books.csv", index=False)

# This block executes only when the script is run directly
if __name__ == "__main__":
    main()