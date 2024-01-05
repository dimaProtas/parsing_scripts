import json
import re

text = '"params":{"path":{"username":"dima_protasevich92"},"query":{"count":12}}},"preloadEnabledOnInit":false,"preloadEnabledOnNav":false},"profile_extras":{"expose":false,"preloaderID":"6668528089317598444","request":{"method":"GET","url":"\/graphql\/query\/","params":{"query":{"query_id":"9957820854288654","user_id":"27694502184","include_chaining":false,"include_reel":true,"include_suggested_users":false,"include_logged_out_extras":false,"include_live_status":false,"include_highlight_reels":true}}},"preloadEnabledOnInit":false,"preloadEnabledOnNav":false}}'


username = 'dima_protasevich92'


def id_user(text, username):
    Uid = re.search(f'{{"user_id":"(\\d+)","username":"{username}"}}', text).group()
    return json.loads(Uid).get('id', username)


# result = id_user(text, username)
# if result:
#     user_id = json.loads(result).get('id')
#     print(user_id)
# else:
#     print(f"User with username '{username}' not found.")


match = re.search(f'"user_id":"(\\d+)"', text)

if match:
    user_id = match.group(1)
    print(f"User ID for {username}: {user_id}")
else:
    print(f"User with username '{username}' not found.")

# print(id_user(text, username))