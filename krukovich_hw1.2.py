import requests
import json
from pprint import pprint


url = 'http://ws.audioscrobbler.com/2.0/'
YOUR_API_KEY = '1264758efee9428e5141015ecc08256c'
params = {'method': 'artist.gettoptracks',
          'artist': 'Beyonce',
          'api_key': YOUR_API_KEY,
          'format': 'json'}
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36'}
response = requests.get(url, headers=headers, params=params)
print(response)
top_tracks = response.json()
with open('top_tracks.json', 'w') as f:
    json.dump(response.json(), f)
#pprint(top_tracks)
print(f"Трек № 1 {top_tracks['toptracks']['@attr']['artist']} на сайте last.fm:"
                         f" {top_tracks['toptracks']['track'][0]['name']}")


