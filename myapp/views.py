from django.shortcuts import render
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from django import forms
from django.templatetags.static import static
from django.contrib.staticfiles.finders import find
from django.http import JsonResponse

def index(request):
    return render(request, 'myapp/index.html')

def fetch_html(request):
    # Set up Chrome options
    chrome_options = Options()
    chrome_options.add_argument('--headless')  # Run Chrome in headless mode (no GUI)

    # Set up Chrome WebDriver
    chrome_driver_path = find('chromedriver-win64\chromedriver.exe')
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
                card_date_text = card_date_element.get_text(strip=True)
                # Find the indices of the date and update text
                ocorrencia_index = card_date_text.find("Data da Ocorrência:")
                atualizacao_index = card_date_text.find("Última Atualização:")
                
                if ocorrencia_index != -1 and atualizacao_index != -1:
                    data_ocorrencia = card_date_text[ocorrencia_index + len("Data da Ocorrência:"):atualizacao_index].strip()
                    ultima_atualizacao = card_date_text[atualizacao_index + len("Última Atualização:"):].strip()
                else:
                    data_ocorrencia = 'No Date'
                    ultima_atualizacao = 'No Date'
            else:
                data_ocorrencia = 'No Date'
                ultima_atualizacao = 'No Date'
    
            card['header'] = card_header.get_text(strip=True) if card_header else 'No Header'
            card['title'] = card_title.get_text(strip=True) if card_title else 'No Title'
            card['text'] = card_text.get_text(strip=True) if card_text else 'No Text'
            card['data_ocorrencia'] = data_ocorrencia
            card['ultima_atualizacao'] = ultima_atualizacao
    
            cards.append(card)

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return render(request, 'myapp/partial_fetch_html.html', {'cards': cards})
    else:
        return render(request, 'myapp/fetch_html.html', {'cards': cards})

''' Estimativas '''

def estimativa_html(request):
    # Predefined station times for different lines
    lines = {
        "Linha 4-Amarela": {
            "Vila Sônia": 1, "São Paulo - Morumbi": 1, "Butantã": 3, "Pinheiros": 1,
            "Faria Lima": 1, "Fradique Coutinho": 1, "Oscar Freire": 1, "Paulista": 1,
            "Higienopolis - Mackenzie": 1, "República": 1, "Luz": 1
        },
        # Add other lines and their stations here
    }

    if request.method == 'POST':
        line_selected = request.POST.get('line')
        start_station = request.POST.get('start_station')
        end_station = request.POST.get('end_station')

        if line_selected in lines and start_station in lines[line_selected] and end_station in lines[line_selected]:
            # Calculate estimated time
            start_index = list(lines[line_selected].keys()).index(start_station)
            end_index = list(lines[line_selected].keys()).index(end_station)
            estimated_time = sum(list(lines[line_selected].values())[start_index:end_index+1])

            # Set up Chrome options
            chrome_options = Options()
            chrome_options.add_argument('--headless')  # Run Chrome in headless mode (no GUI)

            # Set up Chrome WebDriver
            chrome_driver_path = find('chromedriver-win64\chromedriver.exe')
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
                        card_date_text = card_date_element.get_text(strip=True)
                        # Find the indices of the date and update text
                        ocorrencia_index = card_date_text.find("Data da Ocorrência:")
                        atualizacao_index = card_date_text.find("Última Atualização:")

                        if ocorrencia_index != -1 and atualizacao_index != -1:
                            data_ocorrencia = card_date_text[ocorrencia_index + len("Data da Ocorrência:"):atualizacao_index].strip()
                            ultima_atualizacao = card_date_text[atualizacao_index + len("Última Atualização:"):].strip()
                        else:
                            data_ocorrencia = 'No Date'
                            ultima_atualizacao = 'No Date'
                    else:
                        data_ocorrencia = 'No Date'
                        ultima_atualizacao = 'No Date'

                    card['header'] = card_header.get_text(strip=True) if card_header else 'No Header'
                    card['title'] = card_title.get_text(strip=True) if card_title else 'No Title'
                    card['text'] = card_text.get_text(strip=True) if card_text else 'No Text'
                    card['data_ocorrencia'] = data_ocorrencia
                    card['ultima_atualizacao'] = ultima_atualizacao

                    cards.append(card)

            filtered_cards = [card for card in cards if card['header'] == 'Linha 4-Amarela']
            
            if filtered_cards and filtered_cards[0]['text'] != "Operação Normal":
               estimated_time += 10

            return JsonResponse({'line': line_selected, 'start_station': start_station, 'end_station': end_station, 'time': estimated_time})

    return render(request, 'myapp/estimativa_html.html', {'lines': lines})