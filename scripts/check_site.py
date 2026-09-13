"""Dependency-free checks for local links and portable static pages."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit, unquote
import sys

ROOT = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else Path(__file__).resolve().parents[1]


class Page(HTMLParser):
    def __init__(self, path):
        super().__init__(convert_charrefs=True)
        self.links, self.ids, self.tags, self.current = [], set(), [], []
        self.description = False
        self.feed(path.read_text())

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        self.tags.append(tag)
        if 'id' in attrs:
            assert attrs['id'] not in self.ids, 'Duplicate ID'
            self.ids.add(attrs['id'])
        for key in ('href', 'src'):
            if key in attrs:
                self.links.append(attrs[key])
        if attrs.get('aria-current') == 'page':
            self.current.append(attrs.get('href'))
        if tag == 'meta' and attrs.get('name') == 'description':
            self.description = bool(attrs.get('content'))
        if tag == 'img':
            assert attrs.get('alt'), 'Missing image alternative text'


pages = {p.name: Page(p) for p in ROOT.glob('*.html')}
assert set(pages) == {'index.html', 'publications.html', 'contact.html'}
for name, page in pages.items():
    assert page.tags.count('h1') == 1, name
    assert page.tags.count('main') == 1, name
    assert page.description and 'title' in page.tags, name
    assert page.current == [name], (name, page.current)
    for link in page.links:
        assert 'YOUR_ID' not in link, (name, link)
        url = urlsplit(link)
        if url.scheme or url.netloc:
            continue
        assert not url.path.startswith('/'), (name, 'Root-relative URL', link)
        target = unquote(url.path) or name
        assert (ROOT / target).is_file(), (name, 'Missing file', link)
        if url.fragment:
            assert target in pages and unquote(url.fragment) in pages[target].ids, (name, 'Missing anchor', link)
print(f'PASS: {len(pages)} pages; local assets, links, anchors, metadata, navigation, and relative paths.')
