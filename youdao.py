# -*- coding: UTF-8 -*-

import webapp2
import urllib2
import json


__author__ = 'wengxf'


class YouDao(webapp2.RequestHandler):
    def post(self):
        word = self.request.get("content")
        if word == '':
            self.response.write('<p>你要翻译的内容为空<p>')
            self.response.write('<a href="/">返回</a>')
            return
        if type(word).__name__ == "unicode":
            word = word.encode('UTF-8')
        result = self.youdao(word)
        self.response.write('<p>你要翻译的内容：'+word+'<p>')
        self.response.write('<p>\n翻译结果:'+result+'</p>')
        self.response.write('<a href="/">返回</a>')

    def youdao(self, word):
        qword = urllib2.quote(word)
        baseurl = r'http://fanyi.youdao.com/openapi.do?keyfrom=wengowl&key=1235066141&type=data&doctype=json&version=1.1' \
                  r'&q='
        url = baseurl + qword
        resp = urllib2.urlopen(url)
        fanyi = json.loads(resp.read())
        if fanyi['errorCode'] == 0:
            if 'basic' in fanyi.keys():
                trans = u'%s:\n%s\n%s\n网络释义：\n%s' % (
                    fanyi['query'], ''.join(fanyi['translation']), ' '.join(fanyi['basic']['explains']),
                    ''.join(fanyi['web'][0]['value']))
                return trans
            else:
                trans = u'%s:\n基本翻译:%s\n' % (fanyi['query'], ''.join(fanyi['translation']))
                return trans
        elif fanyi['errorCode'] == 20:
            return u'对不起，要翻译的文本过长'
        elif fanyi['errorCode'] == 30:
            return u'对不起，无法进行有效的翻译'
        elif fanyi['errorCode'] == 40:
            return u'对不起，不支持的语言类型'
        else:
            return u'对不起，您输入的单词%s无法翻译,请检查拼写' % word