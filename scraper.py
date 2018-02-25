from requests import get, post


class Scraper(object):
    template = "https://fewdmaterials.github.io/{}/EGGERS_CONTENTS.json"

    @staticmethod
    def setTemplate(template):
        Scraper.template = template

    @staticmethod
    def assemble(*args):
        return Scraper.template.format(*args)

    @staticmethod
    def run(url):
        r = get(url)
        return r.json()


class MyJSON(object):
    url_base = 'https://api.myjson.com'
    rehearsal_base = 'https://mottaquikarim.github.io/rehearsal/public/stage.html?source={}'

    @staticmethod
    def post(data):
        r = post("{}/bins".format(MyJSON.url_base), json={
            "d": data,
        }, headers={
            'Content-type': 'application/json',
            'Accept': 'text/plain'
        })
        ret = r.json()
        uri = ret.get('uri', None)

        if not uri:
            raise Exception('URI not found')

        jsonID = uri.split('/')

        return MyJSON.rehearsal_base.format(jsonID[-1])
