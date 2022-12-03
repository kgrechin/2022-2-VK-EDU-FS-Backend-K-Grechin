from bs4 import BeautifulSoup


def remove_tags(text):
    return BeautifulSoup(text, features='html.parser').get_text()
