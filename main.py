import requests, json
from tqdm import tqdm
from typing import Dict, Union


json_fn = "database"


def read_databae(database_id, headers, save=True) -> Union[Dict, None]:
    url = f"https://api.notion.com/v1/databases/{database_id}/query"
    payload = {"page_size": 1000}
    res = requests.request("POST", url, json=payload, headers=headers)
    data = res.json()
    print(len(data['results']))

    if save:
        with open(f'./{json_fn}.json', 'w', encoding='utf8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
    else:
        return data


def update_database(database_id, headers):
    
    db_data = read_databae(database_id, headers, save=False)
    pages = db_data['results']

    with tqdm(total=len(pages), desc='Updating') as pbar:
        for page in pages:
            page_url = f"https://api.notion.com/v1/pages/{page['id']}"
            payload = {
                "icon": {
                    "type": "external",
                    "external": {
                        "url": "https://raw.githubusercontent.com/eirikmadland/notion-icons/master/v5/icon3/ul-label-alt.svg"
                    }
                }
            }
            response = requests.request("PATCH", page_url, json=payload, headers=headers)
            if response.status_code != 200:
                print(f"Error updating page {page['id']}")
            
            pbar.update(1)


if __name__ == "__main__":
    with open('token.txt', encoding='utf8') as f:
        api_token = f.readline()
    
    database_id = "213bac35fee64ef3b67a1c4e40ab7a4b"

    headers = {
        "Accept": "application/json",
        "Notion-Version": "2021-08-16",
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_token}"
    }

    update_database(database_id, headers)
