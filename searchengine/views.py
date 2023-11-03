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

def home(request):
    return render(request, 'main.html')

def searchengine(request):
    if request.method == 'GET':
        return render(request, 'searchEngine.html')

def search_engine(request):
    #if request.method == 'GET':
        #return render(request, 'searchEngine.html')

    if request.method == 'POST':
        search_query = request.POST.get('search_query', '')  # Get the search query from the POST request

        if search_query:
            # Your Elasticsearch and Appsearch code here
            # Ensure you define 'search_options' and perform the search on both engines

            # Replace 'st.write' with the appropriate way to store and pass data to your template
            search_results_engine_1 = []
            search_results_engine_2 = []

            for result in search_results_engine_1['results']:
                # Process and store the results for Engine 1
                search_results_engine_1.append({
                    'law_name': result.get('law', {}).get('raw', ''),
                    # Add other fields as needed
                })

            for result in search_results_engine_2['results']:
                # Process and store the results for Engine 2
                search_results_engine_2.append({
                    '사건명': result.get('사건명', {}).get('raw', ''),
                    # Add other fields as needed
                })

            return render(request, 'search_results.html', {
                'search_results_engine_1': search_results_engine_1,
                'search_results_engine_2': search_results_engine_2,
            })

        return JsonResponse({'message': 'No search query provided'})

