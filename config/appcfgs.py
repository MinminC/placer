import os


class Config(object):
    # 프로젝트 경로를 BASE DIR로 사용
    BASE_DIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

    DATA_DIR = os.path.join(BASE_DIR, 'data')
    if not os.path.exists(DATA_DIR):
        os.mkdir(DATA_DIR)

    # 공공데이터 주소
    SERVICE_KEY = 'm%2BXQ6JZ8nOxT0%2B2ewkBZu5xzdEDAqebDxTFvI5yk%2BUl%2BNBdExNfOCji4u6PJkpZcGcujkx%2FLd26XQiHfFtraLw%3D%3D'
    SERVER_URL = 'http://api.visitkorea.or.kr/openapi/service/rest/KorService/searchKeyword'


class TestingConfig(Config):
    TESTING = True
