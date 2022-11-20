import requests
from bs4 import BeautifulSoup

def main():
    cookies = {
        '_CIAN_GK': '60db38ea-50d7-408f-9633-208c60117be2',
        'adb': '1',
        'login_mro_popup': '1',
        '_gcl_au': '1.1.1346659849.1668503805',
        '_ga': 'GA1.2.696808565.1668503805',
        '_gid': 'GA1.2.505507560.1668503805',
        'sopr_utm': '%7B%22utm_source%22%3A+%22direct%22%2C+%22utm_medium%22%3A+%22None%22%7D',
        'sopr_session': 'a92f60540044467f',
        'uxfb_usertype': 'searcher',
        'tmr_lvid': '20c6e8b124f7cf8361dadc70645ab04f',
        'tmr_lvidTS': '1668503805227',
        '_ym_uid': '166850380599759126',
        '_ym_d': '1668503805',
        '_ym_isad': '1',
        'uxs_uid': '39c0c3f0-64c6-11ed-879e-3b851a7a15ad',
        '_gpVisits': '{"isFirstVisitDomain":true,"todayD":"Tue%20Nov%2015%202022","idContainer":"10002511"}',
        'afUserId': '2af92e5a-f8c0-4f1e-948a-1cf99c24d3cf-p',
        'AF_SYNC': '1668503806181',
        'session_region_id': '1',
        'session_main_town_region_id': '1',
        '_cc_id': 'c816c8e99d4f53a10235d781d4a75f1c',
        'panoramaId_expiry': '1668590669685',
        'distance_calculating_onboarding_counter': '1',
        '__cf_bm': 'aaGKdOlq0p15k_AUP91th27hsBZRNm8SwaRae1grA74-1668506838-0-AYfORa/LDBmfmDfzlfxyDp62LX4VupFMBYCQLra1HDhfvN/zMzRVLfbcJ1C1dRicGIB/vHvoDBaw3BoALgZk1n0=',
        'cookie_agreement_accepted': '1',
        '_ym_visorc': 'b',
        'hide_route_tab_onboarding': '1',
        '_gp10002511': '{"hits":4,"vc":1,"ac":1,"a6":1}',
        'tmr_reqNum': '48',
        '_dc_gtm_UA-30374201-1': '1',
    }

    headers = {
        'authority': 'api.cian.ru',
        'accept': '*/*',
        'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
        'content-type': 'text/plain;charset=UTF-8',
        # Requests sorts cookies= alphabetically
        # 'cookie': '_CIAN_GK=60db38ea-50d7-408f-9633-208c60117be2; adb=1; login_mro_popup=1; _gcl_au=1.1.1346659849.1668503805; _ga=GA1.2.696808565.1668503805; _gid=GA1.2.505507560.1668503805; sopr_utm=%7B%22utm_source%22%3A+%22direct%22%2C+%22utm_medium%22%3A+%22None%22%7D; sopr_session=a92f60540044467f; uxfb_usertype=searcher; tmr_lvid=20c6e8b124f7cf8361dadc70645ab04f; tmr_lvidTS=1668503805227; _ym_uid=166850380599759126; _ym_d=1668503805; _ym_isad=1; uxs_uid=39c0c3f0-64c6-11ed-879e-3b851a7a15ad; _gpVisits={"isFirstVisitDomain":true,"todayD":"Tue%20Nov%2015%202022","idContainer":"10002511"}; afUserId=2af92e5a-f8c0-4f1e-948a-1cf99c24d3cf-p; AF_SYNC=1668503806181; session_region_id=1; session_main_town_region_id=1; _cc_id=c816c8e99d4f53a10235d781d4a75f1c; panoramaId_expiry=1668590669685; distance_calculating_onboarding_counter=1; __cf_bm=aaGKdOlq0p15k_AUP91th27hsBZRNm8SwaRae1grA74-1668506838-0-AYfORa/LDBmfmDfzlfxyDp62LX4VupFMBYCQLra1HDhfvN/zMzRVLfbcJ1C1dRicGIB/vHvoDBaw3BoALgZk1n0=; cookie_agreement_accepted=1; _ym_visorc=b; hide_route_tab_onboarding=1; _gp10002511={"hits":4,"vc":1,"ac":1,"a6":1}; tmr_reqNum=48; _dc_gtm_UA-30374201-1=1',
        'origin': 'https://www.cian.ru',
        'referer': 'https://www.cian.ru/',
        'sec-ch-ua': '"Google Chrome";v="107", "Chromium";v="107", "Not=A?Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36',
    }

    data = '{"jsonQuery":{"_type":"flatsale","engine_version":{"type":"term","value":2},"room":{"type":"terms","value":[1,2,3,4,5,6,9,7]},"region":{"type":"terms","value":[2]},"sort":{"type":"term","value":"creation_date_desc"}}}'

    response = requests.post('https://api.cian.ru/search-offers/v2/search-offers-desktop/', cookies=cookies, headers=headers, data=data)
    
    data=response.json()
    print(data)
    # with open("file.json", "r") as read_file:
    #     data = json.load(read_file)
    #     print(data)
    # # return data

if __name__ == '__main__':
    main()