from odnoklassniki import Odnoklassniki


CLIENT = r""
SECRET = r""
ACCESS_TOKEN = r""
# Enter your app's serial data here.  

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
