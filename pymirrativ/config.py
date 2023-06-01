
class Config:
    # --- Client Settings ---
    OS = "iOS"
    OS_VER = "16.1.2"
    MODEL = "iPhone10,1"
    APP_VER = "10.16.0"
    UNITY_VER = "4.28.0"
    # --- Endpoints ---
    BASE_URL = "https://www.mirrativ.com/api"
    # Auth
    PROFILE_EDIT = "/user/profile_edit"
    # User
    ME = "/user/me"
    PROFILE = "/user/profile"
    FOLLOW = "/graph/follow"
    UNFOLLOW = "/graph/unfollow"
    BLOCK = "/graph/block"
    UNBLOCK = "/graph/unblock"
    LIVE_REQUEST = "/user/post_live_request"
    USER_APPS = "/user/user_apps"
    CURRENCY = "/user/currency"
    # Live
    LIVE = "/live/live"
    COMMENTS = "/live/live_comments"
    STREAMING_URL = "/live/get_streaming_url"
    CATALOG = "/live/catalog"
    LEAVE = "/live/leave"
    ONLINE_USERS = "live/online_users"
    # Search
    SEARCH = "/search"
    # Ad
    REWARD_COMPLETE = "/reward_ad/complete"

