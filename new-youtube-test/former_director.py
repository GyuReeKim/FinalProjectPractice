# director model에 저장
# 업데이트 필요

from datetime import datetime, timedelta
import requests
import json

today = datetime.today()

daily_url = 'http://www.kobis.or.kr/kobisopenapi/webservice/rest/boxoffice/searchDailyBoxOfficeList.json'
detail_url = 'http://www.kobis.or.kr/kobisopenapi/webservice/rest/movie/searchMovieInfo.json'

# key값 따로 저장 필요
key = '660f73acbf0225280f5db341b9f4e840'

directors_list = []
for i in range(60):
# for i in range(5):
    targetDt = (today + timedelta(days=-(i+1))).strftime('%Y%m%d')
    # print(targetDt)
    daily_movie_url = f'{daily_url}?key={key}&targetDt={targetDt}'

    res = requests.get(daily_movie_url).json()

    for k in range(10):
        movieCd = res.get('boxOfficeResult').get('dailyBoxOfficeList')[k].get('movieCd')
        movieNm = res.get('boxOfficeResult').get('dailyBoxOfficeList')[k].get('movieNm')
            
        detail_movie_url = f'{detail_url}?key={key}&movieCd={movieCd}'
        detail_res = requests.get(detail_movie_url).json()
        
        peopleNms = detail_res.get('movieInfoResult').get('movieInfo').get('directors')
        peopleNm_list = []
        for p in range(len(peopleNms)):
            peopleNm = peopleNms[p].get('peopleNm')
            peopleNm_list.append(peopleNm)
        if peopleNm_list not in directors_list:
            directors_list.append(peopleNm_list)
print(directors_list)


directors_dict_list = []
each_directors_list = []
cnt_id = 0
for dl in range(len(directors_list)):
    # print(directors_list[dl])
    for d in range(len(directors_list[dl])):
        if directors_list[dl][d] not in each_directors_list:
            each_directors_dict = {}
            cnt_id += 1
            each_directors_dict["id"] = cnt_id
            each_directors_dict["model"] = "movies.director"
            each_directors_dict["fields"] = {"name": directors_list[dl][d]}
            each_directors_list.append(directors_list[dl][d])
            directors_dict_list.append(each_directors_dict)
print(directors_dict_list)

with open('fixtures/director.json', 'w', encoding='utf-8') as f:
    json.dump(directors_dict_list, f, ensure_ascii=False)