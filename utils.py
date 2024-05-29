from urllib.parse import urlparse
import csv
from math import ceil


def get_href_value(anchor_tags):
    return {anchor_tag["href"] for anchor_tag in anchor_tags}

def remove_hash(slugs):
    """Internal links with '#' in the links
    * '#service' not '/services'
    * '/blogs#blog-1' not '/blogs'
    """
    return {slug for slug in slugs if "#" not in slug}

def remove_external(slugs, url):
    return {slug for slug in slugs if slug.startswith(url) or slug.startswith("/")}


def remove_homepage(slugs, url):
    homepage_variations = {
        "/",
        "./",
        "./index.php",
        "./index.html",
        "./index.htm",
        "index.php",
        "index.html",
        "index.htm",
        url,
        f"{url}/",
    }
    slugs -= homepage_variations
    return slugs


def get_merge_links(slugs, url):
    """If the slug starts with absolute url then continue or if it starts with
    relative slug then add url+slug to make it absolute. For example
    * url/blog/ then keep it as it is.
    * /blog/ then make it like url/blog/
    """
    return [f"{url}{slug}" if not slug.startswith("http") else slug for slug in slugs]


def extract_filename_from_url(url):
    """ Extract the domain name from the url to use it as filename """
    parsed_url = urlparse(url)
    netloc_parts = parsed_url.netloc.split(".")
    return netloc_parts[-2] if len(netloc_parts) >= 2 else netloc_parts[-1]


def create_csv_file_with_header(file_name):
    try:
        with open(f"{file_name}.csv", mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["SL No", "Links", "Title Tag", "Meta Description"])
    except Exception as e:
        print(f"An error occurred: {e}")


def write_row(file, data):
    writer = csv.writer(file)
    sl = data["serial_number"]
    link = data["webpage_link"]
    title = data["webpage_title"]
    description = data["webpage_description"]
    writer.writerow([sl, link, title, description])


def write_to_csv(data):
    try:
        with open(
            f'{data["file_name"]}.csv', mode="a", newline="", encoding="utf-8"
        ) as file:
            write_row(file, data)
    except Exception as e:
        print(f"An error occurred: {e}")

def show_progress(total_num, num):
    increment = ceil(total_num / 10)
    if num % increment == 0:
        progress_percentage = int(ceil((num / total_num) * 100 / 10) * 10)
        print(f"Progress: {progress_percentage}%")
