import requests
from bs4 import BeautifulSoup


def get_soup(url:str) -> BeautifulSoup:
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')

    return soup


def get_links(soup:BeautifulSoup) -> list:
    ls = []
    try:
        title = soup.find_all('h1')[0].get_text()
    except:
        title = "OPS"

    for a in soup.find_all('a'):
        try:
            link = a['href']
            if link[0] != '#':
                ls.append(a['href'])
        except:
            continue

    return (ls, title)


def go_url(url:str) -> str:
    return url if url[0] != '/' else "https://pt.wikipedia.org" + url


def check_limits(url:str):
    if url[:20] == "https://pt.wikipedia":
      return url
    else:
      raise "Fora dos limites da wiki pt"


def check(title:str, target:str) -> bool:
    return True if title.lower().replace(' ', '') == target.lower().replace(' ', '') else False


class Node(object):
    def __init__(self, url: str, parent = None):
        self.url = url
        self.parent = parent


def print_strategy(title: str , url: str):
    print("passando por: " + str(title) + " url: " + str(url))


def bfs(node: Node, target: str, log_strategy):
    memo = {}
    queue = []
    current = node
    queue.append(current)
    while not len(queue) == 0:
        front = queue.pop(0)
        memo[front.url] = True
        try:
            links, title = get_links(get_soup(check_limits(front.url)))
            log_strategy(title, front.url)
        except:
            continue
        if check(title, target):
            return front
        for link in links:
            link = go_url(link)
            try:
                if memo[link] == True:
                    continue
            except:
                memo[link] = True
                node = Node(link, front)
                queue.append(node)

    return None

path = bfs(Node("https://pt.wikipedia.org/wiki/Wikip%C3%A9dia:P%C3%A1gina_principal"), "Roma", print_strategy)
