import requests
import bs4

def get_bonds_at(date):
    """
    Input: date yyyy-mm-dd
    """
    
    year = date[:4]
    day = date[5:7] + date[8:10]
    
    url = 'http://bond.jrj.com.cn/quote/' + year + '/' + day + '/zqhq.html'
    resp = requests.get(url)
    if resp.status_code == 200:
        soup = bs4.BeautifulSoup(resp.text)
        items = soup.select('table tr')
        for item in items:
            rows = item.select('td')
            if size(rows) == 10:
                id = str(item.select('td.w2 a')[0].text)
                

    


