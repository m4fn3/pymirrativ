import json.decoder


class Response(object):
    def __init__(self, resp, parse=True):
        self.raw = {}
        self.resp = resp
        if resp.status_code == 200:
            if parse:
                try:
                    self.raw = resp.json()
                    if not self.raw["status"]["ok"]:
                        raise RuntimeError(f"Mirrativ Error: error code {self.raw['status']['error_code']}\n{self.raw['status']['error']}")
                except json.decoder.JSONDecodeError:
                    raise RuntimeError("Internal Error: Failed to parse the result as json")
        else:
            detail = ""
            if not resp.text.startswith("<!DOCTYPE html>"):
                detail += resp.text
            raise RuntimeError(f"Request Error: Failed with status code {resp.status_code}\n{detail}")

    def __getattr__(self, name):
        if name in self.raw:
            return self.raw.get(name)
        else:
            return None
