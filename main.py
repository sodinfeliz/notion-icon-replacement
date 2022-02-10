import requests, json
from tqdm import tqdm
from typing import Dict, Union


json_fn = "database"


def read_database(database_id, headers, start_cursor: str=None) -> Union[Dict, None]:
    url = f"https://api.notion.com/v1/databases/{database_id}/query"
    if start_cursor is not None:
        payload = {"start_cursor": start_cursor}
    else:
        payload = {"page_size": 100}

    res = requests.request("POST", url, json=payload, headers=headers)
    if res.status_code != 200:
        res = res.json()
        if "path failed validation" in res["message"]:
            print("Invalid database id")

        return False
    else:
        return res.json()


def update_database(database_id: str, headers: dict, image_url: str):
    
    has_more = True
    start_cursor = None

    while has_more:
        db_data = read_database(database_id, headers, start_cursor=start_cursor)
        if db_data is False: break

        with tqdm(total=len(db_data['results']), desc='Updating') as pbar:
            for page in db_data['results']:
                page_url = f"https://api.notion.com/v1/pages/{page['id']}"
                payload = {
                    "icon": {
                        "type": "external",
                        "external": {
                            "url": image_url
                        }
                    }
                }
                response = requests.request("PATCH", page_url, json=payload, headers=headers)
                if response.status_code != 200:
                    print(f"Error updating page {page['id']}")
                
                pbar.update(1)

        has_more = db_data['has_more']
        start_cursor = db_data['next_cursor']


if __name__ == "__main__":
    with open('token.txt', encoding='utf8') as f:
        api_token = f.readline()

    database_id = input("Enter database id: ")
    image_url = input("Enter image url: ")

    headers = {
        "Accept": "application/json",
        "Notion-Version": "2021-08-16",
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_token}"
    }

    update_database(database_id, headers, image_url)
