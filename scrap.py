import requests
from bs4 import BeautifulSoup
from utils import remove_external, remove_hash, get_href_value, get_full_links, extract_filename_from_url, create_csv_file_with_header


def get_soup(url):
    response = requests.get(url)
    return BeautifulSoup(response.text, "html.parser")

def main(url):
    print("The program is running...")
    soup = get_soup(url)
    anchor_tags = soup.find_all("a", href=True)
    # Extract and the filter href values
    hrefs = remove_external(remove_hash(get_href_value(anchor_tags)), url)
    full_links = get_full_links(hrefs, url)
    file_name = extract_filename_from_url(url)
    create_csv_file_with_header(file_name)


if __name__ == '__main__':
    url = input('Enter the website URL: ')
    main(url)
