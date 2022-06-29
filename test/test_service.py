from unittest import TestCase, mock

from mods import *
from web import app
from config import appcfgs
from web.main import service


class TestService(TestCase):
    def create_app(self):
        app.config.from_object(appcfgs.TestingConfig)
        self.app = app.test_client()
        self.app.config = app.config

    def setUp(self):
        self.create_app()

    @mock.patch('web.main.service.requests.get')
    def test_get_opendata_success(self, mocked_requests_get):
        """
        OpenData 엔진에서 키워드로 검색할 때 성공한 경우
        :return:
        """
        # Given
        keyword = 'search_word'
        page_no = '1'
        content_id = '12'
        test_url = 'http://api.visitkorea.or.kr/openapi/service/rest/KorService/searchKeyword'\
                   + '?serviceKey='+self.app.config['SERVICE_KEY']\
                   + '&MobileApp=AppTest&MobileOS=ETC&pageNo=1&numOfRows=5&listYN=Y&arrange=A'\
                   + '&contentTypeId=12&keyword=search_word'
        mocked_requests_get.return_value.text = '<?xml version="1.0" encoding="UTF-8" standalone="yes"?><response><header>' \
                                 + '<resultCode>0000</resultCode><resultMsg>OK</resultMsg></header><body>' \
                                 + '<items><item><addr1>경상남도 고성군 고성읍 이당리</addr1><areacode>36</areacode>' \
                                 + '<booktour>0</booktour><cat1>A01</cat1><cat2>A0101</cat2><cat3>A01010600</cat3>' \
                                 + '<contentid>2613159</contentid><contenttypeid>12</contenttypeid>'\
                                 + '<createdtime>20190726225107</createdtime><mapx>128.2693627701</mapx>'\
                                 + '<mapy>34.9727568130</mapy><mlevel>6</mlevel>'\
                                 + '<modifiedtime>20220425155721</modifiedtime>' \
                                 + '<readcount>0</readcount><sigungucode>3</sigungucode><title>갈모봉 산림욕장</title>'\
                                 + '</item></items><numOfRows>1</numOfRows><pageNo>1</pageNo>'\
                                 + '<totalCount>40</totalCount></body></response>'
        expected = ERROR_CODE_SUCCESS, ERROR_CODE_SUCCESS_MSG, mocked_requests_get.return_value.text

        # When
        actual = service.get_opendata(keyword, page_no, content_id)

        # Then
        self.assertEqual(expected, actual)
        mocked_requests_get.assert_called_with(test_url)

    @mock.patch('web.main.service.requests.get')
    def test_get_opendata_engine_error(self, mocked_requests_get):
        """
        OpenData 엔진에서 키워드로 검색할 때 엔진에서 실패한 경우
        :return:
        """
        # Given
        keyword = 'search_word'
        page_no = '1'
        content_id = '12'
        test_url = 'http://api.visitkorea.or.kr/openapi/service/rest/KorService/searchKeyword' \
                   + '?serviceKey=' + self.app.config['SERVICE_KEY'] \
                   + '&MobileApp=AppTest&MobileOS=ETC&pageNo=1&numOfRows=5&listYN=Y&arrange=A' \
                   + '&contentTypeId=12&keyword=search_word'
        mocked_requests_get.side_effect = Exception('openData Server Error')
        expected = ERROR_OPENDATA_ENGINE_ERROR, ERROR_OPENDATA_ENGINE_ERROR_MSG, ''

        # When
        actual = service.get_opendata(keyword, page_no, content_id)

        # Then
        self.assertEqual(expected, actual)
        mocked_requests_get.assert_called_with(test_url)

    @mock.patch('web.main.service.requests.get')
    def test_get_opendata_parameter_error(self, mocked_requests_get):
        """
        OpenData 엔진에서 키워드로 검색할 때 파라미터 오류로 비정상적인 값이 반환된 경우
        :return:
        """
        # Given
        keyword = 'search_word'
        page_no = '1'
        content_id = '12'
        test_url = 'http://api.visitkorea.or.kr/openapi/service/rest/KorService/searchKeyword'\
                   + '?serviceKey='+self.app.config['SERVICE_KEY']\
                   + '&MobileApp=AppTest&MobileOS=ETC&pageNo=1&numOfRows=5&listYN=Y&arrange=A'\
                   + '&contentTypeId=12&keyword=search_word'
        mocked_requests_get.return_value.text = '<?xml version="1.0" encoding="UTF-8" standalone="yes"?><response>'\
                                                + '<header><responseTime>2022-06-29T10:23:24.512+09:00</responseTime>'\
                                                + '<resultCode>30</resultCode>'\
                                                + '<resultMsg>SERVICE KEY IS NOT REGISTERED ERROR.</resultMsg>'\
                                                + '</header></response>'
        expected = ERROR_OPENDATA_ENGINE_ERROR, 'SERVICE KEY IS NOT REGISTERED ERROR.', ''

        # When
        actual = service.get_opendata(keyword, page_no, content_id)

        # Then
        self.assertEqual(expected, actual)
        mocked_requests_get.assert_called_with(test_url)
