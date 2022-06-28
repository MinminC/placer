import json
import requests
from urllib.parse import quote

from mods import *
from web import app
# from config import appcfgs


def get_opendata(keyword, page_no, content_id):
    """
    공공데이터 서버에 정보 검색 요청
    :param keyword: 검색할 키워드
    :param page_no: 검색할 페이지
    :param content_id: 검색할 관광지 분류 코드
    :return: 응답 코드, 응답 메세지, 응답 결과
    """
    # 요청 데이터 TODO 전부 하나로 합치는 것 os같은 모듈 사용?
    url = app.config['SERVER_URL']
    url += "?serviceKey="+app.config['SERVICE_KEY']
    url += "&MobileApp=AppTest"
    url += "&MobileOS=ETC"
    url += "&pageNo="+page_no
    url += "&numOfRows=5"
    url += "&listYN=Y"
    url += "&arrange=A"
    url += "&contentTypeId="+content_id
    url += "&keyword="+quote(keyword)

    response = requests.get(url)

    result = response.text

    return ERROR_CODE_SUCCESS, ERROR_CODE_SUCCESS_MSG, result
