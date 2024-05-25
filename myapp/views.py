from django.shortcuts import render
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from django import forms
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

class EstimativaForm(forms.Form):
    LINE_CHOICES = [
        ("Linha 4-Amarela", "Linha 4-Amarela"),
        # Add other lines here
    ]
    
    line = forms.ChoiceField(choices=LINE_CHOICES, label="Line")
    station = forms.ChoiceField(choices=[], label="Station")

    def __init__(self, *args, **kwargs):
        line_stations = kwargs.pop('line_stations', {})
        super(EstimativaForm, self).__init__(*args, **kwargs)
        if 'line' in self.data:
            self.fields['station'].choices = [(station, station) for station in line_stations.get(self.data['line'], [])]

def estimativa_html(request):
    lines = {
        "Linha 4-Amarela": [
            "Vila Sônia", "São Paulo - Morumbi", "Butantã", "Pinheiros",
            "Faria Lima", "Fradique Coutinho", "Oscar Freire", "Paulista",
            "Higienopolis - Mackenzie", "República", "Luz"
        ],
        # Add other lines and their stations here
    }

    if request.method == 'POST':
        form = EstimativaForm(request.POST, line_stations=lines)
        if form.is_valid():
            line_selected = form.cleaned_data['line']
            station_selected = form.cleaned_data['station']

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

                # Wait for the page to load
                driver.implicitly_wait(5)

                # Get the HTML content
                html_content = driver.page_source

            finally:
                # Close the WebDriver
                driver.quit()

            # Parse the HTML content with BeautifulSoup
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

            station_times = {
                "Linha 4-Amarela": {
                    "Vila Sônia": 1, "São Paulo - Morumbi": 1, "Butantã": 3, "Pinheiros": 1,
                    "Faria Lima": 1, "Fradique Coutinho": 1, "Oscar Freire": 1, "Paulista": 1,
                    "Higienopolis - Mackenzie": 1, "República": 1, "Luz": 1
                },
                # Add other lines and their stations here
            }

            estimated_time = station_times[line_selected][station_selected]

            # Adjust estimated time based on card headers
            for card in cards:
                if station_selected in card['title'] and card['header'] != "Operação Normal":
                    estimated_time += 2  # Add extra time if there's a disruption

            context = {
                'line': line_selected,
                'station': station_selected,
                'time': estimated_time,
                'form': form,
            }
            return render(request, 'estimativa.html', context)

    else:
        form = EstimativaForm(line_stations=lines)

    return render(request, 'estimativa.html', {'form': form, 'lines': lines})