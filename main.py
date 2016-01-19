import urllib
import webapp2
import json
import cgi

'''
    Examples:
        curl "http://localhost:20080/?s=1&er=xdc&s=2"
        curl --data "s=1&er=xdc&s=2" http://localhost:20080/
        curl --form "fileupload=@1.txt" --form "x=saaa&fileupload=aaa" http://localhost:20080/
        curl -H 'Content-Type: application/json' -X PUT -d '{"tags":["tag1","tag2"],"question":"Which band?","answers":[{"id":"a0","answer":"Answer1"},{"id":"a1","answer":"answer2"}]}' http://localhost:20080/
        curl -X DELETE "http://localhost:20080/?s=1&er=xdc&s=2"
        curl -v -X HEAD "http://localhost:20080/?s=1&er=xdc&s=2"
'''

class InfoHandler(webapp2.RequestHandler):
    def base_info(self):
        rv = {
            #'User-Agent': self.request.headers['User-Agent'],
            #'Content-Type': self.request.headers['Content-Type'],
            'ip': self.request.remote_addr,
            'headers': dict(self.request.headers),
        }
        return rv

    def body_params(self, obj):
        ct = obj.get('Content-Type', '').lower()
        if ct.startswith('application/x-www-form-urlencoded') or ct.startswith('multipart/form-data'):
            prms = {}
            for arg in self.request.arguments():
                val = self.request.POST[arg]
                if isinstance(val, cgi.FieldStorage):
                    prms[arg] = { 
                        'content-type': val.type,
                        'name': val.filename,
                        'size': len(val.value),
                    }
                else:
                    prms[arg] = val
            obj['parameters'] = prms
        else:
            obj['body'] = self.request.body
        return obj

    def url_params(self, obj):
        prms = {}
        for arg in self.request.arguments():
            lst = self.request.get_all(arg)
            if len(lst) > 1:
                prms[arg] = lst
            elif len(lst) == 1:
                prms[arg] = lst[0]
            else:
                prms[arg] = '<error>'
        obj['parameters'] = prms
        return obj

    def get(self):
        self.response.headers['Content-Type'] = 'application/json'
        obj = self.base_info()
        obj['method'] = 'GET'
        obj = self.url_params(obj)
        if len(self.request.body):
            obj['body'] = self.request.body
        self.response.out.write(json.dumps(obj))

    def post(self):
        self.response.headers['Content-Type'] = 'application/json'
        obj = self.base_info()
        obj['method'] = 'POST'
        obj = self.body_params(obj)
        self.response.out.write(json.dumps(obj))

    def put(self):
        self.response.headers['Content-Type'] = 'application/json'
        obj = self.base_info()
        obj['method'] = 'PUT'
        obj = self.body_params(obj)
        self.response.out.write(json.dumps(obj))

    def delete(self):
        self.response.headers['Content-Type'] = 'application/json'
        obj = self.base_info()
        obj['method'] = 'DELETE'
        obj = self.url_params(obj)
        self.response.out.write(json.dumps(obj))

    def head(self):
        self.response.headers['Content-Type'] = 'application/json'
        #obj = self.base_info()
        #obj['method'] = 'HEAD'
        #obj = self.url_params(obj)
        #self.response.out.write(json.dumps(obj))
        self.response.clear()


app = webapp2.WSGIApplication(
            [
             ('/', InfoHandler),
            ], debug=False)
