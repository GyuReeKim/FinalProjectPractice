# base_url = 'https://www.googleapis.com/youtube/v3/search'
# key = 'AIzaSyAeap5unk6t-txCBkaWbJYN9aa04THfCx0'
# youtube_url = f'{base_url}?key={key}'

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from oauth2client.tools import argparser

DEVELOPER_KEY = "AIzaSyAeap5unk6t-txCBkaWbJYN9aa04THfCx0"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey = DEVELOPER_KEY)

search_response = youtube.search().list(
    q = "겨울왕국",
    part = "snippet",
    maxResults = 1
).execute()

search_response.get('items')[0].get('id').get('videoId')

