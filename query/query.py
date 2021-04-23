# vod-recom - 본방사수 실패한 콘텐츠 제안
# interest - 관심 콘텐츠의 신규 에피소드
# active - 관심 VOD
# prepurchase - 구매 중 이탈 콘텐츠 가격할인
# nolgs - 시청 종료일이 다가오는 콘텐츠 시청 제안
# zapping - Zapping시 콘텐츠 제안
# noresult - 검색시 미수급 콘텐츠 수급
# dcmark - 찜하고 시청하지않은 콘텐츠 가격할인

DAY_NUDGE_COUNT = """
{
  "size": 0, 
  "query": {
    "match_all": {}
  },"aggs": {
    "group_by_state": {
      "terms": {
        "field": "nudge_type",
        "size": 1000
      }
    }
  }
}
"""
TOTAL_STB_COUNT = """
{
  "size": 0, 
  "aggs": {
    "group_by_state": {
      "cardinality": {
        "field": "stb_id"
      }
    }
  }
}
"""
STB_COUNT = """
{
  "size": 0, 
  "query": {
    "bool": {
      "filter": [
        {
          "term": {
            "nudge_type": %s
          }
        }
      ]
    }
  },"aggs": {
    "group_by_state": {
      "cardinality": {
        "field": "stb_id"
      }
    }
  }
}
"""
NUDGE_DSL = """
{
  "size": 0, 
  "aggs": {
    "group_by_state": {
      "cardinality": {
        "field": "stb_id"
      }
    }
  }
}
"""
NUDGE_7_TEXT = """
{
  "size": 0, 
  "aggs": {
    "NAME": {
      "cardinality": {
        "field": "stb_id"
      }
    }
  }
}
"""
NUDGE_7_VOICE = """
{
  "size": 0, 
  "aggs": {
    "NAME": {
      "cardinality": {
        "field": "messageJson.params.stb_id"
      }
    }
  }
}
"""
