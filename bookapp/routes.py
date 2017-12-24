from flask import render_template
import re
from bs4 import BeautifulSoup
from bookapp import app


def parse_htmlbook(page):
    links = get_chap_links(page)
    sections = {}
    for ind in range(len(links)):
        section = {}
        start = links[ind]
        if ind < len(links)-1:
            end = links[ind+1]
            patt = ('<a name="{}"></a>(.*)' + '<a name="{}"></a>').format(start,end)
            match = re.search(patt,page,re.MULTILINE|re.DOTALL)
            if match == None:
                raise Exception('patt: '+patt+'\n\n')
        else:
            patt = '<a name="{}"></a>(.*)<pre>'.format(start)
            match = re.search(patt,page,re.MULTILINE|re.DOTALL)
        if match:
            soup = BeautifulSoup(match.group("sectionbody"), 'html.parser')
            plist = [p.contents[0] for p in soup.find_all('p')]
            section['title']= (soup.find('h3').contents)[0]
            section['plist']= plist
            sections[start] = section
    return links, sections



def get_chap_links(page):
    soup = BeautifulSoup(page)
    links = [str(link.get('href'))[1:]
             for link in soup.find_all('a') if link.get('href')]
    return links


@app.route('/')
def index():
    page = render_template('senseandsensibility.html')
    links, sections = parse_htmlbook(page)
    chapter = len(links)
    title = "Sense and Sensibility by Jane Austen"
    section = []
    for i in range(chapter):
        section.append(str(sections[links[i]]['title']))

    print(str(chapter))
    print(section)
    return render_template('index.html', value='Hello World!')
