# captcha_helper.py
import re
from lxml import html

def get_captcha_code(session, cookies):
    headers = get_headers()
    data = {'type': '3'}
    response = session.post(
        'https://www.bcregistry.org.in/iba/ajax/home/captchasession.jsp',
        cookies=cookies,
        headers=headers,
        data=data,
        timeout=60
    )
    print(response.status_code)
    return response.text.replace(" ", "")

def get_bcid_list(session, pincode_search, captcha_code, cookies, headers):
    params = {'doBCPortal': 'yes'}
    data = {
        'doBCPortal': 'yes',
        'searchType': '4',
        'pincode': f'{pincode_search}',
        'cap_search': f'{captcha_code}',
    }

    response = session.post(
        'https://www.bcregistry.org.in/iba/home/HomeAction.do',
        params=params,
        cookies=cookies,
        headers=headers,
        data=data,
        timeout=60
    )
    print(response.status_code)

    tree = html.fromstring(response.content)
    bcid_text_list = tree.xpath('//table[@class="table table-hover table-light"]/tbody/tr/td[@class="bc_name"]/a/@href')
    bcid_list = [re.search(r"'(\d+)'", bcid_text).group(1) for bcid_text in bcid_text_list if re.search(r"'(\d+)'", bcid_text)]
    return bcid_list

def get_headers():
    return {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Language': 'en-US,en;q=0.9',
        'Connection': 'keep-alive',
        'Content-Type': 'application/x-www-form-urlencoded',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
    }
