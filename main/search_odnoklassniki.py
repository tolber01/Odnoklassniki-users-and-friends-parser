from multiprocessing import Pool
from functools import partial
from odnoklassniki import Odnoklassniki, OdnoklassnikiError


def get_query_info():
    """Function reads query information by keyboard enter by user: text of
    query, date of the birth: day, month, year.

    :return: text (str), day (str), month (str), year (str)
    """
    text = input(
        "Enter your text query (the name and the last name) here: "
    )
    print("Now input the date of the birth")
    try:
        day = int(input("Day: "))
    except ValueError:
        day = 0

    try:
        month = int(input("Month: "))
    except ValueError:
        month = 0

    try:
        year = int(input("Year: "))
    except ValueError:
        year = 0

    return text, day, month, year


def get_filters_parameter(day, month, year):
    """Function gets birthday info (day, month, year) as arguments and
    returns filters parameter in string format.

    :param day: the day of the birth
    :type day: int
    :param month: the month of the birth
    :type month: int
    :param year: the year of the birth
    :type year: int
    :return: filters_string (str)
    """
    filters = [{"type": "user"}]
    filters[0].update({
        key: value for key, value in zip(
            ("birthDay", "birthMonth", "birthYear"),
            (day, month, year)
        ) if value
    })
    filters_string = str(filters).replace("'", '"')

    return filters_string


def get_fields_parameter(fields_names):
    """Function gets fields_names sequence and returns fields
    parameter in string format.

    :param fields_names: sequence of result fields in response
    :type fields_names: tuple
    :return: fields_string (str)
    """
    fields_string = ", ".join(
        ["user." + field.lower() for field in fields_names]
    )

    return fields_string


def work_with_user(any_user, client, secret, token, fields):
    """Procedure works with user object, add to this object user's
    friends objects as list, print finally processed user object.

    :param any_user: user object with information from response
    :type any_user: dict
    :param client: client odnoklassniki application key
    :type client: str
    :param secret: secret odnoklassniki application key
    :type secret: str
    :param token: odnoklassniki application access token
    :type token: str
    :param fields: using fields of response parameter
    :type fields: str
    :return: None
    """
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
    CLIENT_KEY = r""
    SECRET_KEY = r""
    ACCESS_TOKEN = r""
    # Enter your app's serial data here.

    FIELDS_OF_RESULTS = (
        "AGE",
        "BIRTHDAY",
        "FIRST_NAME",
        "LAST_NAME",
        "LOCATION",
        "PIC640X480",
        "UID",
        "URL_PROFILE"
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
    print(filters_parameter)

    fields_parameter = get_fields_parameter(FIELDS_OF_RESULTS)

    ok_object = Odnoklassniki(
        CLIENT_KEY,
        SECRET_KEY,
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

    p.map(
        partial(
            work_with_user,
            client=CLIENT_KEY,
            secret=SECRET_KEY,
            token=ACCESS_TOKEN,
            fields=fields_parameter
        ),
        users_objects_list
    )

    p.close()
    p.join()
