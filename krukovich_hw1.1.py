import requests
import json


url = 'https://api.github.com'
user = 'Krukovicholga'
user_repositories_url = requests.get(f'{url}/users/{user}/repos')
with open('user_repositories.json', 'w') as f:
    json.dump(user_repositories_url.json(), f)
for i in user_repositories_url.json():
    print(i['name'])

#"user_repositories_url": "https://api.github.com/users/{user}/repos{?type,page,per_page,sort}",