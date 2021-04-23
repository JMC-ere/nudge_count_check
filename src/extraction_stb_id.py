import json
from query import query
from elasticsearch import Elasticsearch


def extraction_stb_count():
    # Connection Information Read
    with open('../config/connect_info.json', 'r') as f:
        config = json.load(f)

    # Extraction_STB_Count
    extraction_count_list = []

    # ES Connect
    es_client = ''

    try:
        es_client = Elasticsearch([config['ES']['ETL_IP1'],
                                   config['ES']['ETL_IP2'],
                                   config['ES']['ETL_IP3']],
                                  port=9200, max_retries=500, timeout=30,
                                  http_auth=(config['ES']['ES_USER'], config['ES']['ES_PWD']))
        es_client.info()
    except ConnectionError as con_err:
        print("ES Connection Error :", con_err)

    try:
        # Extraction STB_ID Count 3
        response = es_client.search(index=config['ES']['PLAY_LIVE'], body=query.NUDGE_DSL)
        nudge_3_count = response['aggregations']['group_by_state']['value']
        nudge_3 = {'nudge_3': nudge_3_count}
        extraction_count_list.append(nudge_3)
    except Exception as err:
        print("NUDGE 3 COUNT ERROR", err)

    try:
        # Extraction STB_ID Count 4
        response = es_client.search(index=config['ES']['PLAY'], body=query.NUDGE_DSL)
        nudge_4_count = response['aggregations']['group_by_state']['value']
        nudge_4 = {'nudge_4': nudge_4_count}
        extraction_count_list.append(nudge_4)
    except Exception as err:
        print("NUDGE 4 COUNT ERROR", err)

    try:
        # Extraction STB_ID Count 5
        response = es_client.search(index=config['ES']['ORDER'], body=query.NUDGE_DSL)
        nudge_5_count = response['aggregations']['group_by_state']['value']
        nudge_5 = {'nudge_5': nudge_5_count}
        extraction_count_list.append(nudge_5)
    except Exception as err:
        print("NUDGE 5 COUNT ERROR", err)

    try:
        # Extraction STB_ID Count 7

        # TEXT Count
        response_text = es_client.search(index=config['ES']['TEXT'], body=query.NUDGE_7_TEXT)
        nudge_7_text_count = response_text['aggregations']['NAME']['value']

        # VOICE Count
        response_voice = es_client.search(index=config['ES']['VOICE'], body=query.NUDGE_7_VOICE)
        nudge_7_voice_count = response_voice['aggregations']['NAME']['value']

        nudge_7_count = nudge_7_voice_count + nudge_7_text_count
        nudge_7 = {"nudge_7": nudge_7_count}
        extraction_count_list.append(nudge_7)

    except Exception as err:
        print("NUDGE 7 COUNT ERROR", err)

    try:
        # Extraction STB_ID Count 8
        response = es_client.search(index=[config['ES']['ORDER-2'], config['ES']['ORDER-7']], body=query.NUDGE_DSL)
        nudge_8_count = response['aggregations']['group_by_state']['value']
        nudge_8 = {'nudge_8': nudge_8_count}
        extraction_count_list.append(nudge_8)
    except Exception as err:
        print("NUDGE 8 COUNT ERROR", err)

    try:
        # Extraction STB_ID Count 9
        response = es_client.search(index=[config['ES']['UNION_SEARCH'], config['ES']['UNION_SYNOPSIS']], body=query.NUDGE_DSL)
        nudge_9_count = response['aggregations']['group_by_state']['value']
        nudge_9 = {'nudge_9': nudge_9_count}
        extraction_count_list.append(nudge_9)
    except Exception as err:
        print("NUDGE 9 COUNT ERROR", err)

    try:
        # Sum Extraction STB_ID Count
        response = es_client.search(index=[config['ES']['PLAY_LIVE'],
                                           config['ES']['PLAY'],
                                           config['ES']['ORDER'],
                                           config['ES']['TEXT'],
                                           config['ES']['VOICE'],
                                           config['ES']['ORDER-2'],
                                           config['ES']['ORDER-7'],
                                           config['ES']['UNION_SEARCH'],
                                           config['ES']['UNION_SYNOPSIS']], body=query.NUDGE_DSL)
        nudge_sum_count = response['aggregations']['group_by_state']['value']
        nudge_sum = {'nudge_sum': nudge_sum_count}
        extraction_count_list.append(nudge_sum)
    except Exception as err:
        print("NUDGE SUM COUNT ERROR", err)

    return extraction_count_list
