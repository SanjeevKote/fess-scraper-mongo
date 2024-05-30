from bs4 import BeautifulSoup 
import requests   
import re
import json

def get_date(url):
    response = requests.get(url)
    # Parse the HTML content
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Extract the publication date from <meta> tags
    publication_date = None
    
    #Find the script tag within the div with id 'datalayerdiv'
    div = soup.find('div', {'id': 'datalayerdiv'})
    if not div:
        print("Div with id 'datalayerdiv' not found.")
        return

    script_tag = div.find('script')
    if not script_tag:
        print("Script tag within the div not found.")
        return

    # Extract the script content
    script_content = script_tag.string
    if not script_content:
        print("Script content is empty.")
        return

    # Adjust the regex to match JSON object more accurately
    json_data_match = re.search(r'dataLayer\.page\s*=\s*(\{(?:.|\n)*?\});', script_content)
    if not json_data_match:
        print("JSON data not found in script content.")
        return

    json_data = json_data_match.group(1)
    # Parse the JSON data
    try:
        data = json.loads(json_data)
        print('data',data)
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")

    # Extract the dates
    create_date = data['attributes']['createDate']
    publish_date = data['attributes']['publishDate']


    publication_date=create_date
    return publication_date
    