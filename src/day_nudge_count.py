import json
from elasticsearch import Elasticsearch

from query import query


def nudge_count():
    # Connection Information Read
    with open('../config/connect_info.json', 'r') as f:
        config = json.load(f)

    # nudge count
    nudge_count_list = []

    # ES Connect
    es_client = ''

    try:
        es_client = Elasticsearch([config['ES']['COMPLETE_IP1'],
                                   config['ES']['COMPLETE_IP2'],
                                   config['ES']['COMPLETE_IP3'],
                                   config['ES']['COMPLETE_IP4'],
                                   config['ES']['COMPLETE_IP5']],
                                  port=9200, max_retries=500,
                                  http_auth=(config['ES']['ES_COMPLETE_USER'], config['ES']['ES_COMPLETE_PWD']))
        es_client.info()
    except ConnectionError as con_err:
        print("ES Connection Error :", con_err)

    try:
        response = es_client.search(index=config['ES']['COMPLETE_ALL'], body=query.DAY_NUDGE_COUNT)
        buckets_list = response['aggregations']['group_by_state']['buckets']
        total_nudge_count = []
        for bucket in buckets_list:
            total_nudge_count.append(bucket['doc_count'])
            bucket_dict = {bucket['key']: bucket['doc_count']}
            nudge_count_list.append(bucket_dict)

        total = sum(total_nudge_count)
        total_dict = {"nudge_total": total}
        nudge_count_list.append(total_dict)

    except Exception as err:
        print("NUDGE COUNT ERROR", err)

    return nudge_count_list
