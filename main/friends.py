from odnoklassniki import Odnoklassniki, OdnoklassnikiError


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


def print_friends(friends_list):
    for friend in friends_list:
        print({
            "id": friend["uid"],
            "name": friend["first_name"],
            "last_name": friend["last_name"],
            "birthday": friend["birthday"],
            "city": friend["location"]["city"]
        })


def work_with_friends_list(fields, ok):
    """Procedure gets and works with list of friends, prints each of them.

    :param fields: fields parameter for getInfo function
    :type fields: str
    :param ok: Odnoklassniki object of API wrapper
    :type ok: Odnoklassniki
    :return: None
    """
    friends = ok.users.getInfo(
        uids=", ".join(user_friends_ids[0:100]),
        fields=fields
    )
    print_friends(friends)


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

    fields_parameter = get_fields_parameter(FIELDS_OF_RESULTS)

    id_input = input("Enter user's id here: ")

    ok_object = Odnoklassniki(
        CLIENT_KEY,
        SECRET_KEY,
        ACCESS_TOKEN
    )

    try:
        user_friends_ids = ok_object.friends.get(fid=id_input)
    except OdnoklassnikiError:
        user_friends_ids = []
    finally:
        print(
            "Found",
            len(user_friends_ids),
            "friends"
        )
        if user_friends_ids:
            while len(user_friends_ids) > 100:
                work_with_friends_list(
                    fields_parameter,
                    ok_object
                )

                user_friends_ids = user_friends_ids[100:]
            else:
                work_with_friends_list(
                    fields_parameter,
                    ok_object
                )
