from datetime import datetime, timedelta
import requests
import json

with open('fixtures/director.json', 'r', encoding='utf-8') as f:
    director_data = json.load(f)
print(director_data)
len_director_data = len(director_data)

today = datetime.today()

daily_url = 'http://www.kobis.or.kr/kobisopenapi/webservice/rest/boxoffice/searchDailyBoxOfficeList.json'
detail_url = 'http://www.kobis.or.kr/kobisopenapi/webservice/rest/movie/searchMovieInfo.json'

# key값 따로 저장 필요
key = '660f73acbf0225280f5db341b9f4e840'
targetDt = (today + timedelta(days=-1)).strftime('%Y%m%d')
print(targetDt)
daily_movie_url = f'{daily_url}?key={key}&targetDt={targetDt}'
res = requests.get(daily_movie_url).json()
# print(res)

cnt_id = len_director_data

for k in range(10):

    movieCd = res.get('boxOfficeResult').get('dailyBoxOfficeList')[k].get('movieCd')

    detail_movie_url = f'{detail_url}?key={key}&movieCd={movieCd}'
    detail_res = requests.get(detail_movie_url).json()

    peopleNms = detail_res.get('movieInfoResult').get('movieInfo').get('directors')
    for p in range(len(peopleNms)):
        temp_dict = {}
        peopleNm = peopleNms[p].get('peopleNm')
        temp = 0
        for d in range(len(director_data)):
            if director_data[d].get('fields').get('name') == peopleNm:
                temp = 1
        if temp == 0:
            cnt_id += 1
            temp_dict['id'] = cnt_id
            temp_dict['model'] = 'movies.director'
            temp_dict['fields'] = {'name': peopleNm}
            director_data.append(temp_dict)
print(director_data)

# 추가된 director 저장
with open('fixtures/director.json', 'w', encoding='utf-8') as f:
    json.dump(director_data, f, ensure_ascii=False)