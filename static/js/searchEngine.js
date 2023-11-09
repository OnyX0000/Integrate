const textarea = document.getElementById("message_input");
const sendbtn = document.getElementById('message_btn');
sendbtn.addEventListener("click",()=>{
    submit(textarea.value);
})
textarea.addEventListener("keydown",(e)=>{
    if(e.keyCode == '13'){
        if(!e.shiftKey){
            submit(textarea.value);
        }
    }
})
function submit(message){
    fetch('/searchEngine/',{
        methot:'POST',
        header:{
            'Content-Type' : 'application/json'
        },
        body:JSON.stringify({
            user_input:message
        })
    })
    .then(response=>{
        return response.json();
    }).catch((error)=>console.log(error))
    .then((data=>{
        result_print(data)
    }))
//     data = {
//         "law": {
//                 "best_answer1_law": {
//                         "law_name": "상가건물 임대차보호법",
//                         "law_specific": "제10조 제1항 제7호 가목",
//                         "law_content": "제10조(계약갱신 요구 등) ① 임대인은 임차인이 임대차기간이 만료되기 6개월 전부터 1개월 전까지 사이에 계약갱신을 요구할 경우 정당한 사유 없이 거절하지 못한다. 다만, 다음 각 호의 어느 하나의 경우에는 그러하지 아니하다. <개정 2013.8.13> 7. 임대인이 다음 각 목의 어느 하나에 해당하는 사유로 목적 건물의 전부 또는 대부분을 철거하거나 재건축하기 위하여 목적 건물의 점유를 회복할 필요가 있는 경우 가. 임대차계약 체결 당시 공사시기 및 소요기간 등을 포함한 철거 또는 재건축 계획을 임차인에게 구체적으로 고지하고 그 계획에 따르는 경우"
//                 },
//                 "best_answer2_law": {
//                         "law_name": "상가건물 임대차보호법",
//                         "law_specific": "제10조 제1항 제7호 다목",
//                         "law_content": "제10조(계약갱신 요구 등) ① 임대인은 임차인이 임대차기간이 만료되기 6개월 전부터 1개월 전까지 사이에 계약갱신을 요구할 경우 정당한 사유 없이 거절하지 못한다. 다만, 다음 각 호의 어느 하나의 경우에는 그러하지 아니하다. <개정 2013.8.13> 7. 임대인이 다음 각 목의 어느 하나에 해당하는 사유로 목적 건물의 전부 또는 대부분을 철거하거나 재건축하기 위하여 목적 건물의 점유를 회복할 필요가 있는 경우 다. 다른 법령에 따라 철거 또는 재건축이 이루어지는 경우"
//                 },
//                 "best_answer3_law": {
//                         "law_name": "상가건물 임대차보호법",
//                         "law_specific": "제10조 제1항 제7호 나목",
//                         "law_content": "제10조(계약갱신 요구 등) ① 임대인은 임차인이 임대차기간이 만료되기 6개월 전부터 1개월 전까지 사이에 계약갱신을 요구할 경우 정당한 사유 없이 거절하지 못한다. 다만, 다음 각 호의 어느 하나의 경우에는 그러하지 아니하다. <개정 2013.8.13> 7. 임대인이 다음 각 목의 어느 하나에 해당하는 사유로 목적 건물의 전부 또는 대부분을 철거하거나 재건축하기 위하여 목적 건물의 점유를 회복할 필요가 있는 경우 나. 건물이 노후ㆍ훼손 또는 일부 멸실되는 등 안전사고의 우려가 있는 경우"
//                 }
//         },
//         "prec": {
//                 "best_answer1_prec": {
//                         "case_name": "건물명도(인도)", 
//                         "case_number": "2019가단10882", 
//                         "sentence_date": "2020.02.05", 
//                         "court_name": "대구지방법원 의성지원", 
//                         "case_type": "민사", 
//                         "holding": null, 
//                         "headnote": null, 
//                         "reference_law": null, 
//                         "reference_prec": null, 
//                         "prec_content": "【원 고】 원고(소송대리인 변호사 손명제)"
//                 },
//                 "best_answer2_prec": {
//                         "case_name": "건물명도", 
//                         "case_number": "2017나68141", 
//                         "sentence_date": "2018.05.30", 
//                         "court_name": "수원지방법원", 
//                         "case_type": "민사", 
//                         "holding": null,
//                         "headnote": null, 
//                         "reference_law": null, 
//                         "reference_prec": null, 
//                         "prec_content": "【원고, 피항소인】 원고 (소송대리인 변호사 정희채)"
//                 },
//                 "best_answer3_prec": {
//                         "case_name": "건물명도등", 
//                         "case_number": "2012다28486", 
//                         "sentence_date": "2014.07.24", 
//                         "court_name": "대법원", 
//                         "case_type": "민사", 
//                         "holding": "[1] 상가건물 임대차보호법의 적용을 받는 상가건물의 임대차에 민법 제640조에서 정한 계약해지 규정이 적용되는지 여부(적극) 및 민법 제640조와 동일한 내용을 정한 약정이 상가건물 임대차보호법 제15조에 의하여 효력이 없다고 할 수 있는지 여부(소극)",
//                         "headnote": "[1] 상가건물 임대차보호법에서 정한 임대인의 갱신요구거절권은 계약해지권과 행사시기, 효과 등이 서로 다를 뿐만 아니라, 상가건물 임대차보호법 제10조 제1항이 민법 제640조에서 정한 계약해지에 관하여 별도로 규정하고 있지 아니하므로, 상가건물 임대차보호법 제10조 제1항 제1호가 민법 제640조에 대한 특례에 해당한다고 할 수 없다. 그러므로 상가건물 임대차보호법의 적용을 받는 상가건물의 임대차에도 민법 제640조가 적용되고, 상가건물의 임대인이라도 임차인의 차임연체액이 2기의 차임액에 이르는 때에는 임대차계약을 해지할 수 있다. 그리고 같은 이유에서 민법 제640조와 동일한 내용을 정한 약정이 상가건물 임대차보호법의 규정에 위반되고 임차인에게 불리한 것으로서 위 법 제15조에 의하여 효력이 없다고 할 수 없다.[2] 갱신 전후 상가건물 임대차계약의 내용과 성질, 임대인과 임차인 사이의 형평, 상가건물 임대차보호법 제10조와 민법 제640조의 입법 취지 등을 종합하여 보면, 상가건물의 임차인이 갱신 전부터 차임을 연체하기 시작하여 갱신 후에 차임연체액이 2기의 차임액에 이른 경우에도 임대차계약의 해지사유인 ‘임차인의 차임연체액이 2기의 차임액에 달하는 때’에 해당하므로, 이러한 경우 특별한 사정이 없는 한 임대인은 2기 이상의 차임연체를 이유로 갱신된 임대차계약을 해지할 수 있다.",
//                         "reference_law": "[1] 상가건물 임대차보호법 제10조 제1항, 제15조, 민법 제640조[2] 상가건물 임대차보호법 제10조 제1항, 제3항, 민법 제640조",
//                         "reference_prec": null,
//                         "prec_content": "【원고, 피상고인】"
//                 }
//         },
//         "status": 200
// }
        result_print(data);

}

function result_print(data){
    var container = document.getElementById('result-container');

    var related_law_container = document.createElement('div');
    related_law_container.classList.add('related_law_container');

    var related_prec_container = document.createElement('div');
    related_prec_container.classList.add('related_prec_container');

    var lawTitle = document.createElement('h3');
    lawTitle.id = 'law';
    lawTitle.classList.add('law');
    lawTitle.textContent = '법령📖';
    
    var grayLine1 = document.createElement('div');
    grayLine1.classList.add('gray-line');
    
    var precTitle = document.createElement('h3');
    precTitle.id = 'prec';
    precTitle.classList.add('law');
    precTitle.textContent = '판례⚖️';
    
    var grayLine2 = document.createElement('div');
    grayLine2.classList.add('gray-line');
    
    related_law_container.appendChild(lawTitle);
    related_law_container.appendChild(grayLine1);
    
    related_prec_container.appendChild(precTitle);
    related_prec_container.appendChild(grayLine2);

    for(var key in data.law){
        var result_law_container = document.createElement('div');
        result_law_container.classList.add('result_law_container');

        var law_data = data.law[key];

        var law_name = document.createElement('p');
        law_name.classList.add('name')
        law_name.textContent = law_data.law_name

        var law_specific = document.createElement('p');
        law_specific.classList.add('jo');
        law_specific.textContent = law_data.law_specific;

        var law_content = document.createElement('p');
        law_content.classList.add('content');
        law_content.textContent=law_data.law_content;
        
        result_law_container.append(law_name);
        result_law_container.append(law_specific);
        result_law_container.append(law_content);

        related_law_container.append(result_law_container);
    }

    for(var key in data.prec){
        var prec_data = data.prec[key];
        var result_prec_container = document.createElement('div');
        result_prec_container.classList.add('result_prec_container')

        var result_prec_container_small_1 = document.createElement('div');
        result_prec_container_small_1.classList.add('result_prec_container_small_1')

        var case_name = document.createElement('p');
        case_name.classList.add('case_name');
        case_name.textContent = prec_data.case_name;

        var case_number = document.createElement('p');
        case_number.classList.add('case_number');
        case_number.textContent = prec_data.case_number;

        result_prec_container_small_1.append(case_name);
        result_prec_container_small_1.append(case_number);

        var result_prec_container_small_2 = document.createElement('div');
        result_prec_container_small_2.classList.add('result_prec_container_small_2')

        var case_type = document.createElement('p');
        case_type.classList.add('case_type');
        case_type.textContent = prec_data.case_type;

        var sentence_date = document.createElement('p');
        sentence_date.classList.add('sentence_date');
        sentence_date.textContent = prec_data.sentenct_date;

        var court_name = document.createElement('p');
        court_name.classList.add('court_name');
        court_name.textContent = prec_data.court_name;

        var prec_content = document.createElement('p');
        prec_content.classList.add('prec_content');
        prec_content.textContent = prec_data.prec_content;

        result_prec_container_small_2.append(case_type);
        result_prec_container_small_2.append(sentence_date);
        result_prec_container_small_2.append(court_name);

        result_prec_container.append(result_prec_container_small_1);
        result_prec_container.append(result_prec_container_small_2);
        result_prec_container.append(prec_content);

        related_prec_container.append(result_prec_container);
    }
    container.append(related_law_container);
    container.append(related_prec_container);

}