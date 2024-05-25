from django.shortcuts import render
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from django.templatetags.static import static
from django.contrib.staticfiles.finders import find

def index(request):
    return render(request, 'myapp/index.html')

def fetch_html(request):
     # Set up Chrome options
    chrome_options = Options()
    chrome_options.add_argument('--headless')  # Run Chrome in headless mode (no GUI)

    # Set up Chrome WebDriver
    chrome_driver_path = find('chromedriver-win64\chromedriver.exe')  # Update with the path to your ChromeDriver 
    service = Service(chrome_driver_path)
    driver = webdriver.Chrome(service=service, options=chrome_options)

    html_content = ""

    try:
        # Navigate to the URL
        url = "https://www.diretodostrens.com.br"
        driver.get(url)

        # Wait for 10 seconds (you can adjust the wait time as needed)
        driver.implicitly_wait(5)

        # Get the HTML content
        html_content = driver.page_source

        # Optionally, you can process the HTML content further here

    finally:
        # Close the WebDriver
        driver.quit()

    soup = BeautifulSoup(html_content, 'html.parser')

    # Extract data from the HTML
    cards = []
    rows = soup.find_all('div', class_='row')
    for row in rows:
        card_elements = row.find_all('div', class_='col-md-4')
        for card_element in card_elements:
            card = {}
            card_header = card_element.find('div', class_='card-header')
            card_title = card_element.find('h5', class_='card-title')
            card_text = card_element.find('p', class_='card-text')
            card_date_element = card_element.find('small')
            if card_date_element:
                card_date = card_date_element.get_text(strip=True)
            else:
                card_date = 'No Date'

            card['header'] = card_header.get_text(strip=True) if card_header else 'No Header'
            card['title'] = card_title.get_text(strip=True) if card_title else 'No Title'
            card['text'] = card_text.get_text(strip=True) if card_text else 'No Text'
            card['date'] = card_date
            
            cards.append(card)

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return render(request, 'myapp/partial_fetch_html.html', {'cards': cards})
    else:
        return render(request, 'myapp/fetch_html.html', {'cards': cards})
