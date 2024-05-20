import requests
from bs4 import BeautifulSoup


def get_soup(url):
    response = requests.get(url)
    return BeautifulSoup(response.text, "html.parser")

def main(url):
    print("The program is running...")
    soup = get_soup(url)
    anchor_tags = soup.find_all("a", href=True)


if __name__ == '__main__':
    url = input('Enter the website URL: ')
    main(url)
