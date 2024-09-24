# BC Registry Scraper

## Overview

The **BC Registry Scraper** is a Python script designed to scrape BC Registry data based on pincodes provided in an input CSV file. It automates the process of fetching details like Name, Contact Number, Gender, Bank Name, and more from the BC Registry website and stores the data in an output CSV file.

## Features

- **Pincode Search**: Automatically fetches BC (Business Correspondent) details for each pincode provided in the input file.
- **Captcha Handling**: Utilizes a helper function to handle and bypass captchas.
- **Session Management**: Uses session cookies for maintaining persistent connections.
- **Data Extraction**: Extracts details such as Name, Contact, Gender, Bank, State, District, etc., from the BC Registry website.
- **CSV Output**: Writes the extracted data into an organized CSV file.

## Challenge: Solving Captcha Using Reverse Engineering

A significant challenge in scraping data from the BC Registry website is solving the CAPTCHA, which is necessary to access the data. The solution implemented involves **reverse engineering** the captcha mechanism by analyzing the requests, responses, and captcha generation process from the website's source code.

### Sourcing URL:
- URL: [https://www.bcregistry.org.in/iba/home/HomeAction.do?doBCPortal=yes](https://www.bcregistry.org.in/iba/home/HomeAction.do?doBCPortal=yes)

By reverse-engineering the captcha request-response flow and extracting the necessary token, this solution automates the process of retrieving the captcha code and submitting it with the form data to access the BC Registry details.

## Requirements

- Python 3.x
- Python Libraries:
  - `requests`
  - `lxml`
  - `beautifulsoup4`
  - `csv`
  - `re`

Install the required libraries using:

```bash
pip install -r requirements.txt
