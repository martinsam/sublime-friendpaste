# -*- coding: utf-8 -*-
import json
import os

FRIENDPASTE_URL = "https://friendpaste.com"


class SendPaste():
    """ data = "{'title': paste_name,
                'snippet': code,
                'language': python}"
    """
    def __init__(self, url=FRIENDPASTE_URL, data=""):
        self._url = FRIENDPASTE_URL
        self._data = data

    def send_paste(self):
        """ Send to FRIENDPASTE - Return url """
        if self._data:
            command = ("curl -XPOST %(url)s -d '%(data)s' " \
                " -H 'Content-Type: application/json' -k") % \
            {"url": FRIENDPASTE_URL, "data": self._data}
            resp = os.popen(command).read()
            resp = json.loads(resp)
            return resp
        return None
