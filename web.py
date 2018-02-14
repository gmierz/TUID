# encoding: utf-8
#
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.
from __future__ import absolute_import
from __future__ import division
from __future__ import unicode_literals

import requests
import json
class Web:
    @staticmethod
    def get(url):
        response = requests.get(url)
        return json.loads(response.text)

    @staticmethod
    def get_string(url):
        return requests.get(url)
