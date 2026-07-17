import re
from html.parser import HTMLParser

class TextExtractor(HTMLParser):
    def __init__(self):
        super().__init__()
        self.text = []
        self.skip = False
        self.skip_tags = {'script', 'style', 'noscript', 'iframe', 'svg'}
    def handle_starttag(self, tag, attrs):
        if tag in self.skip_tags:
            self.skip = True
    def handle_endtag(self, tag):
        if tag in self.skip_tags:
            self.skip = False
        if tag in ('p', 'div', 'br', 'li', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6'):
            self.text.append('\n')
    def handle_data(self, data):
        if not self.skip:
            self.text.append(data)
    def get_text(self):
        return ''.join(self.text)

with open('/tmp/csdn_openclaw.html', 'r', encoding='utf-8') as f:
    html_content = f.read()

m = re.search(r'<div[^>]*id="content_views"[^>]*>(.*?)</div>\s*<div[^>]*class="more_toolbox', html_content, re.DOTALL)
if not m:
    m = re.search(r'<div[^>]*id="content_views"[^>]*>(.*)', html_content, re.DOTALL)

if m:
    article_html = m.group(1)
    for marker in ['<div class="more_toolbox', '<div class="toc', '<div id="tree', '<div class="hide-article-box']:
        if marker in article_html:
            article_html = article_html.split(marker)[0]
    
    article_html = re.sub(r'<pre[^>]*>', '\n```\n', article_html)
    article_html = re.sub(r'</pre>', '\n```\n', article_html)
    
    extractor = TextExtractor()
    extractor.feed(article_html)
    text = extractor.get_text()
    text = re.sub(r'\n{3,}', '\n\n', text)
    text = re.sub(r' {2,}', ' ', text)
    text = text.strip()
    
    title_m = re.search(r'<title>([^<]+)</title>', html_content)
    title = title_m.group(1) if title_m else 'Unknown'
    
    print(f"TITLE: {title}")
    print(f"---LENGTH: {len(text)}---")
    # Cut off promotional content
    # Try to find end marker for promotional section
    cut_markers = ['如何学习大模型', 'AI大模型风口已至', 'CSDN官方认证二维码']
    for marker in cut_markers:
        idx = text.find(marker)
        if idx > 2000:  # only cut if marker appears well into the article
            text = text[:idx]
            print(f"CUT at: {marker}, remaining length: {len(text)}")
            break
    print("---FIRST 3000 CHARS---")
    print(text[:3000])
    with open('/tmp/csdn_openclaw_text.txt', 'w', encoding='utf-8') as f:
        f.write(f"TITLE: {title}\n\n{text}")
