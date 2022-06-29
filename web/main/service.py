import os
import uuid
import requests
from datetime import datetime
from urllib.parse import quote
import xml.etree.ElementTree as ET

from mods import *
from web import app


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

    try:
        response = requests.get(url)
        root = ET.fromstring(response.text)
        status_code = root[0][0].text
    except Exception as e:
        return ERROR_OPENDATA_ENGINE_ERROR, ERROR_OPENDATA_ENGINE_ERROR_MSG, ''
    if status_code != '0000':
        status_msg = root[0][2].text
        return ERROR_OPENDATA_ENGINE_ERROR, status_msg, ''

    return ERROR_CODE_SUCCESS, ERROR_CODE_SUCCESS_MSG, response.text


def save_image(image_storage, file_ext):
    random_num = str(uuid.uuid4())[:8]
    file_id = '{}_{}'.format(datetime.now().strftime('%Y%m%d_%H%M%S'), random_num)
    filename = '{}{}'.format(file_id, file_ext)
    filepath = os.path.join(app.config['DATA_DIR'], filename)

    try:
        # 요청 받은 이미지 저장
        image_storage.save(filepath)
    except Exception as e:
        return ERROR_IMGPROC_ERROR, ERROR_IMGPROC_ERROR_MSG, {}

    return ERROR_CODE_SUCCESS, ERROR_CODE_SUCCESS_MSG
