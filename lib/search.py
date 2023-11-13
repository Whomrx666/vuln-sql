import contextlib
import threading
from queue import Queue
from requests_html import HTMLSession


class Search:
    base_url = 'https://bing.com'
    parameters = '/search?q={}'

    def __init__(self, query):
        self.query = query

        self.is_alive = True
        self.is_searching = True

        self.links = Queue()

        self.lock = threading.RLock()

    def next_page(self, html):
        with contextlib.suppress(Exception):
            a = html.find('.b_pag', first=True).find('.b_widePag')
            return self.base_url + a[-1].attrs['href']

    def is_valid(self, link):

        return '=' in link

    def find_links(self):

        session = HTMLSession()
        session.headers[
            'user-agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36'

        url = self.base_url + self.parameters.format(self.query)

        while self.is_alive:
            try:
                html = session.get(url).html
            except Exception:
                break

            for r in html.find('.b_algo'):
                a = r.find('h2', first=True).find('a', first=True)

                try:
                    link = a.attrs['href']
                except Exception:
                    continue

                if self.is_valid(link):
                    self.links.put(link)

            if next_page := self.next_page(html):
                url = next_page

            else:
                break

        with self.lock:
            self.is_searching = False

    def get_link(self):
        if self.links.qsize():
            return self.links.get()

    def start(self):

        self.find_links()

    def is_active(self):

        with self.lock:
            is_searching = self.is_searching

        return bool(is_searching or self.links.qsize() > 0)

    def stop(self):
        self.is_alive = False
