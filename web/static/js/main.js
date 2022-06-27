$(function(){
    // 여행지 검색
    $('#search-opendata').click(function(){
        var keyword = $(this).siblings('input[type=search]').val();
        if(keyword == ''){
            alert('검색어를 입력하세요');
        }
        else{
            ajaxSearchPlace(keyword, 1);
        }
    })

    // 테이블의 행을 클릭 시 selectPlace 영역에 결과 출력
    $('#placeList tbody').on('click', 'tr', function(){
        $('input[name=placeName]').val($(this).find('.title').text());
        $('input[name=placeLat]').val($(this).find('.mapx').val());
        $('input[name=placeLon]').val($(this).find('.mapy').val());
        $('#placeImg').attr('src', $(this).find('.firstimage').val());
        $('input[name=placeAddress]').val($(this).find('.address').text());
        $('select[name=area]>option[value='+$(this).find('.areacode').val()+']').attr('selected', true);
        $('select[name=typeCode]>option[value='+$(this).find('.contenttype').val()+']').attr('selected', true);
        $('#placeImg').show();
    })

    // 위도에 숫자와 점 이외의 값 입력 시 경고
    $('input[name=placeLat]').keyup(function(){
        if(!regExpNumber($(this).val())){
            alert('위도를 입력하세요.');
            $(this).val('');
            $(this).focus();
        }
    })

    // 경도에 숫자와 점 이외의 값 입력 시 경고
    $('input[name=placeLon]').keyup(function(){
        if(!regExpNumber($(this).val())){
            alert('경도를 입력하세요.');
            $(this).val('');
            $(this).focus();
        }
    })

    // 태그에서 벗어나면 태그 목록에 등록
    $('#tagNow').blur(function(){
        enrollTag();
    })

    // 태그를 입력하고 엔터 키를 입력하면 태그 등록
    $('#tagNow').keydown(function(event){
        if(event.keyCode == 13 || event.which == 13){
            enrollTag();
        }
    });

    // 태그에서 X 누르면 해당 태그 삭제
    $('#tags').on('click','i', function(){
        $(this).parent().remove();
    })
})

// 빈 값이 아닌 경우 태그를 입력
function enrollTag(){
    if(!$('#tagNow').val()){
        $('#tagNow').siblings('ul').append('<li><span>'+$('#tagNow').val()+'</span><i>X</i></li>');
        $('#tagNow').val('');
    }
}

// 위도, 경도가 정상적인 숫자로 이루어져있는지 확인하는 정규식
function regExpNumber(keyword){
    var regExp = /^[\d.]{1,}$/;
    return regExp.test(keyword);
}

// 여행지 검색하도록 AJAX 요청
function ajaxSearchPlace(keyword, pageNo){
    var contentTypeId = $('select[name=contentTypeId]').val();
    $.ajax({
        url:'search',
        data:{
            'keyword' : keyword,
            'pageNo' : pageNo,
            'contentTypeId' :  contentTypeId
            },
        success: function(result){
            render(result, keyword, pageNo, contentTypeId);
        }
    })
}

// 작성한 일지를 저장하도록 AJAX 요청
function checkIntegrity(){
    //태그를 하나로 묶기
    var tagArr = [];
    var $tags = $('#tags span');
    for(var i = 0; i<$tags.length; i++)
        tagArr.push($tags[i].innerText);
    var tagStr = tagArr.join(',');
    $('input[name=placeTags]').val(tagStr);

    //내용 삽입
    if(!$('textarea[name=placeDes]').val()){
        alert('내용 넣어요!!!!');
        return false;
    }
    //사진의 주소를 input 태그에 저장 TODO
    var imgPath = $('#placeImg').prop('src');
    if(imgPath == 'http://localhost:8112/firstclass/insertForm.pl'){//이미지가 없는 경우 현재 주소 반환됨
        alert('이미지를 등록해주세요!');
        return false;
    }else{
        $('input[name=imgPath]').val(imgPath);
    }

    ajaxInsertData(data);
    return true;
}

// 이미지가 변경된 경우 화면에 출력
function changeImg(picture){
    if(picture.files.length == 1){
        var reader = new FileReader();
        reader.readAsDataURL(picture.files[0]);
        reader.onload = function(e){
            $('#placeImg').attr('src', e.target.result);
        }
    }else
        $('#placeImg').attr('src', null);
    $('#placeImg').show();
}

// 여행지 정보를 출력 TODO
function render(result, keyword, pageNo, contentTypeId){
    var currentPage = pageNo;
    //페이징바 10개, 총 게시글은 5개씩 보여주기
        var listCount = Number($(result).find('totalCount').text());
        var currentPage = Number($(result).find('pageNo').text());
        var pageLimit = Number($(result).find('numOfRows').text());
        var boardLimit = 10;
        var maxPage = Math.ceil(listCount/boardLimit);
        var startPage = (currentPage -1)/pageLimit * pageLimit +1;
        var endPage = startPage + pageLimit -1;

        if(endPage > maxPage)
            endPage = maxPage;

        var value='';

        if(currentPage != 1)
            value += '<li class="page-item"><a class="page-link" onclick="ajaxSearchPlace('+"'"+keyword+"'"+', '+(pageNo-1)+');">&lt;</a></li>';
        for(var i=1;i<endPage+1;i++){
            value += '<li class="page-item';
            if(currentPage == i)
                value += ' active';
            value += '"><a class="page-link" onclick="ajaxSearchPlace('+"'"+keyword+"'"+', '+i+');">'+i+'</a></li>';
        }
        if(currentPage<maxPage)
            value += '<li class="page-item endPage"><a class="page-link" onclick="ajaxSearchPlace('+"'"+keyword+"', "+(pageNo+1)+');">&gt;</a></li>';
        $('.pagination').html(value);

        var itemArr = $(result).find('item');
        var value = '';
        itemArr.each(function(i, item){//인덱스, 해당 인덱스에서의 값

        value += '<tr><td class="title">'+$(item).find('title').text()//이름
            +'</td><td class="address">'+$(item).find('addr1').text()+' '+$(item).find('addr2').text()//주소
            +'<input type="hidden" class="areacode" value="'+$(item).find('areacode').text()//지역코드
            +'"><input type="hidden" class="sigungucode" value="'+$(item).find('sigungucode').text()//시군구코드
            +'"><input type="hidden" class="mapx" value="'+$(item).find('mapx').text()//x좌표
            +'"><input type="hidden" class="mapy" value="'+$(item).find('mapy').text()//u좌표
            +'"><input type="hidden" class="firstimage" value="'+$(item).find('firstimage').text()//대표 사진
            +'"><input type="hidden" class="contenttype" value="'+$(item).find('contenttypeid').text()//여행지타입:12==관광지
            +'"></td></tr>';
    });
    $('#placeList tbody').html(value);
}

// 리셋 버튼 클릭 시 초기화
function clearAll(){
    $('select[name=contentTypeId]>option').eq(0).attr('selected', true);
    $('#input-search').val('');
    $('#placeList>tbody').empty();
    $('.pagination').empty();

    $('input[name=placeName]').val('');
    $('input[name=placeLat]').val('');
    $('input[name=placeLon]').val('');
    $('#placeImg').attr('src', '');
    $('input[name=placeAddress]').val('');
    $('select[name=area]>option').eq(0).attr('selected', true);
    $('select[name=typeCode]>option').eq(0).attr('selected', true);
    $('#placeImg').hide();

    $('#tags>ul').empty();
    $('input[name=placeTags]').val('');
    $('textarea[name=placeDes]').val('');
}

// 일지를 저장 TODO
function ajaxInsertData(result){
    $.ajax({
        url: 'insert',
        type: 'post',
        data: result,
        success: function(){
        },
        error: function(){
        }
    })
}