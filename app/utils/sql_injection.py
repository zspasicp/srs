import requests as req
from utils.levenshtein_distance import similarity

injection_patterns = ["'", "'or1=1;#"]

initial_vulnerable_key_words = ['sql', 'database', 'odbc']


def test_for_eql_injection():
    return "RESULT of SQL injection"


def inject_url(url: str):
    vulnerable_key_word = []
    resp = req.get(url)
    #print(resp.text)
    html1 = resp.text
    for kw in initial_vulnerable_key_words:
        if kw not in html1:
            vulnerable_key_word.append(kw)
    for ip in injection_patterns:
        resp = req.get(url)
        #print(resp.text)
        html2 = resp.text
        # for kw in vulnerable_key_word:
            # if kw in html2:
                # return True
    print(similarity(html1, html2))
    
    
    
if __name__ == '__main__':
    inject_url('https://stackoverflow.com/questions/2349991/how-to-import-other-python-files')