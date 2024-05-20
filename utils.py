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
