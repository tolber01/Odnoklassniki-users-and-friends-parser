from odnoklassniki import Odnoklassniki


CLIENT = r"CBAKIBKMEBABABABA"
SECRET = r"08097B8BD95218A55BD5EF52"
ACCESS_TOKEN = \
    r"tkn1Inmu3moGvGUD6GWgPPq2zXKBEKtsZyF4YwC7Yc7DRvcl1NZ11fFIzzuIUvmeXs48P0"

ok_object = Odnoklassniki(
    CLIENT,
    SECRET,
    ACCESS_TOKEN
)

friends_ids_list = ok_object.friends.get(fid="573767567812")
print(friends_ids_list)

for user in ok_object.users.getInfo(uids=",".join(friends_ids_list),
                                    fields="NAME"):
    print(user)
