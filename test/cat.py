import json
import requests
import os

CAT_URL = 'https://api.thecatapi.com/v1/images/search'

headers = {
    'X-API-KEY': os.getenv('CAT')
}

'''
params = {
    'size': 'small',
    'limit': 10
}
'''

query_url = f'{CAT_URL}?limit=10&size=small'
res = requests.get(query_url, headers=headers)
print(res.request.headers)
res_content = json.loads(res.content)
print(res_content)