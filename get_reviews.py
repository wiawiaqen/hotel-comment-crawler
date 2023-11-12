import aiohttp
import asyncio
import os
import json
import time

url = "https://www.agoda.com/api/cronos/property/review/ReviewComments"
headers = {
    "cookie": 'agoda.vuser=UserId=bc8ae5ca-cea4-42e5-a0a4-bb009ac4d436; agoda.user.03=UserId=69459c0c-41b2-4dd5-85c2-63db55c8793c; agoda.prius=PriusID=0&PointsMaxTraffic=Agoda; agoda.price.01=PriceView=1; _40-40-20Split=Group20; _ab50group=GroupB; deviceId=2a9b4507-a9c8-4cf7-8f7f-ab305bf3f4bc; FPID=FPID2.2.LzSK87qYF2O28lIU%2B%2BMCrdtXX%2FLDZH%2BpKn40n6qrW5c%3D.1659451742; ab.storage.userId.d999de98-30bc-4346-8124-a15900a101ae=%7B%22g%22%3A%2269459c0c-41b2-4dd5-85c2-63db55c8793c%22%2C%22c%22%3A1659451745050%2C%22l%22%3A1659451745050%7D; ab.storage.deviceId.d999de98-30bc-4346-8124-a15900a101ae=%7B%22g%22%3A%220003dc5e-fd63-53cc-380a-0d8ac40d5002%22%2C%22c%22%3A1659451745058%2C%22l%22%3A1659451745058%7D; _gcl_aw=GCL.1659451746.CjwKCAjwlqOXBhBqEiwA-hhitLF9TZL1ZSCG_IQoG_Fd15N-6M5Y_WM6iiauNnmY-EUG7QjuVmPHYBoCp3EQAvD_BwE; __gads=ID=232ead09695636ac:T=1659451747:S=ALNI_Ma3neTzQc9fKxNsZ9JoERp65R__pQ; _cc_id=7b9f9aef57219c2ac881e27153b22aa2; agoda.familyMode=Mode=0; agoda.lastclicks=1891474||99f03749-3c7e-589e-fa81-305d021c7a12||2022-08-14T00:02:45||g3weksayiqd0e0u53buse14j||{"IsPaid":true,"gclid":"CjwKCAjw0dKXBhBPEiwA2bmObfzovq85fRKb73oWpWUUZu_ag7OuzGZZW_44Y38MmMbSNsN4TN_g6BoC0T4QAvD_BwE","Type":""}; tealiumEnable=true; _gid=GA1.2.1941826582.1660735661; _ha_aw=GCL.1660740402.CjwKCAjw0dKXBhBPEiwA2bmObfzovq85fRKb73oWpWUUZu_ag7OuzGZZW_44Y38MmMbSNsN4TN_g6BoC0T4QAvD_BwE; _hab_aw=GCL.1660740402.CjwKCAjw0dKXBhBPEiwA2bmObfzovq85fRKb73oWpWUUZu_ag7OuzGZZW_44Y38MmMbSNsN4TN_g6BoC0T4QAvD_BwE; _gac_UA-6446424-30=1.1660740403.CjwKCAjw0dKXBhBPEiwA2bmObfzovq85fRKb73oWpWUUZu_ag7OuzGZZW_44Y38MmMbSNsN4TN_g6BoC0T4QAvD_BwE; agoda.firstclicks=-1||||2022-08-19T00:59:30||o1wsnwaqkd2qf2w1kcfcl50g||{"IsPaid":false,"gclid":"","Type":""}; agoda.version.03=CookieId=72cde216-5009-40bd-a0f3-268561c42391&AllocId=7b0538d37625b11a8118d4d7b862becbce07ee7354c8640f2c8cabeac59f8e14375892b665e1e57d80a3df57d3f7a617937c07ef4fffdf8e0ca8a77eaa1d019653ca795e0c513788175518053e23da62eb3ccd702d72cde21650090bd0f3268561c42391&DLang=vi-vn&CurLabel=VND&DPN=1&Alloc=&FEBuildVersion=&TItems=2$-1$08-19-2022 00:59$09-18-2022 00:59$&CuLang=24; agoda.attr.03=ATItems=1891474$08-14-2022 00:02$99f03749-3c7e-589e-fa81-305d021c7a12|-1$08-19-2022 00:59$; agoda.landings=-1|||o1wsnwaqkd2qf2w1kcfcl50g|2022-08-19T00:59:30|False|19----1891474|99f03749-3c7e-589e-fa81-305d021c7a12|CjwKCAjw0dKXBhBPEiwA2bmObfzovq85fRKb73oWpWUUZu_ag7OuzGZZW_44Y38MmMbSNsN4TN_g6BoC0T4QAvD_BwE|g3weksayiqd0e0u53buse14j|2022-08-14T00:02:45|True|20-----1|||o1wsnwaqkd2qf2w1kcfcl50g|2022-08-19T00:59:30|False|99; ASP.NET_SessionId=o1wsnwaqkd2qf2w1kcfcl50g; __gpi=UID=0000082934541f19:T=1659451747:RT=1660883435:S=ALNI_MaORuvVmSiTbbwsbYWEM9PhDfOXCQ; panoramaId_expiry=1661488236399; panoramaId=00554afbf6c84acf51f4a120de584945a702575c357a7175125c13b4f257b24b; xsrf_token=CfDJ8Dkuqwv-0VhLoFfD8dw7lYwRQp-HE9ygDsPI--L537EAGPQ9hFqKXuTmkJrtBijrpym4kujLceNLChljtaX5SJ187-yO5DezyijI-TYh04Lc5EYq85HkiSUKnXPCldP9ZFa9t2VvE4ZIYeQikp0e-iM; FPLC=Lpyy7OxUquHPq1Ky0XcpXbopeQr97nxZ%2FhwvN1KjtxL6Y9cR%2ByNhp163Fz%2FJrfO1zVqRciUG8HGsmMC0XSmkcj0tC%2FDvDyjeSf0YVzTTRAOLJGiv3AmCCkBlUxZu7w%3D%3D; ab.storage.sessionId.d999de98-30bc-4346-8124-a15900a101ae=%7B%22g%22%3A%225ef3ce77-ac50-159a-1ad2-75d01b71415b%22%2C%22e%22%3A1660896419139%2C%22c%22%3A1660894619102%2C%22l%22%3A1660894619139%7D; agoda.search.01=SHist=1$226464$7909$1$1$1$0$0$$|1$17162$7909$1$1$1$0$0$$|1$105991$7909$1$1$1$0$0$$|1$106067$7909$1$1$1$0$0$$|1$78906$7909$1$1$1$0$0$$|1$204057$7909$1$1$1$0$0$$|1$115625$7909$1$1$1$0$0$$|1$204056$7909$1$1$1$0$0$$|1$204063$7909$1$1$1$0$0$$|1$214967$7909$1$1$1$0$0$$|1$204059$7909$1$1$1$0$0$$|1$226502$7909$1$1$1$0$0$$|1$115754$7909$1$1$1$0$0$$|1$115751$7909$1$1$1$0$0$$|1$720974$7909$1$1$1$0$0$$|1$19657$7909$1$1$1$0$0$$|1$115734$7909$1$1$1$0$0$$|1$204067$7909$1$1$1$0$0$$|1$115629$7909$1$1$1$0$0$$|1$115753$7909$1$1$1$0$0$$|1$204064$7909$1$1$1$0$0$$|1$115635$7909$1$1$1$0$0$$|1$204053$7909$1$1$1$0$0$$|1$204055$7909$1$1$1$0$0$$|1$204058$7909$1$1$1$0$0$$|1$204061$7909$1$1$1$0$0$$|1$204071$7909$1$1$1$0$0$$|1$204065$7909$1$1$1$0$0$$|1$115748$7909$1$1$1$0$0$$|1$222541$7909$1$1$1$0$0$$|1$115651$7909$1$1$1$0$0$$|1$115658$7909$1$1$1$0$0$$|1$204070$7909$1$1$1$0$0$$|1$728004$7909$1$1$1$0$0$$|1$215124$7909$1$1$1$0$0$$|1$18867$7909$1$1$1$0$0$$|1$115657$7909$1$1$1$0$0$$|4$2320499$7909$1$1$1$0$0$$|1$13170$7909$1$1$1$0$0$$|4$2838433$7909$1$1$1$0$0$$&H=7900|7$5869838|5$5869838|4$10984$1951432$10990$1951432$10984|2$1158058$297330$10984$401248|0$2320499$2838433; agoda.analytics=Id=1200415306712663159&Signature=1197611095078720666&Expiry=1660906415603; _ga_T408Z268D2=GS1.1.1660902820.17.1.1660902820.60.0.0; utag_main=v_id:01825f0817820075450544823adc05086011607e00978$_sn:16$_se:2$_ss:0$_st:1660904621611$ses_id:1660902816109%3Bexp-session$_pn:1%3Bexp-session; _ga=GA1.2.406930584.1659451742; _uetsid=9ba407301e1f11edaef951fbd7dfa76f; _uetvid=42dd5070127211eda811d9f5711b3836; _clck=1u7wmly|1|f45|0; cto_bundle=5qywNF85NjJZZ0trciUyQnA0eXZQVUVDaE1FeTRJdkhMcUFDdHQ2Uk9YUm9vRXM1V3J3QURXQzZyUXZ3N2gxSWdGQmw4aHRZWGNocG5EOVJDcSUyQm5FT3pjOG4zV2lBbXc0MUZEVU0lMkZPbExIMDVFWHJQQ1VNbEJldFBCVldvWDNWVklIYUJIMXdpYW01eDVVU1VKJTJCMFRPUXVDRnBTZyUzRCUzRA; _clsk=qis8pw|1660902823773|1|0|n.clarity.ms/collect',
    "cr-currency-code": "VND",
    "origin": "https://www.agoda.com",
    "referer": "https://www.agoda.com/vi-vn/green-star-hotel_2/hotel/ho-chi-minh-city-vn.html?finalPriceView=1&isShowMobileAppPrice=false&cid=-1&numberOfBedrooms=&familyMode=false&adults=1&children=0&rooms=1&maxRooms=0&checkIn=2022-08-28&isCalendarCallout=false&childAges=&numberOfGuest=0&missingChildAges=false&travellerType=-1&showReviewSubmissionEntry=false&currencyCode=VND&isFreeOccSearch=false&isCityHaveAsq=false&tspTypes=16&los=1&searchrequestid=a871e79b-1f5b-4a8f-9ccb-c9e7c1406dce",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.81 Safari/537.36 Edg/104.0.1293.54",
    "accept-encoding": "gzip, deflate, br",
    "pragma": "no-cache",
    "accept-language": "en-US,en;q=0.9,vi;q=0.8",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "x-requested-with": "XMLHttpRequest",
    "accept": "application/json",
    "sec-ch-ua-mobile": "?0",
}


async def get_page(
    session: aiohttp.ClientSession,
    hotel_ID: int,
    offset: int,
    URL: str = url,
    HEADERS: dict = headers,
) -> dict:
    """
    Get data from hotel page offset of hotel_ID

    Args:
        session (aiohttp.ClientSession): aiohttp session
        hotel_ID (int): hotel ID
        offset (int): hotel page offset
        URL (str, optional): url. Defaults to url.
        HEADERS (dict, optional): headers. Defaults to headers.

    Returns:
        dict: data
    """
    payload = {
        "hotelId": hotel_ID,
        "providerId": 332,
        "demographicId": 0,
        "page": offset // 20 + 1,
        "pageSize": 20,
        "sorting": 7,
        "providerIds": [332],
        "isReviewPage": False,
        "isCrawlablePage": True,
        "filters": {"language": [24], "room": []},
        "searchKeyword": "",
        "searchFilters": [],
    }
    try:
        async with session.request(
            "POST", URL, headers=HEADERS, json=payload
        ) as response:
            data = await response.json()
            return data
    except:
        pass


async def get_all(session: aiohttp.ClientSession) -> list[asyncio.Task]:
    """
    get all data from hotel

    Args:
        session (aiohttp.ClientSession): aiohttp session

    Returns:
        list[asyncio.Task]: list of task
    """
    global local_dir, province
    tasks = []
    # get all json file in folder Hotel
    files = os.listdir(local_dir)
    for file in files:
        # create directory for each province
        if not os.path.exists(f"./Data/{province}"):
            os.makedirs(f"./Data/{province}")
        try:
            with open(f"./Hotel/{province}/{file}", "r", encoding="utf-8") as f:
                data = json.load(f)
                for object in data:
                    if object["total_reviews"] == 0:
                        continue
                    total_review = range(0, object["total_reviews"], 20)
                    id = object["id"]
                    for i in total_review:
                        tasks.append(asyncio.create_task(get_page(session, id, i)))
                res = await asyncio.gather(*tasks)
                return res
        except Exception as e:
            print(e)


def get_all_usable_data_from_response(response: dict):
    """
    Extract usable data from response

    Args:
        response (dict): response
    """
    lst = []
    try:
        usable_data = response["comments"]
    except:
        return []
    for item in usable_data:
        review = {}
        try:
            review["reviewer_name"] = item["reviewerInfo"]["displayMemberName"]
        except:
            review["reviewer_name"] = None
        try:
            review["reviewer_country"] = item["reviewerInfo"]["countryName"]
        except:
            review["reviewer_country"] = None
        try:
            review["language"] = item["responseTranslateSource"]
        except:
            review["language"] = None
        try:
            review["stay_length"] = item["reviewerInfo"]["lengthOfStay"]
        except:
            review["stay_length"] = None
        try:
            review["review_date"] = item["formattedReviewDate"]
        except:
            review["review_date"] = None
        try:
            review["groupName"] = item["reviewerInfo"]["reviewGroupName"]
        except:
            review["groupName"] = None
        try:
            review["typeName"] = item["reviewerInfo"]["roomTypeName"]
        except:
            review["typeName"] = None
        try:
            review["rating"] = item["rating"]
        except:
            review["rating"] = None
        try:
            review["rating_text"] = item["ratingText"]
        except:
            review["rating_text"] = None
        try:
            review["review_title"] = item["reviewTitle"]
        except:
            review["review_title"] = None
        try:
            review["review_comments"] = item["reviewComments"]
        except:
            review["review_comments"] = None
        try:
            review["review_positive_comments"] = item["reviewPositives"]
        except:
            review["review_positive_comments"] = None
        try:
            review["review_negative_comments"] = item["reviewNegatives"]
        except:
            review["review_negative_comments"] = None
        lst.append(review)

    global i, local_dir_for_data, no
    with open(
        f"{local_dir_for_data}/data_page{no}.json", "w", encoding="utf-8"
    ) as file:
        if lst != []:
            json.dump(lst, file, indent=4, ensure_ascii=False)
            no += 1
        file.close()


async def main():
    async with aiohttp.ClientSession() as session:
        res = await get_all(session)
        try:
            for i in res:
                get_all_usable_data_from_response(i)
            return res
        except:
            return


if __name__ == "__main__":
    start = time.time()
    files = os.listdir("./Hotel")
    for i in range(0, len(files)):
        dir_start = time.time()
        no = 0
        local_dir = f"./Hotel/{files[i]}"
        province = files[i].split("/")[-1]
        local_dir_for_data = f"./Data/{province}"
        if not os.path.exists(local_dir_for_data):
            os.makedirs(local_dir_for_data)
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
        asyncio.run(main())
        print(f"Dir {files[i]} Done in {time.time() - dir_start} seconds")
    print(f"Done in {time.time() - start} seconds")
