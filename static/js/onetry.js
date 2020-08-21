function call_ajax() {
    // 입력텍스트상자에서 키보드로 입력이 들어왔을 때 호출
    // 모든 키에 대해서 처리하는게 아니라 enter key일 경우에만 처리
    if (event.keyCode == 13) {
        // 만약 입력된 enter key이면 이 부분을 수행하게 된다.
        // 서버쪽 프로그램을 호출해서 결과를 받아온다.
        // jQuery를 이용해서 AJAX처리를 해보자.
        // ajax의 인자로 javascript 객체를 넣어준다.
        // javascript 객체는 => { key : value, key : value, ......}
        // data : 서버프로그램에게 넘겨줄 데이터들...
        $.ajax({
            async : true,      // 비동기 방식의 호출(default)    false는 동기 방식으로 호출
            url : "http://apis.data.go.kr/1470000/FoodNtrIrdntInfoService/getFoodNtrItdntList?",
            data : {
                serviceKey : 'YtKyAF9FxF7M4DG2iK3wwuYPN9QOZZ5Gq0UteffbkUIU2wPq8az1Ue6plV6kZQsNB1E4rNv4YcaL60LiXla9vQ%3D%3D',
                desc_kor : '바나나칩',
                pageNo : '1',
                numOfRows : '3',
                bgn_year : '2017',
                animal_plant : '(유)돌코리아'
            },
            type : "GET",
            timeout : 3000,      //밀리세컨드기준임. 3초
            dataType : "xml",       // 결과 JSON은 JavaScript객체로 변환이 된다.
            success : function (result) {    // 서버가 보내준 데이터가 result로 받는다.
                alert("서버호출 성공!!")
                console.log(result)
            },
            error : function (error) {
                alert("서버호출 실패!!")
            }
        })
    }


}