import requests
import json
from pprint import pprint

headers = {
    'accept': '*/*',
    'accept-encoding': 'gzip, deflate',
    'accept-language': 'fr-FR,fr;q=0.9',
    'content-type': 'application/json',
    'origin': 'https://ecosystem.lafrenchtech.com',
    'referer': 'https://ecosystem.lafrenchtech.com/',
    'sec-ch-ua': '".Not/A)Brand";v="99", "Google Chrome";v="103", "Chromium";v="103"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'cross-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36',
    'x-requested-with': 'XMLHttpRequest',
    'x-dealroom-app-id': '060818060'

}


def get_all_companies(limit=None):
    results = []
    offset = 0

    while True:
        new_result = search_companies(offset)
        if (limit and len(results) >= limit) or not new_result:
            break
        results += new_result
        offset += 25
    return results


def search_companies(offset=0):
    payload = {
        "fields": "id,angellist_url,appstore_app_id,client_focus,company_status,core_side_value,corporate_industries,create_date,crunchbase_url,employee_12_months_growth_delta,employee_12_months_growth_percentile,employee_12_months_growth_relative,employee_12_months_growth_unique,employee_3_months_growth_delta,employee_3_months_growth_percentile,employee_3_months_growth_relative,employee_3_months_growth_unique,employee_6_months_growth_delta,employee_6_months_growth_percentile,employee_6_months_growth_relative,employee_6_months_growth_unique,employees_chart,employees_latest,employees,entity_sub_types,facebook_url,founders_score_cumulated,founders,founders_top_university,founders_top_past_companies,fundings,fundings,growth_stage,has_strong_founder,has_super_founder,has_promising_founder,hq_locations,images,income_streams,industries,innovations,innovations_count,innovation_corporate_rank,investments,investors,is_editorial,is_ai_data,is_from_traderegister,latest_revenue_enhanced,latest_valuation_enhanced,launch_month,launch_year,linkedin_url,lists_ids,matching_score,name,participated_events,past_founders_raised_10m,past_founders,path,playmarket_app_id,revenues,sdgs,service_industries,similarweb_12_months_growth_delta,similarweb_12_months_growth_percentile,similarweb_12_months_growth_relative,similarweb_12_months_growth_unique,similarweb_3_months_growth_delta,similarweb_3_months_growth_percentile,similarweb_3_months_growth_relative,similarweb_3_months_growth_unique,similarweb_6_months_growth_delta,similarweb_6_months_growth_percentile,similarweb_6_months_growth_relative,similarweb_6_months_growth_unique,similarweb_chart,sub_industries,startup_ranking_rating,tags,tagline,technologies,total_funding_enhanced,total_jobs_available,trading_multiples,type,tech_stack,twitter_url,job_roles",
        "limit": 25,
        "offset": offset,
        "form_data": {
            "must": {
                "filters": {
                    "locations": {
                        "values": [
                            "France"
                        ],
                        "execution": "and"
                    },
                    "data_type": {
                        "values": [
                            "Verified"
                        ],
                        "execution": "or"
                    }
                },
                "execution": "and"
            },
            "should": {
                "filters": {

                }
            },
            "must_not": {
                "growth_stages": [
                    "mature"
                ],
                "company_type": [
                    "service provider",
                    "government nonprofit"
                ],
                "tags": [
                    "outside tech"
                ],
                "company_status": [
                    "closed"
                ]
            }
        },
        "keyword": None,
        "sort": "-last_funding_date"
    }
    r = requests.post(url="https://api.dealroom.co/api/v2/companies", headers=headers, data=json.dumps(payload))
    return r.json()["items"]


def get_company_info(url_page):
    def get_team(slug):
        url = 'https://api.dealroom.co/api/v2/entities/{}/team?limit=100&offset=0&show_past=true&no_editorial=true'.format(slug)
        r = requests.get(url=url, headers=headers)
        return r.json()

    def get_investments(slug):
        url = 'https://api.dealroom.co/api/v2/entities/{}/investments?show_exited=false&limit=25&offset=0&sort=-last_funding_date'.format(slug)
        r = requests.get(url=url, headers=headers)
        return r.json()

    def get_overview(slug):
        url = 'https://api.dealroom.co/api/v2/entities/{}?fields=achievements,affiliated_funds,aliases,angellist_url,app_12_months_growth_percentile,app_12_months_growth_unique,app_downloads_summary,appstore_app_id,can_edit,client_focus,closing_month,closing_year,company_status,core_side_value,corporate_industries,count_towards_employee_aggregates,country_experience,crunchbase_url,current_ownership,delivery_method,employee_12_months_growth_percentile,employee_12_months_growth_unique,employees_chart,employees_hq_chart,employees_latest,employees,entity_sub_types,events,exits_higher_800m,facebook_url,followers_summary,fundings_investor,growth_index_chart,growth_stage,hq_locations,id,images(100x100),income_streams,industries,industry_experience,innovations_count,investments_higher_800m,investments_num,investments,investor_exits_funding_enhanced,investor_exits_num,investor_total_rank,investor_total,investors,is_editorial,is_government,is_non_profit,is_strong_founder,is_super_founder,job_offers_total,kpi_summary,landscapes,last_funding,lastupdate_bobject,lastupdate,latest_valuation_enhanced,launch_month,launch_year,linkedin_url,lists_ids,lists,lp_investments,lp_investors,name,ownerships,path,places,playmarket_app_id,priori_appstore_app_id,priori_playmarket_app_id,revenues,rounds_experience,sdgs,service_industries,share_ticker_symbol,similarweb_12_months_growth_percentile,similarweb_12_months_growth_unique,similarweb_chart,similarweb_hidden,sub_industries,tagline,tags,team_total,tech_stack,technologies,total_funding_enhanced,trading_multiples,traffic_summary,traffic(top_countries,visitors),twitter_url,instagram_handle,type,vc_backed,vc_backed_manual,verify_date,verify_user,website_url&limit=25&offset=0'.format(slug)
        r = requests.get(url=url, headers=headers)
        return r.json()

    def get_analytics(slug):
        url = 'https://api.dealroom.co/api/v2/entities/{}/analytics?fields=facebook_likes_chart,twitter_tweets_chart,twitter_followers_chart,twitter_favorites_chart,instagram_followers_chart,instagram_posts_chart,growth_index_chart,similarweb_chart,employee_12_months_growth_delta_chart,app_downloads_ios_incremental_chart,app_downloads_android_incremental_chart,employees_chart,traffic,growth_stage,kpi_summary,similarweb_hidden,trading_multiples&limit=25&offset=0'.format(slug)
        r = requests.get(url=url, headers=headers)
        return r.json()

    def get_jobs(slug):
        url = 'https://api.dealroom.co/api/v2/entities/{}/jobs?limit=25&offset=0'.format(slug)
        r = requests.get(url=url, headers=headers)
        return r.json()

    def get_funds(slug):
        url = 'https://api.dealroom.co/api/v2/entities/{}/funds?limit=25&offset=0&sort=-new_fund_date'.format(slug)
        r = requests.get(url=url, headers=headers)
        return r.json()

    slug_now = url_page.split('/')[-1]

    dict_element_company = {
        'teams': get_team(slug_now),
        'investments': get_investments(slug_now),
        'overview': get_overview(slug_now),
        'analytics': get_analytics(slug_now),
        'jobs': get_jobs(slug_now),
        'funds': get_funds(slug_now)
    }
    return dict_element_company


if __name__ == "__main__":
    # for company in get_all_companies(25):
    #     dict_company = {
    #         'url_company': company['company_url']
    #     }
    #     dict_company.update(get_company_info(dict_company['url_company']))
    #
    # search_companies()
    pprint(get_company_info('https://ecosystem.lafrenchtech.com/companies/bnp'))


