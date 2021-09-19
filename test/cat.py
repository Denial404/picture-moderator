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

'''
[{'breeds': [], 'id': '24u', 'url': 'https://24.media.tumblr.com/tumblr_lhug35i9EB1qfyzelo1_250.jpg', 'width': 400, 'height': 564}, {'breeds': [], 'categories': [{'id': 1, 'name': 'hats'}], 'id': '39r', 'url': 'https://24.media.tumblr.com/tumblr_lsctmjkgZL1qdvbl3o1_250.jpg', 'width': 1024, 'height': 680}, {'breeds': [], 'id': '4h4', 'url': 'https://cdn2.thecatapi.com/images/4h4.gif', 'width': 500, 'height': 281}, {'breeds': [], 'id': '5rp', 'url': 'https://24.media.tumblr.com/tumblr_ln3twtMmvE1qbt33io1_250.jpg', 'width': 420, 'height': 587}, {'breeds': [], 'id': '9pj', 'url': 'https://25.media.tumblr.com/tumblr_m2o51zVZpc1qd477zo1_250.jpg', 'width': 400, 'height': 300}, {'breeds': [], 'id': 'b23', 'url': 'https://25.media.tumblr.com/tumblr_m1729uw6Pf1qz5dg8o1_250.jpg', 'width': 640, 'height': 426}, {'breeds': [], 'id': 'bdq', 'url': 'https://24.media.tumblr.com/tumblr_lhd7ouWse91qgnva2o1_250.jpg', 'width': 500, 'height': 334}, {'breeds': [], 'id': 'XvrmhmEoP', 'url': 'https://cdn2.thecatapi.com/images/XvrmhmEoP.jpg', 'width': 3547, 'height': 1995}, {'breeds': [], 'id': 'DFe66Y-lt', 'url': 'https://cdn2.thecatapi.com/images/DFe66Y-lt.jpg', 'width': 1265, 'height': 951}, {'breeds': [], 'id': 'vCGSc-o44', 'url': 'https://cdn2.thecatapi.com/images/vCGSc-o44.png', 'width': 2232, 'height': 1920}]
'''