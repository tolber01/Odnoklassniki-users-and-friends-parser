from multiprocessing import Pool
from functools import partial
from odnoklassniki import Odnoklassniki, OdnoklassnikiError


def get_query_info():
    text = input(
        "Enter your text query (the name and the last name) here: "
    )
    print("Now input the date of the birth")
    day = input("Day: ")
    month = input("Month: ")
    year = input("Year: ")

    return text, day, month, year


def get_filters_parameter(day, month, year):
    filters = {
        key: value for key, value in zip(
            ("birthDay", "birthMonth", "birthYear"),
            (day, month, year)
        ) if value
    }
    filters["type"] = "user"
    filters = str([filters]).replace("'", '"')

    return filters


def get_fields_parameter(fields_names):
    return ", ".join(["user." + field for field in fields_names])


def work_with_user(any_user, client, secret, token, fields):
    ok = Odnoklassniki(
        client,
        secret,
        token
    )

    any_user["friends"] = []

    try:
        user_friends_ids = ok.friends.get(fid=any_user["uid"])
    except OdnoklassnikiError:
        user_friends_ids = []
    finally:
        if user_friends_ids:
            if len(user_friends_ids) > 100:
                while len(user_friends_ids) > 100:
                    friends = ok.users.getInfo(
                        uids=", ".join(user_friends_ids[0:100]),
                        fields=fields
                    )
                    any_user["friends"] += friends

                    user_friends_ids = user_friends_ids[100:]
            else:
                friends = ok.users.getInfo(
                    uids=", ".join(user_friends_ids[0:100]),
                    fields=fields
                )
                any_user["friends"] += friends

        print(any_user)

if __name__ == "__main__":
    CLIENT = r""
    SECRET = r""
    ACCESS_TOKEN = r""
    # Enter your app's serial data here.

    FIELDS_OF_RESULTS = (
        "NAME",
        "BIRTHDAY",
        "AGE",
        "CITY_OF_BIRTH",
        "UID",
        "URL_PROFILE",
        "PIC640X480"
    )
    # You can find another fields here:
    # https://apiok.ru/dev/types/data.UserInfoField
    MAX_NUMBER_OF_RESULTS = 100

    text_query, day_of_birth, month_of_birth, year_of_birth = get_query_info()

    filters_parameter = get_filters_parameter(
        day_of_birth,
        month_of_birth,
        year_of_birth
    )

    fields_parameter = get_fields_parameter(FIELDS_OF_RESULTS)

    ok_object = Odnoklassniki(
        CLIENT,
        SECRET,
        ACCESS_TOKEN
    )

    has_more_users = True
    users_objects_list = []
    anchor_parameter = ""

    while has_more_users:
        response_object = ok_object.search.quick(
            query=text_query,
            types="USER",
            fields=fields_parameter,
            filters=filters_parameter,
            anchor=anchor_parameter,
            count=MAX_NUMBER_OF_RESULTS
        )
        try:
            users_objects_list.extend(response_object["entities"]["users"])
            has_more_users = response_object["has_more"]
            anchor_parameter = response_object["anchor"]
        except KeyError:
            break
    print("Users found:", len(users_objects_list))

    p = Pool(20)

    results = p.map(
        partial(
            work_with_user,
            client=CLIENT,
            secret=SECRET,
            token=ACCESS_TOKEN,
            fields=fields_parameter
        ),
        users_objects_list
    )

    p.close()
    p.join()
