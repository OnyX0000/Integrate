from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk
from sentence_transformers import SentenceTransformer, util
import re # 정규식
from elastic_app_search import Client
import json
import datetime

def bulk_indexing(model):
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
    
    bulk_data = []
    for doc in model.objects.all():
        bulk_data.append(
            {
                '_op_type': 'index',
                '_index': 'legal_qa_final',
                '_id': doc.id,
                '_source': {
                    'question': doc.question,
                    'answer': doc.answer,
                    'law': doc.law,
                    'prec': doc.prec,
                    'embedding': doc.embedding
                }
            }
        )
    success, _ = bulk(es, bulk_data)
    return success