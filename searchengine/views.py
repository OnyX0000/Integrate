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

def search(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            search_query = data.get('search_query', '')  # 검색어를 JSON 데이터에서 추출
            if not search_query:
                return JsonResponse({"error": "입력이 없습니다"}, status=400)

            # 검색 옵션 설정 (score 점수 내림차순 정렬, 상위 3개 결과)
            search_options = {
                "sort": [{"_score": "desc"}],
                "page": {"size": 3, "current": 1}
            }

            # 법 검색 로직: Elasticsearch 및 Appsearch 코드를 이 부분에 추가
            search_results_engine_1 = {}  # 법 검색 결과를 저장할 변수

            # 판례 검색 로직: Elasticsearch 및 Appsearch 코드를 이 부분에 추가
            search_results_engine_2 = {}  # 판례 검색 결과를 저장할 변수

            # 법과 판례의 best_answer 정보 초기화
            best_answer1_law = None
            best_answer2_law = None
            best_answer3_law = None
            best_answer1_case = {}
            best_answer2_case = {}
            best_answer3_case = {}

            # 법 검색 결과를 best_answer_law에 추가
            for i, result in enumerate(search_results_engine_1['results']):
                if i == 0:
                    best_answer1_law = {
                        "law_name": result.get('law', {}).get('raw', ''),
                        "law_specific": result.get('law_specific', {}).get('raw', ''),
                        "law_content": result.get('law_content', {}).get('raw', '')
                    }
                    print(best_answer1_law)
                elif i == 1:
                    best_answer2_law = {
                        "law_name": result.get('law', {}).get('raw', ''),
                        "law_specific": result.get('law_specific', {}).get('raw', ''),
                        "law_content": result.get('law_content', {}).get('raw', '')
                    }
                elif i == 2:
                    best_answer3_law = {
                        "law_name": result.get('law', {}).get('raw', ''),
                        "law_specific": result.get('law_specific', {}).get('raw', ''),
                        "law_content": result.get('law_content', {}).get('raw', '')
                    }
                    
            fields_to_print = ['사건명', '사건번호', '선고일자', '법원명', '사건종류명', '판시사항', '판결요지', '참조조문', '참조판례', '판례내용']

            for i, result in enumerate(search_results_engine_2['results']):
                result_dict = None

                if i == 0:
                    result_dict = best_answer1_case
                elif i == 1:
                    result_dict = best_answer2_case
                elif i == 2:
                    result_dict = best_answer3_case

                for field in fields_to_print:
                    if field in result:
                        field_value = result[field]['raw']
                        if not field_value:
                            continue

                        if field == '선고일자':
                            try:
                                date_value = datetime.datetime.strptime(str(int(field_value)), '%Y%m%d').strftime('%Y.%m.%d')
                                result_dict[field] = f"{date_value}"
                            except ValueError:
                                result_dict[field] = field_value
                        elif field in ['법원명', '사건종류명']:
                            result_dict[field] = field_value
                        elif field == '판시사항' or field == '판결요지':
                            if field_value:
                                field_value = field_value.replace('[', '\n[')
                            result_dict[field] = field_value
                        elif field in ['참조조문', '참조판례']:
                            if field_value:
                                field_value = field_value.replace('/', '\n\n')
                            result_dict[field] = field_value
                        elif field == '판례내용':
                            if field_value:
                                field_value = field_value.replace('【', '\n\n【')
                            result_dict[field] = field_value

            # Django 템플릿을 렌더링하며 검색 결과와 best_answer 정보를 전달
            return render(request, 'search_results.html', {
                'search_results_engine_1': search_results_engine_1,
                'search_results_engine_2': search_results_engine_2,
                'best_answer1_law': best_answer1_law,
                'best_answer2_law': best_answer2_law,
                'best_answer3_law': best_answer3_law,
                'best_answer1_case': best_answer1_case,
                'best_answer2_case': best_answer2_case,
                'best_answer3_case': best_answer3_case,
            })

        except json.JSONDecodeError:
            return JsonResponse({'error': '잘못된 JSON 데이터입니다.'}, status=400)
    else:
        # GET 요청 또는 다른 요청 메서드를 처리하기 위한 추가 로직
        return render(request, 'searchEngine.html')
