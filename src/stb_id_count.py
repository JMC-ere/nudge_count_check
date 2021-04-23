import json
import src.day_nudge_count
from elasticsearch import Elasticsearch

from query import query


def stb_id_count():
    # Connection Information Read
    with open('../config/connect_info.json', 'r') as f:
        config = json.load(f)

    # nudge count
    result_stb_count_list = []

    # ES Connect
    es_client = ''

    try:
        es_client = Elasticsearch([config['ES']['COMPLETE_IP1'],
                                   config['ES']['COMPLETE_IP2'],
                                   config['ES']['COMPLETE_IP3'],
                                   config['ES']['COMPLETE_IP4'],
                                   config['ES']['COMPLETE_IP5']],
                                  port=9200, max_retries=500, timeout=30,
                                  http_auth=(config['ES']['ES_COMPLETE_USER'], config['ES']['ES_COMPLETE_PWD']))
        es_client.info()
    except ConnectionError as con_err:
        print("ES Connection Error :", con_err)

    try:
        # STB_ID Count
        nudge_type = []

        # Get nudge_type_name
        for type_id in src.day_nudge_count.nudge_count():
            type_set = set(type_id.keys())
            nudge_type.append(type_set)
        del nudge_type[len(nudge_type)-1]

        for result_type in nudge_type:
            result_type = str(result_type).replace("{", "").replace("}", "").replace("'", '"')
            response = es_client.search(index=config['ES']['COMPLETE_ALL'], body=query.STB_COUNT % result_type)
            stb_count = response['aggregations']['group_by_state']['value']
            stb_count_dict = {result_type.replace('"', ""): stb_count}
            result_stb_count_list.append(stb_count_dict)

    except Exception as err:
        print("STB_ID COUNT ERROR", err)

    try:
        # Total STB_ID Count
        response = es_client.search(index=config['ES']['COMPLETE_ALL'], body=query.TOTAL_STB_COUNT)
        total_count = response['aggregations']['group_by_state']
        total_stb_count_dict = {"stb_total": total_count["value"]}
        result_stb_count_list.append(total_stb_count_dict)

    except Exception as err:
        print("TOTAL STB_ID COUNT ERROR", err)

    return result_stb_count_list
