import requests
from bs4 import BeautifulSoup
from utils import (
    remove_external,
    remove_hash,
    get_href_value,
    get_merge_links,
    extract_filename_from_url,
    create_csv_file_with_header,
    write_to_csv,
    remove_homepage,
    show_progress
)


HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:127.0) Gecko/20100101 Firefox/127.0'}
filtered_slugs = set()


def get_soup(base_url):
    response = requests.get(base_url, headers=HEADERS)
    return BeautifulSoup(response.text, "html.parser")


def get_webpage_description(soup):
    # Safely get the meta tag with name="description"
    description_tag = soup.find("meta", attrs={"name": "description"})
    return description_tag.get("content") if description_tag else "No description given"


def get_webpage_title(soup):
    # Safely get the title tag value
    title_tag = soup.find("title")
    return title_tag.string if title_tag else "No title found"


def add_homepage_to_csv(file_name, base_url):
    soup = get_soup(base_url)
    data = {
        "file_name": file_name,
        "serial_number": 1,
        "webpage_link": base_url,
        "webpage_title": get_webpage_title(soup),
        "webpage_description": get_webpage_description(soup),
    }
    write_to_csv(data)


def add_all_webpages_to_csv(file_name, links):
    total_links = len(links)
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
        show_progress(total_links, serial_number)
        serial_number += 1


def get_anchor_tags(soup):
    return soup.find_all("a", href=True)


def scrap_pages(full_links):
    """
    * Scrap all pages of the website
    * Merge the relative slug value create absolute link with the user provided base link
    """
    for link in full_links:
        update_filtered_slugs_set(link)
    return get_merge_links(filtered_slugs, base_url)


def update_filtered_slugs_set(link):
    """Get a set and add those new set items to the set"""
    filtered_slugs.update(get_provided_website_slug_only(link))


def get_provided_website_slug_only(base_url):
    """ Returns slug values set
    * Scrap page and collect all anchor tags slug value
    * Remove hashed slug, external slug, and homepage variations slug value
    """
    slugs = get_href_value(get_anchor_tags(get_soup(base_url)))
    return remove_homepage(remove_external(remove_hash(slugs), base_url), base_url)


def main(base_url):
    print("The program is running...")
    update_filtered_slugs_set(base_url)
    homepage_all_links = get_merge_links(filtered_slugs, base_url)
    file_name = extract_filename_from_url(base_url)
    create_csv_file_with_header(file_name)
    add_homepage_to_csv(file_name, base_url)
    website_all_links = scrap_pages(homepage_all_links)
    print(f"Progress: 10%")
    add_all_webpages_to_csv(file_name, website_all_links)
    print(f'Completed! Report file has been created. The file name is {file_name}')


if __name__ == '__main__':
    base_url = input('Enter the website base_url: ').strip().rstrip('/')
    main(base_url)
