# movies model에 저장
# 업데이트를 하려면 새로운 코드를 짜야할 것 같다.

from datetime import datetime, timedelta
import requests
import json
import urllib.request
from bs4 import BeautifulSoup

# youtube
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from oauth2client.tools import argparser

today = datetime.today()

daily_url = 'http://www.kobis.or.kr/kobisopenapi/webservice/rest/boxoffice/searchDailyBoxOfficeList.json'
detail_url = 'http://www.kobis.or.kr/kobisopenapi/webservice/rest/movie/searchMovieInfo.json'

### key값 따로 저장 필요 ###
key = '89463563279eb5bce6f2e9655a090259'

# director.json 불러오기
with open('fixtures/director.json', 'r', encoding='utf-8') as f:
    director_data = json.load(f)
# print(director_data)

watchgrade_dict = {1: '전체관람가', 2: '12세이상관람가', 3: '15세이상관람가', 4: '청소년관람불가', 5: '제한상영가', 6: '등급보류'}

movieNm_list = []
audiAcc_list = []
movieNmEn_list = []
directors_list = []
watchGradeNm_list = []
# for i in range(60):
for i in range(1):
    targetDt = (today + timedelta(days=-(i+1))).strftime('%Y%m%d')
    # print(targetDt)
    daily_movie_url = f'{daily_url}?key={key}&targetDt={targetDt}'
    print(daily_movie_url)
    res = requests.get(daily_movie_url).json()

    for k in range(10):
        movieCd = res.get('boxOfficeResult').get('dailyBoxOfficeList')[k].get('movieCd')
        movieNm = res.get('boxOfficeResult').get('dailyBoxOfficeList')[k].get('movieNm')
        audiAcc = res.get('boxOfficeResult').get('dailyBoxOfficeList')[k].get('audiAcc')
        if movieNm not in movieNm_list and '3D' not in movieNm:
            movieNm_list.append(movieNm)
            audiAcc_list.append(int(audiAcc))
            
            detail_movie_url = f'{detail_url}?key={key}&movieCd={movieCd}'
            detail_res = requests.get(detail_movie_url).json()
            movieNmEn = detail_res.get('movieInfoResult').get('movieInfo').get('movieNmEn')
            movieNmEn_list.append(movieNmEn)
            
            peopleNms = detail_res.get('movieInfoResult').get('movieInfo').get('directors')
            peopleNm_list = []
            for dd in range(len(director_data)):
                for p in range(len(peopleNms)):
                    peopleNm = peopleNms[p].get('peopleNm')
                    if peopleNm == director_data[dd].get('fields').get('name'):
                        peopleNm_list.append(director_data[dd].get('id'))
            directors_list.append(peopleNm_list)
            
            watchGradeNms = detail_res.get('movieInfoResult').get('movieInfo').get('audits')
            if len(watchGradeNms) == 0:
                watchGradeNm_list.append(6)
            else:
                watchGradeNm = watchGradeNms[0].get('watchGradeNm')
                for dict_id, val in watchgrade_dict.items():
                    if val == watchGradeNm:
                        watchGradeNm_list.append(dict_id)
                        break
                else:
                    watchGradeNm_list.append(6)
    # print(watchGradeNm_list)
# print(len(movieNm_list))
# print(audiAcc_list)
# print(movieNmEn_list)
# print(directors_list)
# print(len(watchGradeNm_list))

# 애플리케이션 클라이언트 id 및 secret
### id, secret값 따로 저장 필요 ###
client_id = "hG6O_G7PA_2DCtQbUri0" 
client_secret = "fsSh41QFYc"

# Youtube
DEVELOPER_KEY = "AIzaSyAVCkIahavkDKoC_PcO7yRS5_2oxzzjbyc"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey = DEVELOPER_KEY)

len_movie = len(movieNm_list)
poster_image_url = "https://movie.naver.com/movie/bi/mi/photoViewPopup.nhn?movieCode="
genre_dict = {1: '드라마', 2: '판타지', 3: '서부', 4: '공포', 5: '로맨스', 6: '모험', 7: '스릴러', 8: '느와르', 9: '컬트', 10: '다큐멘터리', 11: '코미디', 12: '가족', 13: '미스터리', 14: '전쟁', 15: '애니메이션', 16: '범죄', 17: '뮤지컬', 18: 'SF', 19: '액션', 20: '무협', 21: '에로', 22: '서스펜스', 23: '서사', 24: '블랙코미디', 25: '실험', 26: '영화카툰', 27: '영화음악', 28: '영화패러디포스터'}
data = [{}] * len_movie
cnt_id = 0
for i in range(len_movie):
    movie_data = {}
    fields = {}

    # youtube 예고편
    preview_search_response = youtube.search().list(
        q = movieNm_list[i] + "메인 예고편",
        part = "snippet",
        maxResults = 1
    ).execute()

    # print(preview_search_response.get('items'))
    if preview_search_response.get('items') != []:
        preview_videoId = preview_search_response.get('items')[0].get('id').get('videoId')
        video_url = f'https://www.youtube.com/embed/{preview_videoId}'
        # print(video_url)
        if video_url == "https://www.youtube.com/embed/None":
            video_url = ''
    else:
        video_url = ''

    # youtube ost
    ost_search_response = youtube.search().list(
        q = movieNm_list[i] + "메인 OST",
        part = "snippet",
        maxResults = 1
    ).execute()

    if ost_search_response.get('items') != []:
        ost_videoId = ost_search_response.get('items')[0].get('id').get('videoId')

        ost_url = f'https://www.youtube.com/embed/{ost_videoId}'
        # print(ost_url)
        if ost_url == "https://www.youtube.com/embed/None":
            ost_url = ''
    else:
        ost_url = ''
    
    #영화검색 url
    url = "https://openapi.naver.com/v1/search/movie.json"
    option = "&display=1"
    query = "?query="+urllib.parse.quote(movieNm_list[i]) # movieNm
    url_query = url + query + option
    
    #Open API 검색 요청 개체 설정
    request = urllib.request.Request(url_query)
    request.add_header("X-Naver-Client-Id",client_id)
    request.add_header("X-Naver-Client-Secret",client_secret)
    
    #검색 요청 및 처리
    response = urllib.request.urlopen(request)
    rescode = response.getcode()
    if(rescode == 200):
        response_body = response.read()
        str_info = response_body.decode('utf-8')
        dict_info = json.loads(str_info)

        if dict_info.get('items') != []:
            cnt_id += 1

            # score
            score = dict_info.get('items')[0].get('userRating') # string type
            score = float(score)
            # print(score)

            # link
            movie_link = dict_info.get('items')[0].get('link') # poster_url, summary, video_url, ost_url

            # poster_url
            temp_link = movie_link
            for t in range(len(temp_link)):
                if temp_link[t] == "=":
                    naver_movie_code = temp_link[t+1:]
                    break
            temp_poster_url = poster_image_url + naver_movie_code
            # print(temp_poster_url)

            poster_response = requests.get(temp_poster_url).text
            poster_soup = BeautifulSoup(poster_response, 'html.parser')
            posters = poster_soup.select('#page_content > a')
            poster_url = posters[0].find_all('img')[0].get('src')
            # print(poster_url)

            # soup
            response = requests.get(movie_link).text
            soup = BeautifulSoup(response, 'html.parser')

            # summary
            contents = soup.select('div.story_area > p.con_tx')

            summary = ''
            if len(contents) == 0:
                summary = "줄거리 없음"
            else:
                for c in contents:
                    temp = c.text
                    temp = temp.replace('\r', '')
                    temp = temp.replace('\xa0', '')
                    temp = temp.replace('   ', ' ')
                    temp = temp.replace('  ', ' ')
                    summary = temp
            # print(summary)
        
            # genres
            genre_list = soup.select('dl.info_spec > dd:nth-child(2) > p')
            temp_genres = genre_list[0].text.replace(',', '').replace('/', ' ')
            temp_genre_list = temp_genres.split()

            genres = []
            for dict_id, val in genre_dict.items():
                for temp_genre in temp_genre_list:
                    if val == temp_genre:
                        genres.append(dict_id)
            # print(genres)
    else:
        print("Error code:"+rescode)

    fields["title"] = movieNm_list[i]
    fields["title_en"] = movieNmEn_list[i]
    fields["summary"] = summary
    fields["score"] = score
    fields["audience"] = audiAcc_list[i]
    fields["poster_url"] = poster_url
    fields["video_url"] = video_url
    fields["ost_url"] = ost_url

    fields["movie_directors"] = directors_list[i]
    fields["movie_genres"] = genres
    fields["grade_id"] = watchGradeNm_list[i]


    movie_data["id"] = cnt_id
    movie_data["model"] = "movies.movie"
    movie_data["fields"] = fields

    data[i] = movie_data
    # print()
print(data)

with open('fixtures/movie.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False)