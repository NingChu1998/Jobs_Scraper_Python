import csv
from datetime import datetime
import requests
from bs4 import BeautifulSoup

base_url = 'https://www.indeed.com'

# This get_url function with the arguments of position and location
def get_url(position, location):
    template ='https://www.indeed.com/jobs?q={}&l={}'
    url = template.format(position, location)
    return url

#Extract job datas from a single record
def get_record(card):
    job_id = card.get("href")
    title = card.find('span', title=True).text.strip()
    company = card.find('span', class_='companyName').text.strip()
    location = card.find('div', class_='companyLocation').text.strip()
    posted = card.find('span', class_='date').text.strip()
    job_link = base_url + job_id
    summary = card.find('div', 'job-snippet').text.strip().replace('\n'," ")
    try:
        job_salary =card.find('div','attribute_snippet').text.strip()
    except AttributeError:
        job_salary = " "
    record = (title, company, location, posted, summary, job_salary,job_link)
    return record

def main(position, location):
    """Run the main program routine"""
    records = []
    url = get_url(position, location)

    while True:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        base_url = 'https://www.indeed.com'
        d = soup.find('div', attrs={'id': 'mosaic-provider-jobcards'})
        cards = soup.find_all('a', class_='tapItem')

        for card in cards:
            record = get_record(card)
            records.append(record)

        try:
            url = base_url + soup.find('a',{'aria-label':"Next"}).get('href')
        except AttributeError:
            break
    # Save the data
    # print(records[0])
    with open('results.csv','w',newline='',encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['title', 'company', 'location', 'posted', 'summary', 'job_salary','job_link'])
        writer.writerows(records)

# Let's run this
print("Hi, there!")
position = input('Enter job title, keywords, company or Exit: ')
while position != 'Exit':
    location = input('Enter city or postcode: ')
    try:
        print('Downloading... Please wait for a few minutes if the file is too heavy')
        main(position, location)
        print('Check Your results.csv Now!')
    except:
        print('Err...Retry it again!')
    position = input('Enter job title, keywords, company or Exit: ')
print('Thank you! Hope you find a great job!👍🏻')


