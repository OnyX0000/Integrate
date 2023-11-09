from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from elasticsearch import Elasticsearch
from elastic_app_search import Client
from sentence_transformers import SentenceTransformer, util
import re
import json
import datetime
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View
from django.views import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.urls import reverse

# Elasticsearch 클라이언트 설정
es_cloud_id = "lowlaw:YXAtbm9ydGhlYXN0LTIuYXdzLmVsYXN0aWMtY2xvdWQuY29tOjQ0MyQ2YzNmMjA4MmNiMzk0M2YxYTBiZWI0ZDY2M2JmM2VlZCRjZTA2NGZhNjFiMmI0N2Y0ODgzMjY0Y2FlMzVlZDgxZQ=="
es_username = "elastic"
es_pw = "LWkW2eILoZYZylsDDThLaCKY"
es = Elasticsearch(cloud_id=es_cloud_id, basic_auth=(es_username, es_pw))

# Appsearch 클라이언트 설정
client = Client(
    base_endpoint="lowlaw.ent.ap-northeast-2.aws.elastic-cloud.com/api/as/v1",
    api_key="private-egnzqo7tt7fd6fngz13mmox9",
    use_https=True
)

engine_name_1 = 'law-content'
engine_name_2 = 'prec-search'

# def home(request):
#     return render(request, 'main.html')

def searchengine(request):
    if request.method == 'GET':
        return render(request, 'searchEngine.html')
    else:
        return HttpResponse(status=200)

@csrf_exempt
def search(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        user_input = data.get('user_input', "")
        
        print(user_input)
        
        if not user_input:
            return JsonResponse({"error": "입력이 없습니다"}, status=400)
        
        # 검색어로 법령과 판례를 각각 검색
        law = law_search(user_input)
        prec = prec_search(user_input)

        # 결과를 JSON 형태로 가공
        result_data = {
            "law": law,
            "prec": prec,
            "status": 200  # 상태 코드, 성공적으로 처리됐을 때는 200을 반환
        }

        print(result_data)

        # JsonResponse로 결과 전송
        return JsonResponse(result_data)

@csrf_exempt
def law_search(law): # App Search에서 참조법령 찾기
    # 검색 옵션 설정 (score 점수 내림차순 정렬, 상위 1개 결과)
    search_options = {
        "sort": [{"_score": "desc"}],  # score 점수 내림차순 정렬
        "page": {"size": 3, "current": 1}  # 상위 3개 결과 (페이지 크기와 현재 페이지 번호를 지정)
    }

    law_results = {}
    
    engine_name = 'law-content' # 법령검색 App Search
    
    # search
    search_query = str(law)
    search_result = client.search(engine_name, search_query, search_options)
    
    for idx, result in enumerate(search_result['results']):
        law_name = result.get('law', {}).get('raw', '')  # 검색 결과에서 법령 이름 가져오기
        if law_name:
            combined_fields = ' '.join([result[field]['raw'] for field in ['jo', 'hang', 'ho', 'mok'] if field in result])
            
            combined_content = ""
            content_fields = ['jo_content', 'hang_content', 'ho_content', 'mok_content']
            for content_field in content_fields:
                if content_field in result:
                    content = result[content_field]['raw']
                    pattern = r'제(\d+)조\(([^)]+)\)'
                    replaced_content = re.sub(pattern, lambda match: f'제{match.group(1)}조({(match.group(2))})', content)
                    combined_content += replaced_content + " "
                
            # 결과를 딕셔너리에 추가
            law_results[f"best_answer{idx + 1}_law"] = {
                "law_name": law_name,
                "law_specific": combined_fields,
                "law_content": combined_content
            }
    
    # 'law' 변수에 저장
    #law = {"law": law_results}
            
    print(law_results)
    
    return law_results

@csrf_exempt
def prec_search(prec): # App Search 에서 참조판례 찾기
    # 검색 옵션 설정 (score 점수 내림차순 정렬, 상위 3개 결과)
    search_options = {
        "sort": [{"_score": "desc"}],  # score 점수 내림차순 정렬
        "page": {"size": 3, "current": 1}  # 상위 3개 결과
    }

    prec_results = {}
    
    engine_name = 'prec-search'
    
    search_query = prec
    search_result = client.search(engine_name, search_query, search_options)
    
    for idx, result in enumerate(search_result['results']):
        result_dict = {}
        score = result['_meta']['score']

        #fields_to_print = ['사건명', '사건번호', '선고일자', '법원명', '사건종류명', '판시사항', '판결요지', '참조조문', '참조판례', '판례내용']
        fields_to_print = {
        '사건명': 'case_name',
        '사건번호': 'case_number',
        '선고일자': 'sentence_date',
        '법원명': 'court_name',
        '사건종류명': 'case_type',
        '판시사항': 'holding',
        '판결요지': 'headnote',
        '참조조문': 'reference_law',
        '참조판례': 'reference_prec',
        '판례내용': 'prec_content'
        }

        for field_kor, field_eng in fields_to_print.items():
            if field_kor in result:
                field_value = result[field_kor]['raw']
                if not field_value:
                    continue
                if field_kor == '선고일자':
                    try:
                        date_value = datetime.datetime.strptime(str(int(field_value)), '%Y%m%d').strftime('%Y.%m.%d')
                        result_dict[field_eng] = f"{date_value}"
                    except ValueError:
                        result_dict[field_eng] = field_value
                elif field_kor in ['법원명', '사건종류명']:
                    result_dict[field_eng] = field_value
                elif field_kor == '판시사항':
                    if field_value:
                        field_value = field_value.replace('[', '\n[')
                        result_dict[field_eng] = field_value
                elif field_kor == '판결요지':
                    if field_value:
                        field_value = field_value.replace('[', '\n[')
                        result_dict[field_eng] = field_value
                elif field_kor == '참조조문':
                    if field_value:
                        field_value = field_value.replace('/', '\n\n')
                        result_dict[field_eng] = field_value
                elif field_kor == '참조판례':
                    if field_value:
                        field_value = field_value.replace('/', '\n\n')
                        result_dict[field_eng] = field_value
                elif field_kor == '판례내용':
                    if field_value:
                        field_value = field_value.replace('【', '\n\n【')
                        result_dict[field_eng] = field_value
                else:
                    result_dict[field_eng] = field_value
                    
        # 결과를 JSON 문자열로 변환하여 딕셔너리에 추가
        prec_results[f"best_answer{idx + 1}_prec"] = result_dict

    #prec = {"prec": prec_results}

    print(prec_results)
    
    return prec_results