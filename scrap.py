import requests
from bs4 import BeautifulSoup
from utils import (
    remove_external,
    remove_hash,
    get_href_value,
    get_full_links,
    extract_filename_from_url,
    create_csv_file_with_header,
    write_to_csv,
)


def get_soup(url):
    response = requests.get(url)
    return BeautifulSoup(response.text, "html.parser")


def get_webpage_description(soup):
    # Safely get the meta tag with name="description"
    description_tag = soup.find("meta", attrs={"name": "description"})
    return description_tag.get("content") if description_tag else "No description given"


def get_webpage_title(soup):
    # Safely get the title tag value
    title_tag = soup.find("title")
    return title_tag.string if title_tag else "No title found"


def add_homepage_to_csv(soup, file_name, url):
    data = {
        "file_name": file_name,
        "serial_number": 1,
        "webpage_link": url,
        "webpage_title": get_webpage_title(soup),
        "webpage_description": get_webpage_description(soup),
    }
    write_to_csv(data)


def add_all_webpages_to_csv(file_name, links):
    serial_number = 2
    for link in links:
        soup = get_soup(link)
        webpage_title = get_webpage_title(soup)
        webpage_description = get_webpage_description(soup)
        data = {
            "file_name": file_name,
            "serial_number": serial_number,
            "webpage_link": link,
            "webpage_title": webpage_title,
            "webpage_description": webpage_description,
        }
        write_to_csv(data)
        serial_number += 1


def main(url):
    print("The program is running...")
    soup = get_soup(url)
    anchor_tags = soup.find_all("a", href=True)
    # Extract and the filter href values
    hrefs = remove_external(remove_hash(get_href_value(anchor_tags)), url)
    full_links = get_full_links(hrefs, url)
    file_name = extract_filename_from_url(url)
    create_csv_file_with_header(file_name)
    add_homepage_to_csv(soup, file_name, url)
    add_all_webpages_to_csv(file_name, full_links)


if __name__ == '__main__':
    url = input('Enter the website URL: ')
    main(url)
