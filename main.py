import requests, json


json_fn = "database"


def read_databae(database_id, headers):
    url = f"https://api.notion.com/v1/databases/{database_id}/query"
    payload = {"page_size": 100}
    res = requests.request("POST", url, json=payload, headers=headers)
    data = res.json()

    with open(f'./{json_fn}.json', 'w', encoding='utf8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


def update_database(database_id, headers):
    url = f"https://api.notion.com/v1/databases/{database_id}"

    with open(f'{json_fn}.json', encoding="utf-8") as json_file:
        data = json.load(json_file) 

    for page in data['results']:
        page['icon'] = {'type': 'external', 'external': {'url': 'https://raw.githubusercontent.com/eirikmadland/notion-icons/master/v5/icon3/mi-basket-ball.svg'}}
    data = json.dumps(data)
    response = requests.request("PATCH", url, headers=headers, data=data)

    print(response.text)


if __name__ == "__main__":
    with open('token.txt', encoding='utf8') as f:
        api_token = f.readline()
    
    database_id = "54806c81a3234dc899af940be2dbdf53"

    headers = {
        "Accept": "application/json",
        "Notion-Version": "2021-08-16",
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_token}"
    }

    read_databae(database_id, headers)
    #update_database(database_id, headers)
