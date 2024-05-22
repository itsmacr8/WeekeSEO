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


def get_soup(user_provided_url):
    response = requests.get(user_provided_url)
    return BeautifulSoup(response.text, "html.parser")


def get_webpage_description(soup):
    # Safely get the meta tag with name="description"
    description_tag = soup.find("meta", attrs={"name": "description"})
    return description_tag.get("content") if description_tag else "No description given"


def get_webpage_title(soup):
    # Safely get the title tag value
    title_tag = soup.find("title")
    return title_tag.string if title_tag else "No title found"


def add_homepage_to_csv(file_name, user_provided_url):
    soup = get_soup(user_provided_url)
    data = {
        "file_name": file_name,
        "serial_number": 1,
        "webpage_link": user_provided_url,
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


def remove_homepage(hrefs):
    """We use set because of performance"""
    homepage_variations = {
        '/',
        './',
        './index.php',
        './index.html',
        './index.htm',
        'index.php',
        'index.html',
        'index.htm',
        user_provided_url,
        f'{user_provided_url}/'
    }
    hrefs -= homepage_variations
    return hrefs


def get_anchor_tags(soup):
    return soup.find_all("a", href=True)


def scrap_pages(full_links, hrefs):
    """
    * Scrap all pages of the website
    * Merge the relative href value create absolute link with the user provided base link
    """
    for link in full_links:
        hrefs.update(get_provided_website_href_only(link))
    return get_full_links(hrefs, user_provided_url)


def get_provided_website_href_only(user_provided_url):
    """ Returns href values set
    * Scrap page and collect all anchor tags href value
    * Remove hashed href, external href, and homepage variations href value
    """
    href_value = get_href_value(get_anchor_tags(get_soup(user_provided_url)))
    return remove_homepage(remove_external(remove_hash(href_value), user_provided_url))


def main(user_provided_url):
    print("The program is running...")
    hrefs = set()
    hrefs.update(get_provided_website_href_only(user_provided_url))
    full_links = get_full_links(hrefs, user_provided_url)
    website_all_links = scrap_pages(full_links, hrefs)
    file_name = extract_filename_from_url(user_provided_url)
    create_csv_file_with_header(file_name)
    add_homepage_to_csv(file_name, user_provided_url)
    add_all_webpages_to_csv(file_name, website_all_links)

if __name__ == '__main__':
    user_provided_url = input('Enter the website user_provided_URL: ')
    main(user_provided_url)
