import json
import os
import requests
import time
import sys

def download_file(url, file_name):
    resp = requests.get(url=url)
    with open(file_name, "wb") as f:
        f.write(resp.content)
        

def get_org_id(code):
    query_url = 'http://www.cninfo.com.cn/new/information/topSearch/query?keyWord={}&maxNum=10'
    resp = requests.post(url=query_url.format(code))
    assert(resp.ok)
    
    results = json.loads(resp.content)
    for r in results:
        if r.get('category') == 'A股':
            return r['orgId']
        
    print('Could not find orgId for {}'.format(code))
    
    
def get_announcements(code):
    query_url = 'http://www.cninfo.com.cn/new/hisAnnouncement/query'
    
    org_id = get_org_id(code)
    payload = {"stock": "{},{}".format(code, org_id), "category": "category_ndbg_szsh;", "tabName": "fulltext"}
    
    resp = requests.post(url=query_url, data=payload)
    assert(resp.ok)
    
    result = json.loads(resp.content)
    
    return result["announcements"]


def download_annual_reports(code):
    download_url = 'http://static.cninfo.com.cn/{}'
    path = '/Users/yuzifeng/GitHub/stock/notebook'   
    
    announcements = get_announcements(code)
    
    if len(announcements) == 0:
        print('Nothing to download')
        return
    
    sec_name = announcements[0]['secName'].replace(' ', '')
    path = os.path.join(path, '{} {}'.format(code, sec_name))
    if not os.path.exists(path):
        print("Create folder {}".format(path))
        os.makedirs(path)
        
    for report in announcements:
        title = report['announcementTitle']
        file_path = os.path.join(path, title + '.pdf')
        if '年度报告' in title and '摘要' not in title and '财务' not in title and not os.path.exists(file_path):
            print('Download {}'.format(file_path))
            download_file(download_url.format(report['adjunctUrl']), file_path)
            time.sleep(1)
        
    print('Download finished.')
    

if __name__ == '__main__':
    assert(get_org_id('600858') == 'gssh0600858')
    assert(len(sys.argv) == 2)    
    download_annual_reports(sys.argv[1])    
