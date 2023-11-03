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

def cached_model():
    model = SentenceTransformer('jhgan/ko-sroberta-multitask')
    return model

model = cached_model()

def home(request):
    return render(request, 'main.html')

def chatbot(request):
    if request.method == 'GET':
        return render(request, 'chatbot.html')

@csrf_exempt
def messages(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        user_input = data.get('user_input', "")
        
        if not user_input:
            return JsonResponse({"error": "입력이 없습니다"}, status=400)
        
        embeddings = model.encode([user_input])[0] if user_input else None

        if len(embeddings) > 0:
            # Elasticsearch에서 embedding 필드 값 검색
            query = {
                "query": {
                    "match_all": {}
                },
                "_source": ["question", "answer", "law", "prec", "embedding"]
            }

            response = es.search(index="legal_qa_final", body=query, size=3000)

            # Initialize chat history
            if "messages" not in request.session:
                request.session["messages"] = []

            # 사용자의 user_input을 chat history에 append
            request.session["messages"].append({"role": "user", "content": user_input})
                
            # 가장 높은 코사인 유사도 값 초기화
            max_cosine_similarity = -1
            best_answer = ""
            related_law = None
            related_prec = None

            # 각 문서와의 코사인 유사도 비교
            for hit in response["hits"]["hits"]:
                doc_embedding = hit["_source"]["embedding"]
                # Elasticsearch에서 가져온 'embedding' 값을 문자열에서 리스트로 변환
                doc_embedding = [float(value) for value in doc_embedding.strip("[]").split(", ")]
                cosine_similarity = util.pytorch_cos_sim(embeddings, [doc_embedding]).item()

                if cosine_similarity > max_cosine_similarity:
                    max_cosine_similarity = cosine_similarity
                    best_answer = hit["_source"]["answer"]
                    related_law = hit["_source"].get("law", None)  # 필드에 데이터가 존재하면 law 값을 가져오고 존재하지 않으면 None 반환
                    related_prec = hit["_source"].get("prec", None)  # 필드에 데이터가 존재하면 prec 값을 가져오고 존재하지 않으면 None 반환

            if max_cosine_similarity > 0.7:  # max_cosine_similarity 값이 0.7 이상이면 해당 답변 출력
                # 최적의 답변을 반환하는 로직
                best_answer = re.sub(r'\((.*?)\)', lambda x: x.group(0).replace('.', ' '), best_answer)
                best_answer = best_answer.replace('.', '.  \n\n')

                #if related_law:
                    #related_law_list = related_law.split(",")
                    #for law in related_law_list:
                        #best_answer += f"\n📖 {law}"
                #else:
                    #best_answer = None

                #if related_prec:
                    #related_prec_list = related_prec.split(",")
                    #for prec in related_prec_list:
                        #best_answer += f"\n⚖️ {prec}"
                #else:
                    #best_answer = None

                legal_info = {
                    "law": related_law,
                    "prec": related_prec
                }
            
            else:  # 챗봇의 답변 오류 메세지
                best_answer = "질문에 대한 답변을 찾을 수 없어요. 상황에 대해서 정확히 입력해주세요!"
                request.session["messages"].append({"role": "assistant", "content": best_answer})
                legal_info = {
                    "law": None,
                    "prec": None
                }
                    
            response_data = {
                "best_answer": best_answer,
                "legal_info": legal_info
            }

            return JsonResponse(response_data)
        
        else:
            return JsonResponse({"error": "입력이 없습니다"}, status=400)

@csrf_exempt
def button_law(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            content = data.get('content')  # 'content'를 요청에서 추출
            print("Received data from frontend: ", content)
            result2 = law_search(content)
            
        #print("Request method: ", request.method)
        #print("Request body: ", request.body)

        #law = request.POST.get('content')  # 'law'를 요청에서 추출
        
        #print("Received data from frontend: ", law)
        
        #result2 = law_search(law)
    
            if result2 is not None:
                data = {"content": result2, "status": 200}
                print(data)
                return JsonResponse({"data": data})
            else:
                return JsonResponse({"error": "Law not found"}, status=404)
        except json.JSONDecodeError:
        
            return JsonResponse({"error": "Invalid request method"}, status=400)

def law_search(law): # App Search에서 참조법령 찾기
    # 검색 옵션 설정 (score 점수 내림차순 정렬, 상위 1개 결과)
    search_options = {
        "sort": [{"_score": "desc"}],  # score 점수 내림차순 정렬
        "page": {"size": 1, "current": 1}  # 상위 1개 결과 (페이지 크기와 현재 페이지 번호를 지정)
    }

    law_content = ""

    engine_name = 'law-content' # 법령검색 App Search
    
    # search
    search_query = str(law)
    search_result = client.search(engine_name, search_query, search_options)

    title_fields = []
    content_fields = []

    # 필요한 필드들을 함께 저장
    for result in search_result['results']:
        score = result['_meta']['score']

        # 조항, 호, 목 필드 값이 있는 경우에만 'title_fields' 변수에 추가
        for field in ['law', 'jo', 'hang', 'ho', 'mok']:
            if field in result and result[field]['raw']:
                title_fields.append(result[field]['raw'])

        # content_fields를 추가
        for field in ['jo_content', 'hang_content', 'ho_content', 'mok_content']:
            if field in result and result[field]['raw']:
                content_fields.append(result[field]['raw'])
                
    # title_fields와 content_fields에 값이 있는 경우에 law_content에 추가
    if title_fields:
        law_content = "\n\n".join(title_fields)
    if content_fields:
        law_content += "\n\n" + "\n\n".join(content_fields) + "\n"
            
    #law_data = {"law_content": law_content}
    
    print(law_content)
    
    return law_content

@csrf_exempt
def button_prec(request) :
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            prec = data.get('prec')  # 'content'를 요청에서 추출
            print("Received data from frontend: ", prec)
            result2 = law_search(prec)
            
        #prec = request.POST.get('prec')  # 'prec'를 요청에서 추출
        
        #print("Received data from frontend: ", prec)
        
        #result2 = prec_search(prec)
        
            if result2 is not None:
                data = {"prec_content": result2, "status": 200}
                print(data)
                return JsonResponse({"data": data})
            else:
                return JsonResponse({"error": "Prec not found"}, status=404)
        except json.JSONDecodeError:
        
            return JsonResponse({"error": "Invalid request method"}, status=400)

def prec_search(prec): # App Search 에서 참조판례 찾기
    # 검색 옵션 설정 (score 점수 내림차순 정렬, 상위 1개 결과)
    search_options = {
        "sort": [{"_score": "desc"}],  # score 점수 내림차순 정렬
        "page": {"size": 1, "current": 1}  # 상위 1개 결과
    }

    # 결과를 딕셔너리로 저장
    prec_data = {}
    
    engine_name = 'prec-search'
    
    # search
    search_query = f'precise_query="{prec}"'
    search_result = client.search(engine_name, search_query, search_options)

    for result in search_result['results']:
        score = result['_meta']['score']

        # 필요한 필드들을 함께 출력
        fields_to_print = ['사건명', '사건번호', '선고일자', '법원명', '사건종류명', '판시사항', '판결요지', '참조조문', '참조판례', '판례내용']
        
        # 결과 문자열 생성
        for field in fields_to_print:
            if field in result:
                field_value = result[field]['raw']
                formatted_field_name = f"{field}"  # 필드명 굵은 글씨
                if not field_value:
                    continue
                if field == '선고일자':
                    try:
                        date_value = datetime.datetime.strptime(str(int(field_value)), '%Y%m%d').strftime('%Y.%m.%d')
                        prec_data[field] = date_value
                    except ValueError:
                        prec_data[field] = field_value
                elif field in ['법원명', '사건종류명']:
                    if field_value:
                        prec_data[field] = field_value
                elif field == '판시사항':
                    if field_value:
                        field_value = field_value.replace('[', '\n[')  # '['가 나오면 '[' 앞에 줄바꿈 추가
                        prec_data[field] = "\n\n" + "-" * 40 + "\n" + f"\n{formatted_field_name}:\n\n{field_value}\n\n" + "-" * 40
                elif field == '판결요지':
                    if field_value:
                        field_value = field_value.replace('[', '\n[')  # '['가 나오면 '[' 앞에 줄바꿈 추가
                        prec_data[field] = f"\n{formatted_field_name}:\n\n{field_value}\n\n" + "-" * 40
                elif field == '참조조문':
                    if field_value:
                        field_value = field_value.replace('/', '\n\n')  # '/'를 기준으로 줄바꿈 후 '/' 삭제
                        prec_data[field] = f"\n{formatted_field_name}:\n\n{field_value}\n\n" + "-" * 40
                elif field == '참조판례':
                    if field_value:
                        field_value = field_value.replace('/', '\n\n')  # '/'를 기준으로 줄바꿈 후 '/' 삭제
                        prec_data[field] = f"\n{formatted_field_name}:\n\n{field_value}\n\n" + "-" * 40
                elif field == '판례내용':
                    if field_value:
                        field_value = field_value.replace('【', '\n\n【')  # '【'가 나오면 '【' 앞에 줄바꿈 추가
                        prec_data[field] = f"{formatted_field_name}:\n\n{field_value}\n\n" + "-" * 40
                else:
                    if field == '사건명':
                        prec_data[field] = f"{formatted_field_name} {field_value}\n\n"  # 사건명 출력 시 콜론을 출력하지 않음
                    elif field == '사건번호':
                        prec_data[field] = f"{formatted_field_name}: {field_value}\n\n"  # 사건번호 출력 시 콜론을 출력함
                    else:
                        prec_data[field] = f"{formatted_field_name}: {field_value}\n"
        
    return prec_data