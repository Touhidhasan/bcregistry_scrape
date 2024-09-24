import requests
import csv
from bs4 import BeautifulSoup
import captcha_helper  # Import the captcha_helper module
import re

class BCRegistryScraper:
    def __init__(self, input_file, output_file):
        self.input_file = input_file
        self.output_file = output_file
        self.session = requests.Session()

    def read_csv(self):
        with open(self.input_file, 'r', newline='') as csvfile:
            csvreader = csv.reader(csvfile)
            for idx, row in enumerate(csvreader, start=1):
                if row:
                    pincode_search = row[0]
                    print(f"Sl: {idx}")
                    print(pincode_search)
                    self.initialize_output_csv()
                    self.scrape_data(pincode_search)

    def initialize_output_csv(self):
        with open(self.output_file, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(
                ["Name", "Contact number", "Gender", "Bank name", "State", "District", "Block tehsil", "Pincode",
                 "Corporate bc name"])

    def scrape_data(self, pincode_search):
        headers, cookies = self.get_session_headers_cookies()
        captcha_code = captcha_helper.get_captcha_code(self.session, cookies)  # Use the helper function
        bcid_list = captcha_helper.get_bcid_list(self.session, pincode_search, captcha_code, cookies,
                                                 headers)  # Use the helper function

        for bcid in bcid_list:
            self.scrape_bc_details(bcid, cookies, headers)

    def get_session_headers_cookies(self):
        headers = captcha_helper.get_headers()  # Use the helper function
        params = {'doBCPortal': 'yes'}
        response = self.session.get('https://www.bcregistry.org.in/iba/home/HomeAction.do', params=params,
                                    headers=headers, timeout=60)

        jsessionid = response.cookies.get('JSESSIONID')
        print(jsessionid)

        cookies = {
            'JSESSIONID': jsessionid,
            '_ga': 'GA1.1.630088434.1716762037',
            'LTFSESSID': 'thrle8ldc7o4tefcabsag800r3',
            '_ga_Z32Y61C43Q': 'GS1.1.1719821192.10.1.1719821336.0.0.0',
        }
        return headers, cookies

    def scrape_bc_details(self, bcid, cookies, headers):
        data = {'detailcaptcha': 'yes', 'bcid': f'{bcid}'}
        response = self.session.post('https://www.bcregistry.org.in/iba/ajax/getuploadcentre.jsp', cookies=cookies,
                                     headers=headers, data=data, timeout=60)
        print(response.status_code)

        captcha_value = re.search(r"id='txtCaptcha_detail'[^>]*value='([^']*)'", response.text).group(1)
        captcha_code = captcha_value.replace(" ", "")

        data = {
            'bcDetailById': 'yes',
            'bcid': f'{bcid}',
            'cap': f'{captcha_code}',
        }
        response = self.session.post('https://www.bcregistry.org.in/iba/ajax/getuploadcentre.jsp', cookies=cookies,
                                     headers=headers, data=data, timeout=60)
        print(response.status_code)

        self.extract_and_write_data(response.text)

    def extract_and_write_data(self, html_content):
        soup = BeautifulSoup(html_content, 'html.parser')
        name = soup.find('td', text='Name of BC').find_next_sibling('td').text.strip()
        contact_number = soup.find('td', text='Contact Number').find_next_sibling('td').text.strip()
        gender = soup.find('td', text='Gender').find_next_sibling('td').text.strip()
        bank_name = soup.find('td', text='Bank Name').find_next_sibling('td').text.strip()
        state = soup.find('td', text='State').find_next_sibling('td').text.strip()
        district = soup.find('td', text='District').find_next_sibling('td').text.strip()
        block_tehsil = soup.find('td', text='Block / Tehsil').find_next_sibling('td').text.strip()
        pincode = soup.find('td', text='Pincode').find_next_sibling('td').text.strip()
        corporate_bc_name = soup.find('td', text='Corporate BC Name').find_next_sibling('td').text.strip()

        print(
            f"Name: {name}, Contact: {contact_number}, Gender: {gender}, Bank: {bank_name}, State: {state}, District: {district}, Block/Tehsil: {block_tehsil}, Pincode: {pincode}, Corporate BC Name: {corporate_bc_name}")

        with open(self.output_file, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(
                [name, contact_number, gender, bank_name, state, district, block_tehsil, pincode, corporate_bc_name])


if __name__ == "__main__":
    scraper = BCRegistryScraper('input.csv', 'output.csv')
    scraper.read_csv()
    print(f"Data has been written to output.csv")
