import time
import uuid
import secrets
import requests

from .config import Config
from .utils import Response


def check_grade(grade):
    def _check_grade(func):
        def wrapper(*args, **kwargs):
            if args[0].grade_id >= grade:
                return func(*args, **kwargs)
            else:
                raise RuntimeError(f"You need grade {grade} to use this function")

        return wrapper

    return _check_grade


class Mirrativ:
    def __init__(self):
        self.session = requests.Session()
        self.grade_id = -1
        self.session.headers.update({
            "user-agent": f"MR_APP/{Config.APP_VER}/{Config.OS}/{Config.MODEL}/{Config.OS_VER}",
            "x-ad": "",
            "x-unity-framework": Config.UNITY_VER,
            "x-network-status": "2",
            "x-os-push": "1",
            "x-client-unixtime": str(time.time()),
            "http_x_timezone": "Asia/Tokyo",
            "accept": "*/*",
            "accept-language": "ja-JP;q=1.0, en-JP;q=0.9",
            "x-adjust-adid": str(secrets.token_hex(16)),
            "x-adjust-idfa": "00000000-0000-0000-0000-000000000000",
            "x-idfv": str(uuid.uuid4()),
            "x-uuid": str(uuid.uuid4())
        })

    # --- Auth ---
    def login(self, token):
        self.session.cookies.update(requests.utils.cookiejar_from_dict({
            "mr_id": token,
            "f": str(uuid.uuid4()),
            "lang": "ja"
        }))
        me = self.me()
        print(f"Logged in as {me.name}({me.user_id})[{me.grade_id}]")
        self.grade_id = me.grade_id

    def create_account(self):
        self.me()  # -> grade 0
        data = {
            "name": "test",
            "include_urge_users": 1,
            "is_avatar_uploaded": 0
        }
        custom_header = {'x-referer': 'login'}
        res = self.session.post(f"{Config.BASE_URL}{Config.PROFILE_EDIT}", data=data, headers=custom_header, files={(None, None)})
        self.me()  # -> grade 1
        return Response(res)

    # --- User ---
    def me(self):
        res = self.session.get(f"{Config.BASE_URL}{Config.ME}")
        me = Response(res)
        self.grade_id = me.grade_id
        return me

    def get_user(self, user_id):
        params = {"user_id": user_id}
        res = self.session.get(f"{Config.BASE_URL}{Config.PROFILE}", params=params)
        return Response(res)

    # User actions
    @check_grade(1)
    def follow(self, user_id):
        data = {"user_id": user_id}
        custom_header = {"x-referer": "profile"}
        res = self.session.post(f"{Config.BASE_URL}{Config.FOLLOW}", data=data, headers=custom_header)
        return Response(res)

    @check_grade(1)
    def unfollow(self, user_id):
        data = {"user_id": user_id}
        custom_header = {"x-referer": "profile"}
        res = self.session.post(f"{Config.BASE_URL}{Config.UNFOLLOW}", data=data, headers=custom_header)
        return Response(res)

    @check_grade(1)
    def block(self, user_id):
        data = {"user_id": user_id}
        custom_header = {"x-referer": "profile"}
        res = self.session.post(f"{Config.BASE_URL}{Config.BLOCK}", data=data, headers=custom_header)
        return Response(res)

    @check_grade(1)
    def unblock(self, user_id):
        data = {"user_id": user_id}
        custom_header = {"x-referer": "profile"}
        res = self.session.post(f"{Config.BASE_URL}{Config.UNBLOCK}", data=data, headers=custom_header)
        return Response(res)

    @check_grade(0)
    def get_currency(self):
        res = self.session.get(f"{Config.BASE_URL}{Config.CURRENCY}")
        return Response(res)

    @check_grade(1)
    def get_user_apps(self, user_id):
        params = {"user_id": user_id}
        res = self.session.get(f"{Config.BASE_URL}{Config.USER_APPS}", params=params)
        return Response(res)

    @check_grade(0)
    def send_live_request(self, user_id, count):
        data = {
            "count": count,
            "user_id": user_id,
            "where": "live_view_end"
        }
        res = self.session.post(f"{Config.BASE_URL}{Config.LIVE_REQUEST}", data=data)
        return Response(res)

    # --- Live ---
    def get_live(self, live_id):
        params = {"live_id": live_id}
        res = self.session.get(f"{Config.BASE_URL}{Config.LIVE}", params=params)
        return Response(res)

    def get_lives_of_following(self):
        params = {"id": 1}
        res = self.session.get(f"{Config.BASE_URL}{Config.CATALOG}", params=params)
        return Response(res)

    def get_lives_of_recommended(self):
        params = {"id": 2}
        res = self.session.get(f"{Config.BASE_URL}{Config.CATALOG}", params=params)
        return Response(res)

    # Live actions
    def get_streaming_url(self, live_id):
        params = {"live_id": live_id}
        res = self.session.get(f"{Config.BASE_URL}{Config.STREAMING_URL}", params=params)
        return Response(res)

    def get_comments(self, live_id):
        params = {"live_id": live_id}
        res = self.session.get(f"{Config.BASE_URL}{Config.COMMENTS}", params=params)
        return Response(res)

    @check_grade(0)
    def send_comment(self, live_id, comment):
        data = {"live_id": live_id, "comment": comment, "type": 1}
        res = self.session.post(f"{Config.BASE_URL}{Config.COMMENT}", data=data)
        return Response(res)

    @check_grade(0)
    def send_join_message(self, live_id):
        data = {"live_id": live_id, "comment": "", "type": 3}
        res = self.session.post(f"{Config.BASE_URL}{Config.COMMENT}", data=data)
        return Response(res)

    def get_viewer(self, live_id, page=1):
        params = {"live_id": live_id, "page": page}
        res = self.session.get(f"{Config.BASE_URL}{Config.ONLINE_USERS}", params=params)
        return Response(res)

    def get_collaborators(self, live_id):
        params = {"live_id": live_id}
        res = self.session.get(f"{Config.BASE_URL}{Config.COLLAB_USERS}", params=params)
        return Response(res)

    def get_view_mission(self, live_id):
        params = {"live_id": live_id}
        res = self.session.get(f"{Config.BASE_URL}{Config.VIEW_MISSION}", params=params)
        return Response(res)

    def do_view_mission(self, live_id):
        data = {"live_id": live_id}
        res = self.session.post(f"{Config.BASE_URL}{Config.VIEW_MISSION}", data=data)
        return Response(res)

    def ping_live(self, live_id):
        data = {"live_id": live_id, "error_count": 0, "is_ui_hidden": 0, "live_user_key": "", "view_mission_combo": 0, "view_mission_status": 360, "viewer_receive_push_notification": 0}
        res = self.session.post(f"{Config.BASE_URL}{Config.LIVE_POLLING}", data=data)
        return Response(res)

    def leave_live(self, live_id):
        data = {"live_id": live_id}
        res = self.session.post(f"{Config.BASE_URL}{Config.LEAVE}", data=data)
        return Response(res)

    # --- Search ---
    @check_grade(0)
    def search(self, search_type, query, page=1):
        if search_type not in ["live", "user", "app"]:
            raise RuntimeError("Specify one of live, user and app for search_type")
        params = {"q": query, "page": page}
        res = self.session.get(f"{Config.BASE_URL}/{search_type}{Config.SEARCH}", params=params)
        return Response(res)

    # --- Ad ---
    def get_reward(self):
        data = {"reward_id": 2}
        custom_header = {
            'Accept-Encoding': 'gzip, deflate, br',
            "accept-language": "ja",
            'content-type': "application/x-www-form-urlencoded",
            'x-referer': 'home',
        }
        res = self.session.post(f"{Config.BASE_URL}{Config.REWARD_COMPLETE}", data=data, headers=custom_header)
        return Response(res)
