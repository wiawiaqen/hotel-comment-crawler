import os
import pandas as pd
import json


def main():
    path = os.listdir("./Data")
    for i in range(len(path)):
        local_dir = f"./Data/{path[i]}"
        province = path[i].split("/")[-1]
        files = os.listdir(local_dir)
        reviewer_name = []
        reviewer_country = []
        review_date = []
        stay_length = []
        rating = []
        rating_text = []
        review_title = []
        review_comments = []
        review_positive_comments = []
        review_negative_comments = []
        review_province = []
        group_name = []
        type_name = []
        print(files)
        for file in files:
            try:
                with open(f"./Data/{province}/{file}", "r", encoding="utf-8") as f:
                    data = json.load(f)
                    for object in data:
                        reviewer_name.append(object["reviewer_name"])
                        reviewer_country.append(object["reviewer_country"])
                        review_date.append(object["review_date"])
                        stay_length.append(object["stay_length"])
                        rating.append(object["rating"])
                        rating_text.append(object["rating_text"])
                        review_title.append(object["review_title"])
                        review_comments.append(object["review_comments"])
                        review_positive_comments.append(
                            object["review_positive_comments"]
                        )
                        review_negative_comments.append(
                            object["review_negative_comments"]
                        )
                        group_name.append(object["groupName"])
                        type_name.append(object["typeName"])
                        review_province.append(province)
            except Exception as e:
                print(e)
        data = {
            "reviewer_name": reviewer_name,
            "reviewer_country": reviewer_country,
            "review_date": review_date,
            "stay_length": stay_length,
            "rating": rating,
            "rating_text": rating_text,
            "review_title": review_title,
            "review_comments": review_comments,
            "review_positive_comments": review_positive_comments,
            "review_negative_comments": review_negative_comments,
            "group_name": group_name,
            "type_name": type_name,
            "province": province,
        }
        df = pd.DataFrame(data)
        df.to_excel(
            f"./grouped/Agoda_{province}.xlsx",
            index=False,
            engine="xlsxwriter",
        )


if __name__ == "__main__":
    if not os.path.exists("./grouped"):
        os.makedirs("./grouped")
    main()
