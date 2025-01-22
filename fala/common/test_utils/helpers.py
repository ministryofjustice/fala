import bs4


def parse_html(content):
    return bs4.BeautifulSoup(content, "html.parser")


def find_element(html, tag, class_):
    return html.find(tag, class_=class_)
