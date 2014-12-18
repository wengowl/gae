#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file exc ept in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import webapp2
import youdao
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


class MainHandler(webapp2.RequestHandler):
    def get(self):

        self.response.out.write("""
        <html>
        <head>
        <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
         </head>
          <body>
          <title>有道翻译API调用测试</title>
          <h3>输入你要翻译的内容，目前支持其他语言到中文的翻译和中文到英文的翻译</h3>
          <form action="/fanyi" method="post">
            <div><textarea name="content" rows="3" cols="60"></textarea></div>
            <div><input type="submit" value="翻译"></div>
          </form>
        </body>
      </html>""")

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/fanyi', youdao.YouDao)
], debug=True)
