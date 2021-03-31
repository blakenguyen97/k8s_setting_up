import json
import requests
# import cv2

if __name__ == "__main__":
    
    url = 'https://wowza02.giamsat247.vn:4935/live/ctx-33.stream/playlist.m3u8'
    url_id = '4970'
    
    data = {'URL' : url, 'URL_ID' : url_id}
    r = requests.post('http://118.69.19.121:30009' + '/start', params=data)
    data = r.text
    print(data)
