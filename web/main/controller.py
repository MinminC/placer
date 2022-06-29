import json

from mods import *
from web import app
from web.main import service
from flask import render_template, request, jsonify, Response


@app.route('/')
def index():
    """
    메인 페이지로 이동
    :return: index.html을 반환
    """
    area_code = [{'areaNo': 1, 'sido': '서울'}, {'areaNo': 2, 'sido': '인천'}, {'areaNo': 21, 'sido': '경기'}]
    place_type = [{'typeCode': 11, 'typeContent': '숙박'}, {'typeCode': 12, 'typeContent': '여행지'}]
    return render_template('index.html', areaCode=area_code, placeType=place_type)


@app.route('/search', methods=['GET'])
def search_place():
    """
    여행지를 오픈데이터에서 검색
    :return: 응답 결과, 응답 코드
    """
    # 요청 값 확인
    try:
        keyword = request.args.get('keyword', '')
        page_no = request.args.get('pageNo', '')
        content_id = request.args.get('contentTypeId', '')
    except Exception as e:
        return jsonify(status=ERROR_CODE_BAD_REQUEST, msg=ERROR_CODE_BAD_REQUEST_MSG), ERROR_CODE_BAD_REQUEST

    # 공공데이터 서버에 요청
    status, msg, result = service.get_opendata(keyword, page_no, content_id)
    if status != ERROR_CODE_SUCCESS:
        return jsonify(status=status, msg=msg), status

    json_string = json.dumps(result, ensure_ascii=False)
    response = Response(json_string, content_type='application/json; charset=utf-8')

    return response, ERROR_CODE_SUCCESS
