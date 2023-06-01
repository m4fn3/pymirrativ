# pymirrativ
An unofficial api wrapper of internal mirrativ api

## Installation
`pip install git+https://github.com/m4fn3/pymirrativ.git`

## Quick Example
```python
from pymirrativ import Mirrativ
client = Mirrativ()
client.login("<ENTER TOKEN HERE>")
print(client.me().raw)
```

## Docs
For available methods, see `client.py`.

Objects returned by functions is Response (in utils)
- `Response.raw` : raw json data returned by the api
- `Response.resp` : raw response object of requests module

Also, you can access values of json with attribute-style access. 
e.g.) `Response.user_id` (same as `Response.raw["user_id"]`)

## Api Details
### Token
You can get your token by following steps:
1. log-in to your account on https://mirrativ.com
2. open developer tools and see http requests to mirrativ.com/api
3. get the value of mr_id in cookies of request headers
### Account Grade
Some actions require a certain grade of the user.
If you are not logged in, it will be -1 by default.
Here are functions that will affect your grade:
- `me()` : a grade will be 0 by calling this function if you are not logged in
- `create_account()` : a grade will be 1
- `login()` : a grade will be whatever a value your account has
