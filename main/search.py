from odnoklassniki import Odnoklassniki


def get_query_info():
    """Function reads query information by keyboard enter by user: text of
    query, date of the birth: day, month, year.

    :return: text (str), day (int), month (int), year (int)
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


def print_users(users_list):
    """Procedure prints each user of the users_list.

    :param users_list: list containing users dicts
    :type users_list: list
    :return: None
    """
    for user in users_list:
        print({
            "id": user["uid"],
            "name": user["first_name"],
            "last_name": user["last_name"],
            "birthday": user["birthday"],
            "city": user["location"]["city"]
        })


if __name__ == "__main__":
    CLIENT_KEY: str = r""
    SECRET_KEY: str = r""
    ACCESS_TOKEN: str = r""
    # Enter your app's serial data here.

    FIELDS_OF_RESULTS: tuple = (
        "BIRTHDAY",
        "FIRST_NAME",
        "LAST_NAME",
        "LOCATION",
        "UID",
    )
    # You can find another fields here:
    # https://apiok.ru/dev/types/data.UserInfoField
    MAX_NUMBER_OF_RESULTS: int = 100
    TYPE_OF_RESULTS: str = "USER"

    text_query, day_of_birth, month_of_birth, year_of_birth = get_query_info()

    filters_parameter = get_filters_parameter(
        day_of_birth,
        month_of_birth,
        year_of_birth
    )
    fields_parameter = get_fields_parameter(FIELDS_OF_RESULTS)

    ok_object = Odnoklassniki(
        CLIENT_KEY,
        SECRET_KEY,
        ACCESS_TOKEN
    )

    has_more_users = True
    first_iteration = True
    users_objects_list = []
    anchor_parameter = ""

    while has_more_users:
        response_object = ok_object.search.quick(
            query=text_query,
            types=TYPE_OF_RESULTS,
            fields=fields_parameter,
            filters=filters_parameter,
            anchor=anchor_parameter,
            count=MAX_NUMBER_OF_RESULTS
        )
        try:
            if first_iteration:
                print("Found users:", response_object["totalCount"])
                first_iteration = not first_iteration

            users_objects_list = response_object["entities"]["users"]
            has_more_users = response_object["has_more"]
            anchor_parameter = response_object["anchor"]
        except KeyError:
            break
        else:
            print_users(users_objects_list)
