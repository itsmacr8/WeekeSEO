from urllib.parse import urlparse


def get_href_value(anchor_tags):
    return [anchor_tag["href"] for anchor_tag in anchor_tags]

def remove_hash(hrefs):
    """Internal links with '#' in the links
    * '#service' not '/services'
    * '/blogs#blog-1' not '/blogs'
    """
    return [href for href in hrefs if "#" not in href]

def remove_external(hrefs, url):
    return [href for href in hrefs if href.startswith(url) or href.startswith("/")]

def get_full_links(hrefs, url):
    """ If the href starts with absolute url then continue or if it starts with
    relative href then add url+href to make it absolute."""
    return [f"{url}{href}" if not href.startswith("http") else href for href in hrefs]

def extract_filename_from_url(url):
    """ Extract the domain name from the url to use it as filename """
    parsed_url = urlparse(url)
    netloc_parts = parsed_url.netloc.split(".")
    return netloc_parts[-2] if len(netloc_parts) >= 2 else netloc_parts[-1]
