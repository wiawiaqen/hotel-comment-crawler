import json
import aiohttp
import asyncio
import time
import datetime


async def get_data(session: aiohttp.ClientSession, province_ID: int, name: str) -> dict:
    """
    get data from agoda.com

    Args:
        session (aiohttp.ClientSession): Aiohttp session
        province_ID (int): Province ID
        name (str): Province name

    Returns:
        dict: Data of page
    """
    url = "https://www.agoda.com/graphql/search"
    headers = {
        "accept": "*/*",
        "ag-language-locale": "vi-vn",
        "cookie": 'agoda.vuser=UserId=bc8ae5ca-cea4-42e5-a0a4-bb009ac4d436; agoda.user.03=UserId=69459c0c-41b2-4dd5-85c2-63db55c8793c; agoda.prius=PriusID=0&PointsMaxTraffic=Agoda; agoda.price.01=PriceView=1; _40-40-20Split=Group20; _ab50group=GroupB; deviceId=2a9b4507-a9c8-4cf7-8f7f-ab305bf3f4bc; FPID=FPID2.2.LzSK87qYF2O28lIU%2B%2BMCrdtXX%2FLDZH%2BpKn40n6qrW5c%3D.1659451742; ab.storage.userId.d999de98-30bc-4346-8124-a15900a101ae=%7B%22g%22%3A%2269459c0c-41b2-4dd5-85c2-63db55c8793c%22%2C%22c%22%3A1659451745050%2C%22l%22%3A1659451745050%7D; ab.storage.deviceId.d999de98-30bc-4346-8124-a15900a101ae=%7B%22g%22%3A%220003dc5e-fd63-53cc-380a-0d8ac40d5002%22%2C%22c%22%3A1659451745058%2C%22l%22%3A1659451745058%7D; _gcl_aw=GCL.1659451746.CjwKCAjwlqOXBhBqEiwA-hhitLF9TZL1ZSCG_IQoG_Fd15N-6M5Y_WM6iiauNnmY-EUG7QjuVmPHYBoCp3EQAvD_BwE; __gads=ID=232ead09695636ac:T=1659451747:S=ALNI_Ma3neTzQc9fKxNsZ9JoERp65R__pQ; _cc_id=7b9f9aef57219c2ac881e27153b22aa2; panoramaId_expiry=1660880885618; panoramaId=00554afbf6c84acf51f4a120de584945a702575c357a7175125c13b4f257b24b; agoda.familyMode=Mode=0; agoda.lastclicks=1891474||99f03749-3c7e-589e-fa81-305d021c7a12||2022-08-14T00:02:45||g3weksayiqd0e0u53buse14j||{"IsPaid":True,"gclid":"CjwKCAjw0dKXBhBPEiwA2bmObfzovq85fRKb73oWpWUUZu_ag7OuzGZZW_44Y38MmMbSNsN4TN_g6BoC0T4QAvD_BwE","Type":""}; tealiumEnable=true; _gid=GA1.2.1941826582.1660735661; _ha_aw=GCL.1660740402.CjwKCAjw0dKXBhBPEiwA2bmObfzovq85fRKb73oWpWUUZu_ag7OuzGZZW_44Y38MmMbSNsN4TN_g6BoC0T4QAvD_BwE; _hab_aw=GCL.1660740402.CjwKCAjw0dKXBhBPEiwA2bmObfzovq85fRKb73oWpWUUZu_ag7OuzGZZW_44Y38MmMbSNsN4TN_g6BoC0T4QAvD_BwE; _gac_UA-6446424-30=1.1660740403.CjwKCAjw0dKXBhBPEiwA2bmObfzovq85fRKb73oWpWUUZu_ag7OuzGZZW_44Y38MmMbSNsN4TN_g6BoC0T4QAvD_BwE; agoda.firstclicks=-1||||2022-08-18T16:26:30||lnp4s4cef4h5vc354usxf4k5||{"IsPaid":False,"gclid":"","Type":""}; agoda.version.03=CookieId=72cde216-5009-40bd-a0f3-268561c42391&AllocId=7b0538d37625b11a8118d4d7b862becbce07ee7354c8640f2c8cabeac59f8e14375892b665e1e57d80a3df57d3f7a617937c07ef4fffdf8e0ca8a77eaa1d019653ca795e0c513788175518053e23da62eb3ccd702d72cde21650090bd0f3268561c42391&DLang=vi-vn&CurLabel=VND&DPN=1&Alloc=&FEBuildVersion=&TItems=2$-1$08-18-2022 16:26$09-17-2022 16:26$&CuLang=24; agoda.attr.03=ATItems=1891474$08-14-2022 00:02$99f03749-3c7e-589e-fa81-305d021c7a12|-1$08-18-2022 16:26$; agoda.landings=-1|||lnp4s4cef4h5vc354usxf4k5|2022-08-18T16:26:30|False|19----1891474|99f03749-3c7e-589e-fa81-305d021c7a12|CjwKCAjw0dKXBhBPEiwA2bmObfzovq85fRKb73oWpWUUZu_ag7OuzGZZW_44Y38MmMbSNsN4TN_g6BoC0T4QAvD_BwE|g3weksayiqd0e0u53buse14j|2022-08-14T00:02:45|True|20-----1|||lnp4s4cef4h5vc354usxf4k5|2022-08-18T16:26:30|False|99; ASP.NET_SessionId=lnp4s4cef4h5vc354usxf4k5; xsrf_token=CfDJ8Dkuqwv-0VhLoFfD8dw7lYyBFRyVDLCfK4K-rh6CDaeimVNJClBQ0KJY03bRKnnCfpe6tFZSsy0xV2MwN9HHonIvNxL2z68GI3Ke0HxDFUz6vYmfxA1ziimKQKCNfxQUFrA6FSUwUliePoCGOzMMTi0; FPLC=EqH2DQIXNT2ihvNqJbD4CcD30GTIsHK0byO82KKl5QBEqn29yLv96xQ6XTdMjgzn%2FwKbOkS4KgQWG6N%2FIt4B%2ByXk97F%2B7PvpCC4Hct685cXZGp0dhClDWN5OeX4Eqw%3D%3D; __gpi=UID=0000082934541f19:T=1659451747:RT=1660814795:S=ALNI_MaORuvVmSiTbbwsbYWEM9PhDfOXCQ; agoda.search.01=SHist=4$5869838$7902$1$1$2$0$0$$$0|4$10990$7902$1$1$2$0$0$$$0|4$1951432$7902$1$1$2$0$0$$$0|4$10984$7902$1$1$2$0$0$$$0|1$13170$7902$1$1$2$0$0$$$0|1$2758$7907$1$1$2$0$0$$$0|1$13170$7907$1$1$1$0$0$$$0|1$2758$7907$1$1$1$0$0$$$0|1$13170$7908$1$1$1$0$0$$$0|1$16440$7908$1$1$1$0$0$$$0&H=7898|5$5869838|3$5869838|2$10984$1951432$10990$1951432$10984|0$1158058$297330$10984$401248; agoda.analytics=Id=8952761739386372349&Signature=8527929413596593598&Expiry=1660825721599; utag_main=v_id:01825f0817820075450544823adc05086011607e00978$_sn:11$_se:22$_ss:0$_st:1660823926700$ses_id:1660820153867%3Bexp-session$_pn:6%3Bexp-session; _ga=GA1.2.406930584.1659451742; ab.storage.sessionId.d999de98-30bc-4346-8124-a15900a101ae=%7B%22g%22%3A%221c6bd0cc-91b0-6c89-a6f4-b656ea9ee7bb%22%2C%22e%22%3A1660823927756%2C%22c%22%3A1660820159452%2C%22l%22%3A1660822127756%7D; _uetsid=9ba407301e1f11edaef951fbd7dfa76f; _uetvid=42dd5070127211eda811d9f5711b3836; _gat_t3=1; cto_bundle=8nv11V9HdmZkRnVQdXpPNnJpazJZZW43eno4alR1a0cxdkVDdXVvUDJ4Q0tSam9jcGNhYXVoRFNjWEtWdDBLbUR1b2Q2R0NxSlJPRURiSVE2Smp4Rzl6MkZKSEhsaHVFVjlGWDBJemwzSmpQVERrNUpTQkhVWHVTMm0yc2g2emM4WlUlMkJzRDlWUHJOSzZFSTlIUk9JbzhzQzlpdyUzRCUzRA; _ga_T408Z268D2=GS1.1.1660820152.11.1.1660822128.56.0.0; _gali=paginationNext',
        "origin": "https://www.agoda.com",
        "referer": "https://www.agoda.com/vi-vn/search?city=13170",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "content-type": "application/json",
        "sec-fetch-site": "same-origin",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.81 Safari/537.36 Edg/104.0.1293.54",
    }
    global today_time, oneweek_later
    payload = {
        "operationName": "citySearch",
        "variables": {
            "CitySearchRequest": {
                "cityId": int(province_ID),
                "searchRequest": {
                    "searchCriteria": {
                        "isAllowBookOnRequest": True,
                        "bookingDate": f"{today_time}T08:51:14.005Z",
                        "checkInDate": f"{oneweek_later}T08:51:11.614Z",
                        "localCheckInDate": f"{oneweek_later}T08:51:11.614Z",
                        "los": 1,
                        "rooms": 1,
                        "adults": 1,
                        "children": 0,
                        "childAges": [],
                        "ratePlans": [],
                        "featureFlagRequest": {
                            "fetchNamesForTealium": True,
                            "fiveStarDealOfTheDay": True,
                            "isAllowBookOnRequest": True,
                            "showUnAvailable": True,
                            "showRemainingProperties": True,
                            "isMultiHotelSearch": False,
                            "enableAgencySupplyForPackages": True,
                            "flags": [
                                {
                                    "feature": "FamilyChildFriendlyPopularFilter",
                                    "enable": True,
                                },
                                {
                                    "feature": "FamilyChildFriendlyPropertyTypeFilter",
                                    "enable": True,
                                },
                                {"feature": "FamilyMode", "enable": False},
                            ],
                            "enablePageToken": True,
                            "enableDealsOfTheDayFilter": False,
                            "isEnableSupplierFinancialInfo": False,
                            "ignoreRequestedNumberOfRoomsForNha": False,
                        },
                        "isUserLoggedIn": False,
                        "currency": "VND",
                        "travellerType": "Couple",
                        "isAPSPeek": False,
                        "enableOpaqueChannel": False,
                        "isEnabledPartnerChannelSelection": None,
                        "sorting": {
                            "sortField": "Ranking",
                            "sortOrder": "Desc",
                            "sortParams": None,
                        },
                        "requiredBasis": "PRPN",
                        "requiredPrice": "Exclusive",
                        "suggestionLimit": 0,
                        "synchronous": False,
                        "supplierPullMetadataRequest": None,
                        "isRoomSuggestionRequested": False,
                        "isAPORequest": False,
                        "hasAPOFilter": False,
                    },
                    "searchContext": {
                        "userId": None,
                        "memberId": 0,
                        "locale": "vi-vn",
                        "cid": -1,
                        "origin": "VN",
                        "platform": 1,
                        "deviceTypeId": 1,
                        "experiments": {
                            "forceByVariant": None,
                            "forceByExperiment": [
                                {"id": "UMRAH-B2B", "variant": "B"},
                                {"id": "UMRAH-B2C-REGIONAL", "variant": "B"},
                                {"id": "UMRAH-B2C", "variant": "Z"},
                                {"id": "JGCW-204", "variant": "B"},
                                {"id": "JGCW-264", "variant": "B"},
                                {"id": "JGCW-202", "variant": "B"},
                                {"id": "JGCW-299", "variant": "B"},
                                {"id": "FD-3936", "variant": "B"},
                            ],
                        },
                        "isRetry": False,
                        "showCMS": False,
                        "storeFrontId": 3,
                        "pageTypeId": 103,
                        "whiteLabelKey": None,
                        "ipAddress": "103.186.155.74",
                        "endpointSearchType": "CitySearch",
                        "trackSteps": None,
                        "searchId": "f64cc016-8d41-4a6a-b32e-cfb10dac18ce",
                    },
                    "matrix": None,
                    "matrixGroup": [
                        {"matrixGroup": "NumberOfBedrooms", "size": 100},
                        {"matrixGroup": "LandmarkIds", "size": 10},
                        {"matrixGroup": "AllGuestReviewBreakdown", "size": 100},
                        {"matrixGroup": "GroupedBedTypes", "size": 100},
                        {"matrixGroup": "RoomBenefits", "size": 100},
                        {"matrixGroup": "AtmosphereIds", "size": 100},
                        {"matrixGroup": "RoomAmenities", "size": 100},
                        {"matrixGroup": "AffordableCategory", "size": 100},
                        {"matrixGroup": "HotelFacilities", "size": 100},
                        {"matrixGroup": "BeachAccessTypeIds", "size": 100},
                        {"matrixGroup": "StarRating", "size": 20},
                        {"matrixGroup": "MetroSubwayStationLandmarkIds", "size": 20},
                        {"matrixGroup": "CityCenterDistance", "size": 100},
                        {"matrixGroup": "ProductType", "size": 100},
                        {"matrixGroup": "BusStationLandmarkIds", "size": 20},
                        {"matrixGroup": "IsSustainableTravel", "size": 2},
                        {"matrixGroup": "ReviewLocationScore", "size": 3},
                        {"matrixGroup": "LandmarkSubTypeCategoryIds", "size": 20},
                        {"matrixGroup": "ReviewScore", "size": 100},
                        {"matrixGroup": "AccommodationType", "size": 100},
                        {"matrixGroup": "PaymentOptions", "size": 100},
                        {"matrixGroup": "TrainStationLandmarkIds", "size": 20},
                        {"matrixGroup": "HotelAreaId", "size": 100},
                        {"matrixGroup": "HotelChainId", "size": 10},
                        {"matrixGroup": "RecommendedByDestinationCity", "size": 10},
                        {"matrixGroup": "Deals", "size": 100},
                    ],
                    "filterRequest": {
                        "idsFilters": [],
                        "rangeFilters": [],
                        "textFilters": [],
                    },
                    "page": {"pageSize": 45, "pageNumber": 1, "pageToken": ""},
                    "apoRequest": {"apoPageSize": 10},
                    "searchHistory": None,
                    "searchDetailRequest": {"priceHistogramBins": 50},
                    "isTrimmedResponseRequested": False,
                    "featuredAgodaHomesRequest": None,
                    "featuredLuxuryHotelsRequest": None,
                    "highlyRatedAgodaHomesRequest": {
                        "numberOfAgodaHomes": 30,
                        "minimumReviewScore": 7.5,
                        "minimumReviewCount": 3,
                        "accommodationTypes": [
                            28,
                            29,
                            30,
                            102,
                            103,
                            106,
                            107,
                            108,
                            109,
                            110,
                            114,
                            115,
                            120,
                            131,
                        ],
                        "sortVersion": 0,
                    },
                    "extraAgodaHomesRequest": None,
                    "extraHotels": {
                        "extraHotelIds": [],
                        "enableFiltersForExtraHotels": False,
                    },
                    "packaging": None,
                    "flexibleSearchRequest": {
                        "fromDate": "2023-02-02",
                        "toDate": "2023-03-13",
                        "alternativeDateSize": 4,
                        "isFullFlexibleDateSearch": False,
                    },
                    "rankingRequest": {
                        "isNhaKeywordSearch": False,
                        "isPulseRankingBoost": False,
                    },
                    "rocketmilesRequestV2": None,
                },
            },
            "ContentSummaryRequest": {
                "context": {
                    "rawUserId": "438e57fa-92fa-4e7a-a3f7-a1eaaec7b2ad",
                    "memberId": 0,
                    "userOrigin": "VN",
                    "locale": "vi-vn",
                    "forceExperimentsByIdNew": [
                        {"key": "UMRAH-B2B", "value": "B"},
                        {"key": "UMRAH-B2C-REGIONAL", "value": "B"},
                        {"key": "UMRAH-B2C", "value": "Z"},
                        {"key": "JGCW-204", "value": "B"},
                        {"key": "JGCW-264", "value": "B"},
                        {"key": "JGCW-202", "value": "B"},
                        {"key": "JGCW-299", "value": "B"},
                        {"key": "FD-3936", "value": "B"},
                    ],
                    "apo": False,
                    "searchCriteria": {"cityId": 15932},
                    "platform": {"id": 1},
                    "storeFrontId": 3,
                    "cid": "-1",
                    "occupancy": {
                        "numberOfAdults": 1,
                        "numberOfChildren": 0,
                        "travelerType": 0,
                        "checkIn": "2023-02-11T08:51:11.614Z",
                    },
                    "deviceTypeId": 1,
                    "whiteLabelKey": "",
                    "correlationId": "",
                },
                "summary": {
                    "highlightedFeaturesOrderPriority": None,
                    "description": False,
                    "includeHotelCharacter": True,
                },
                "reviews": {
                    "commentary": None,
                    "demographics": {
                        "providerIds": None,
                        "filter": {"defaultProviderOnly": True},
                    },
                    "summaries": {
                        "providerIds": None,
                        "apo": True,
                        "limit": 1,
                        "travellerType": 0,
                    },
                    "cumulative": {"providerIds": None},
                    "filters": None,
                },
                "images": {
                    "page": None,
                    "maxWidth": 0,
                    "maxHeight": 0,
                    "imageSizes": None,
                    "indexOffset": None,
                },
                "rooms": {
                    "images": None,
                    "featureLimit": 0,
                    "filterCriteria": None,
                    "includeMissing": False,
                    "includeSoldOut": False,
                    "includeDmcRoomId": False,
                    "soldOutRoomCriteria": None,
                    "showRoomSize": True,
                    "showRoomFacilities": True,
                    "showRoomName": False,
                },
                "nonHotelAccommodation": True,
                "engagement": True,
                "highlights": {
                    "maxNumberOfItems": 0,
                    "images": {
                        "imageSizes": [
                            {"key": "full", "size": {"width": 0, "height": 0}}
                        ]
                    },
                },
                "personalizedInformation": False,
                "localInformation": {"images": None},
                "features": None,
                "rateCategories": True,
                "contentRateCategories": {"escapeRateCategories": {}},
                "synopsis": True,
            },
            "PricingSummaryRequest": {
                "cheapestOnly": True,
                "context": {
                    "isAllowBookOnRequest": True,
                    "abTests": [
                        {"testId": 9021, "abUser": "B"},
                        {"testId": 9023, "abUser": "B"},
                        {"testId": 9024, "abUser": "B"},
                        {"testId": 9025, "abUser": "B"},
                        {"testId": 9027, "abUser": "B"},
                        {"testId": 9029, "abUser": "B"},
                    ],
                    "clientInfo": {
                        "cid": -1,
                        "languageId": 24,
                        "languageUse": 1,
                        "origin": "VN",
                        "platform": 1,
                        "searchId": "f64cc016-8d41-4a6a-b32e-cfb10dac18ce",
                        "storefront": 3,
                        "userId": "438e57fa-92fa-4e7a-a3f7-a1eaaec7b2ad",
                        "ipAddress": "103.186.155.74",
                    },
                    "experiment": [
                        {"name": "UMRAH-B2B", "variant": "B"},
                        {"name": "UMRAH-B2C-REGIONAL", "variant": "B"},
                        {"name": "UMRAH-B2C", "variant": "Z"},
                        {"name": "JGCW-204", "variant": "B"},
                        {"name": "JGCW-264", "variant": "B"},
                        {"name": "JGCW-202", "variant": "B"},
                        {"name": "JGCW-299", "variant": "B"},
                        {"name": "FD-3936", "variant": "B"},
                    ],
                    "isDebug": False,
                    "sessionInfo": {"isLogin": False, "memberId": 0, "sessionId": 1},
                    "packaging": None,
                },
                "isSSR": True,
                "roomSortingStrategy": None,
                "pricing": {
                    "bookingDate": "2023-02-02T08:51:13.929Z",
                    "checkIn": "2023-02-11T08:51:11.614Z",
                    "checkout": "2023-02-12T08:51:11.614Z",
                    "localCheckInDate": "2023-02-11",
                    "localCheckoutDate": "2023-02-12",
                    "currency": "VND",
                    "details": {
                        "cheapestPriceOnly": False,
                        "itemBreakdown": False,
                        "priceBreakdown": False,
                    },
                    "featureFlag": [
                        "ClientDiscount",
                        "PriceHistory",
                        "VipPlatinum",
                        "RatePlanPromosCumulative",
                        "PromosCumulative",
                        "CouponSellEx",
                        "MixAndSave",
                        "APSPeek",
                        "StackChannelDiscount",
                        "AutoApplyPromos",
                        "EnableAgencySupplyForPackages",
                        "EnableCashback",
                        "CreditCardPromotionPeek",
                        "EnableCofundedCashback",
                        "DispatchGoLocalForInternational",
                        "EnableGoToTravelCampaign",
                    ],
                    "features": {
                        "crossOutRate": False,
                        "isAPSPeek": False,
                        "isAllOcc": False,
                        "isApsEnabled": False,
                        "isIncludeUsdAndLocalCurrency": False,
                        "isMSE": True,
                        "isRPM2Included": True,
                        "maxSuggestions": 0,
                        "isEnableSupplierFinancialInfo": False,
                        "isLoggingAuctionData": False,
                        "newRateModel": False,
                        "overrideOccupancy": False,
                        "filterCheapestRoomEscapesPackage": False,
                        "priusId": 0,
                        "synchronous": False,
                        "enableRichContentOffer": True,
                        "showCouponAmountInUserCurrency": False,
                        "disableEscapesPackage": False,
                        "enablePushDayUseRates": False,
                        "enableDayUseCor": False,
                    },
                    "filters": {
                        "cheapestRoomFilters": [],
                        "filterAPO": False,
                        "ratePlans": [1],
                        "secretDealOnly": False,
                        "suppliers": [],
                        "nosOfBedrooms": [],
                    },
                    "includedPriceInfo": False,
                    "occupancy": {
                        "adults": 1,
                        "children": 0,
                        "childAges": [],
                        "rooms": 1,
                        "childrenTypes": [],
                    },
                    "supplierPullMetadata": {"requiredPrecheckAccuracyLevel": 0},
                    "mseHotelIds": [],
                    "ppLandingHotelIds": [],
                    "searchedHotelIds": [],
                    "paymentId": -1,
                    "externalLoyaltyRequest": None,
                },
                "suggestedPrice": "Exclusive",
            },
            "PriceStreamMetaLabRequest": {"attributesId": [8, 1, 18, 7, 11, 2, 3]},
        },
        "query": "query citySearch($CitySearchRequest: CitySearchRequest!, $ContentSummaryRequest: ContentSummaryRequest!, $PricingSummaryRequest: PricingRequestParameters, $PriceStreamMetaLabRequest: PriceStreamMetaLabRequest) {\n  citySearch(CitySearchRequest: $CitySearchRequest) {\n    searchResult {\n      sortMatrix {\n        result {\n          fieldId\n          sorting {\n            sortField\n            sortOrder\n            sortParams {\n              id\n            }\n          }\n          display {\n            name\n          }\n          childMatrix {\n            fieldId\n            sorting {\n              sortField\n              sortOrder\n              sortParams {\n                id\n              }\n            }\n            display {\n              name\n            }\n            childMatrix {\n              fieldId\n              sorting {\n                sortField\n                sortOrder\n                sortParams {\n                  id\n                }\n              }\n              display {\n                name\n              }\n            }\n          }\n        }\n      }\n      searchInfo {\n        flexibleSearch {\n          currentDate {\n            checkIn\n            price\n          }\n          alternativeDates {\n            checkIn\n            price\n          }\n        }\n        hasSecretDeal\n        isComplete\n        totalFilteredHotels\n        hasEscapesPackage\n        searchStatus {\n          searchCriteria {\n            checkIn\n          }\n          searchStatus\n        }\n        objectInfo {\n          objectName\n          cityName\n          cityEnglishName\n          countryId\n          countryEnglishName\n          mapLatitude\n          mapLongitude\n          mapZoomLevel\n          wlPreferredCityName\n          wlPreferredCountryName\n          cityId\n          cityCenterPolygon {\n            geoPoints {\n              lon\n              lat\n            }\n            touristAreaCenterPoint {\n              lon\n              lat\n            }\n          }\n        }\n      }\n      urgencyDetail {\n        urgencyScore\n      }\n      histogram {\n        bins {\n          numOfElements\n          upperBound {\n            perNightPerRoom\n            perPax\n          }\n        }\n      }\n      nhaProbability\n    }\n    properties(ContentSummaryRequest: $ContentSummaryRequest, PricingSummaryRequest: $PricingSummaryRequest, PriceStreamMetaLabRequest: $PriceStreamMetaLabRequest) {\n      propertyId\n      sponsoredDetail {\n        sponsoredType\n        trackingData\n        isShowSponsoredFlag\n      }\n      propertyResultType\n      content {\n        informationSummary {\n          hotelCharacter {\n            hotelTag {\n              name\n              symbol\n            }\n            hotelView {\n              name\n              symbol\n            }\n          }\n          propertyLinks {\n            propertyPage\n          }\n          atmospheres {\n            id\n            name\n          }\n          isSustainableTravel\n          localeName\n          defaultName\n          displayName\n          accommodationType\n          awardYear\n          hasHostExperience\n          address {\n            countryCode\n            country {\n              id\n              name\n            }\n            city {\n              id\n              name\n            }\n            area {\n              id\n              name\n            }\n          }\n          propertyType\n          rating\n          agodaGuaranteeProgram\n          remarks {\n            renovationInfo {\n              renovationType\n              year\n            }\n          }\n          spokenLanguages {\n            id\n          }\n          geoInfo {\n            latitude\n            longitude\n          }\n        }\n        propertyEngagement {\n          lastBooking\n          peopleLooking\n        }\n        nonHotelAccommodation {\n          masterRooms {\n            noOfBathrooms\n            noOfBedrooms\n            noOfBeds\n            roomSizeSqm\n            highlightedFacilities\n          }\n          hostLevel {\n            id\n            name\n          }\n          supportedLongStay\n        }\n        facilities {\n          id\n        }\n        images {\n          hotelImages {\n            id\n            caption\n            providerId\n            urls {\n              key\n              value\n            }\n          }\n        }\n        reviews {\n          contentReview {\n            isDefault\n            providerId\n            demographics {\n              groups {\n                id\n                grades {\n                  id\n                  score\n                }\n              }\n            }\n            summaries {\n              recommendationScores {\n                recommendationScore\n              }\n              snippets {\n                countryId\n                countryCode\n                countryName\n                date\n                demographicId\n                demographicName\n                reviewer\n                reviewRating\n                snippet\n              }\n            }\n            cumulative {\n              reviewCount\n              score\n            }\n          }\n          cumulative {\n            reviewCount\n            score\n          }\n        }\n        familyFeatures {\n          hasChildrenFreePolicy\n          isFamilyRoom\n          hasMoreThanOneBedroom\n          isInterConnectingRoom\n          isInfantCottageAvailable\n          hasKidsPool\n          hasKidsClub\n        }\n        personalizedInformation {\n          childrenFreePolicy {\n            fromAge\n            toAge\n          }\n        }\n        localInformation {\n          landmarks {\n            transportation {\n              landmarkName\n              distanceInM\n            }\n            topLandmark {\n              landmarkName\n              distanceInM\n            }\n            beach {\n              landmarkName\n              distanceInM\n            }\n          }\n          hasAirportTransfer\n        }\n        highlight {\n          cityCenter {\n            distanceFromCityCenter\n          }\n          favoriteFeatures {\n            features {\n              id\n              title\n              category\n            }\n          }\n          hasNearbyPublicTransportation\n        }\n        rateCategories {\n          escapeRateCategories {\n            rateCategoryId\n            localizedRateCategoryName\n          }\n        }\n      }\n      soldOut {\n        soldOutPrice {\n          averagePrice\n        }\n      }\n      pricing {\n        pulseCampaignMetadata {\n          promotionTypeId\n          webCampaignId\n          campaignTypeId\n          campaignBadgeText\n          campaignBadgeDescText\n          dealExpiryTime\n          showPulseMerchandise\n        }\n        isAvailable\n        isReady\n        benefits\n        cheapestRoomOffer {\n          agodaCash {\n            showBadge\n            giftcardGuid\n            dayToEarn\n            earnId\n            percentage\n            expiryDay\n          }\n          cashback {\n            cashbackGuid\n            showPostCashbackPrice\n            cashbackVersion\n            percentage\n            earnId\n            dayToEarn\n            expiryDay\n            cashbackType\n            appliedCampaignName\n          }\n        }\n        isEasyCancel\n        isInsiderDeal\n        isMultiHotelEligible\n        suggestPriceType {\n          suggestPrice\n        }\n        roomBundle {\n          bundleId\n          bundleType\n          saveAmount {\n            perNight {\n              ...Frag9ji2cf8feje46j9b8f8d\n            }\n          }\n        }\n        pointmax {\n          channelId\n          point\n        }\n        priceChange {\n          changePercentage\n          searchDate\n        }\n        payment {\n          cancellation {\n            cancellationType\n            freeCancellationDate\n          }\n          payLater {\n            isEligible\n          }\n          payAtHotel {\n            isEligible\n          }\n          noCreditCard {\n            isEligible\n          }\n          taxReceipt {\n            isEligible\n          }\n        }\n        cheapestStayPackageRatePlans {\n          stayPackageType\n          ratePlanId\n        }\n        pricingMessages {\n          location\n          ids\n        }\n        suppliersSummaries {\n          id\n          supplierHotelId\n        }\n        supplierInfo {\n          id\n          name\n          isAgodaBand\n        }\n        offers {\n          roomOffers {\n            room {\n              extraPriceInfo {\n                displayPriceWithSurchargesPRPN\n                corDisplayPriceWithSurchargesPRPN\n              }\n              availableRooms\n              isPromoEligible\n              promotions {\n                typeId\n                promotionDiscount {\n                  value\n                }\n                isRatePlanAsPromotion\n                cmsTypeId\n                description\n              }\n              bookingDuration {\n                unit\n                value\n              }\n              supplierId\n              corSummary {\n                hasCor\n                corType\n                isOriginal\n                hasOwnCOR\n                isBlacklistedCor\n              }\n              localVoucher {\n                currencyCode\n                amount\n              }\n              packaging {\n                token {\n                  clientToken\n                  interSystemToken\n                }\n                products {\n                  refId\n                  info {\n                    type\n                    offerType\n                    identifier {\n                      key\n                      value\n                    }\n                  }\n                  pricingItems {\n                    currency\n                    display {\n                      perPax {\n                        type\n                        allInclusive {\n                          chargeTotal\n                          specialPriceAndSaving {\n                            targetPrice\n                            saving {\n                              amount\n                            }\n                          }\n                          crossedOut\n                        }\n                        exclusive {\n                          chargeTotal\n                          specialPriceAndSaving {\n                            targetPrice\n                            saving {\n                              amount\n                            }\n                          }\n                          crossedOut\n                        }\n                      }\n                      perBook {\n                        type\n                        allInclusive {\n                          chargeTotal\n                          specialPriceAndSaving {\n                            targetPrice\n                            saving {\n                              amount\n                            }\n                          }\n                          crossedOut\n                        }\n                        exclusive {\n                          chargeTotal\n                          specialPriceAndSaving {\n                            targetPrice\n                            saving {\n                              amount\n                            }\n                          }\n                          crossedOut\n                        }\n                      }\n                      perRoomPerNight {\n                        allInclusive {\n                          chargeTotal\n                          specialPriceAndSaving {\n                            targetPrice\n                            saving {\n                              amount\n                            }\n                          }\n                          crossedOut\n                        }\n                        exclusive {\n                          chargeTotal\n                          specialPriceAndSaving {\n                            targetPrice\n                            saving {\n                              amount\n                            }\n                          }\n                          crossedOut\n                        }\n                      }\n                    }\n                  }\n                }\n                pricing {\n                  display {\n                    perBook {\n                      total {\n                        allInclusive {\n                          specialPriceAndSaving {\n                            targetPrice\n                            saving {\n                              amount\n                            }\n                          }\n                          crossedOut\n                          channelSaving {\n                            amount\n                          }\n                          totalSaving {\n                            amount\n                          }\n                          original\n                          chargeTotal\n                        }\n                        exclusive {\n                          specialPriceAndSaving {\n                            targetPrice\n                            saving {\n                              amount\n                            }\n                          }\n                          crossedOut\n                          channelSaving {\n                            amount\n                          }\n                          totalSaving {\n                            amount\n                          }\n                          original\n                          chargeTotal\n                        }\n                      }\n                      differential {\n                        allInclusive {\n                          chargeTotal\n                        }\n                        exclusive {\n                          chargeTotal\n                        }\n                      }\n                    }\n                    perPax {\n                      total {\n                        allInclusive {\n                          crossedOut\n                          channelSaving {\n                            amount\n                          }\n                          totalSaving {\n                            amount\n                          }\n                          original\n                          chargeTotal\n                        }\n                        exclusive {\n                          crossedOut\n                          channelSaving {\n                            amount\n                          }\n                          totalSaving {\n                            amount\n                          }\n                          original\n                          chargeTotal\n                        }\n                      }\n                      differential {\n                        allInclusive {\n                          chargeTotal\n                        }\n                        exclusive {\n                          chargeTotal\n                        }\n                      }\n                    }\n                  }\n                }\n              }\n              pricing {\n                currency\n                price {\n                  perNight {\n                    exclusive {\n                      display\n                      cashbackPrice\n                      displayAfterCashback\n                      originalPrice\n                    }\n                    inclusive {\n                      display\n                      cashbackPrice\n                      displayAfterCashback\n                      originalPrice\n                    }\n                  }\n                  perBook {\n                    exclusive {\n                      display\n                      cashbackPrice\n                      displayAfterCashback\n                      rebatePrice\n                      originalPrice\n                      autoAppliedPromoDiscount\n                    }\n                    inclusive {\n                      display\n                      cashbackPrice\n                      displayAfterCashback\n                      rebatePrice\n                      originalPrice\n                      autoAppliedPromoDiscount\n                    }\n                  }\n                  perRoomPerNight {\n                    exclusive {\n                      display\n                      crossedOutPrice\n                      cashbackPrice\n                      displayAfterCashback\n                      rebatePrice\n                      pseudoCouponPrice\n                      originalPrice\n                    }\n                    inclusive {\n                      display\n                      crossedOutPrice\n                      cashbackPrice\n                      displayAfterCashback\n                      rebatePrice\n                      pseudoCouponPrice\n                      originalPrice\n                    }\n                  }\n                  totalDiscount\n                  priceAfterAppliedAgodaCash {\n                    perBook {\n                      ...Fragfeg44dc89db72c8hh141\n                    }\n                    perRoomPerNight {\n                      ...Fragfeg44dc89db72c8hh141\n                    }\n                  }\n                }\n                apsPeek {\n                  perRoomPerNight {\n                    ...Frag9ji2cf8feje46j9b8f8d\n                  }\n                }\n                promotionPricePeek {\n                  display {\n                    perBook {\n                      ...Frag9ji2cf8feje46j9b8f8d\n                    }\n                    perRoomPerNight {\n                      ...Frag9ji2cf8feje46j9b8f8d\n                    }\n                    perNight {\n                      ...Frag9ji2cf8feje46j9b8f8d\n                    }\n                  }\n                  discountType\n                  promotionCodeType\n                  promotionCode\n                  promoAppliedOnFinalPrice\n                  childPromotions {\n                    campaignId\n                  }\n                  campaignName\n                }\n                channelDiscountSummary {\n                  channelDiscountBreakdown {\n                    display\n                    discountPercent\n                    channelId\n                  }\n                }\n                packagePriceAndSaving {\n                  perPax {\n                    allInclusive {\n                      specialPriceAndSaving {\n                        baseChannel\n                        targetChannel\n                        targetPrice\n                        saving {\n                          amount\n                        }\n                      }\n                    }\n                  }\n                }\n                promotionsCumulative {\n                  promotionCumulativeType\n                  amountPercentage\n                  minNightsStay\n                }\n              }\n              uid\n              payment {\n                paymentModel\n                cancellation {\n                  cancellationType\n                }\n              }\n              discount {\n                deals\n                channelDiscount\n              }\n              saveUpTo {\n                perRoomPerNight\n              }\n              benefits {\n                id\n                targetType\n              }\n              channel {\n                id\n              }\n              mseRoomSummaries {\n                supplierId\n                subSupplierId\n                pricingSummaries {\n                  currency\n                  channelDiscountSummary {\n                    channelDiscountBreakdown {\n                      channelId\n                      discountPercent\n                      display\n                    }\n                  }\n                  price {\n                    perRoomPerNight {\n                      exclusive {\n                        display\n                      }\n                      inclusive {\n                        display\n                      }\n                    }\n                  }\n                }\n              }\n              cashback {\n                cashbackGuid\n                showPostCashbackPrice\n                cashbackVersion\n                percentage\n                earnId\n                dayToEarn\n                expiryDay\n                cashbackType\n                appliedCampaignName\n              }\n              agodaCash {\n                showBadge\n                giftcardGuid\n                dayToEarn\n                expiryDay\n                percentage\n              }\n              corInfo {\n                corInfo {\n                  corType\n                }\n              }\n              loyaltyDisplay {\n                items\n              }\n              capacity {\n                extraBedsAvailable\n              }\n              pricingMessages {\n                formatted {\n                  location\n                  texts {\n                    index\n                    text\n                  }\n                }\n              }\n              campaign {\n                selected {\n                  messages {\n                    campaignName\n                    title\n                    titleWithDiscount\n                    description\n                    linkOutText\n                    url\n                  }\n                }\n              }\n              isPackageEligible\n              stayPackageType\n            }\n          }\n        }\n      }\n      metaLab {\n        attributes {\n          attributeId\n          dataType\n          value\n          version\n        }\n      }\n      enrichment {\n        topSellingPoint {\n          tspType\n          value\n        }\n        pricingBadges {\n          badges\n        }\n        uniqueSellingPoint {\n          rank\n          segment\n          uspType\n          uspPropertyType\n        }\n        bookingHistory {\n          bookingCount {\n            count\n            timeFrame\n          }\n        }\n        showReviewSnippet\n        isPopular\n        roomInformation {\n          cheapestRoomSizeSqm\n          facilities {\n            id\n            propertyFacilityName\n            symbol\n          }\n        }\n      }\n    }\n    searchEnrichment {\n      suppliersInformation {\n        supplierId\n        supplierName\n        isAgodaBand\n      }\n      pageToken\n    }\n    aggregation {\n      matrixGroupResults {\n        matrixGroup\n        matrixItemResults {\n          id\n          name\n          count\n          filterKey\n          filterRequestType\n          extraDataResults {\n            text\n            matrixExtraDataType\n          }\n        }\n      }\n    }\n  }\n}\n\nfragment Fragfeg44dc89db72c8hh141 on DisplayPrice {\n  exclusive\n  allInclusive\n}\n\nfragment Frag9ji2cf8feje46j9b8f8d on DFDisplayPrice {\n  exclusive\n  allInclusive\n}\n",
    }
    async with session.request("POST", url, json=payload, headers=headers) as response:
        x = await response.json()
        return {
            "id": province_ID,
            "name": name,
            "total": x["data"]["citySearch"]["searchResult"]["searchInfo"][
                "totalFilteredHotels"
            ],
        }


async def fetch_all(session: aiohttp.ClientSession) -> list[asyncio.Task]:
    tasks = []
    file = json.load(open("province_ID.json", encoding="utf-8"))
    for object in file:
        province = object["id"]
        name = object["name"]
        tasks.append(asyncio.create_task(get_data(session, province, name)))
    res = await asyncio.gather(*tasks)
    return res


async def main():
    async with aiohttp.ClientSession() as session:
        res = await fetch_all(session)
    with open("data.json", "w", encoding="utf-8") as outfile:
        json.dump(res, outfile, indent=4, ensure_ascii=False)


def main_function():
    start = time.time()
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main())
    print(f"Done in {time.time() - start} seconds")


if __name__ == "__main__":
    today_time = datetime.date.today()
    oneweek_later = today_time + datetime.timedelta(days=7)
    main_function()
