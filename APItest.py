#!/usr/bin/env python
import requests

def getStatusCode(url, excepted):
    response = requests.get(API + url)
    if response.status_code == excepted:
        return 0, response.status_code
    else:
        return 1, response.status_code

def postStatusCode(url, excepted, data):
    response = requests.post(API + url, data=data)
    if response.status_code == excepted:
        return 0, response.status_code
    else:
        return 1, response.status_code

def manageResult(res, value):
    if (res[0] == 0):
        print("[OK] - {} {}".format(value['message'], value['excepted']))
    else:
        print("[FAIL] - {} {}, received {}".format(value['message'], value['excepted'], res[1]))
    return ''

def test():
    result=""
    url="/secrettoken"
    nbError=0
    for value in valueGetToTest:
        res = getStatusCode(url, value['excepted'])
        manageResult(res, value)
        nbError+=res[0]

    for value in valuePostToTest:
        res = postStatusCode(url, value['excepted'], value['data'])
        manageResult(res, value)
        nbError+=res[0]
    return nbError

if __name__ == "__main__":
    API="http://127.0.0.1:8080"
    valueGetToTest = [
        { 'excepted': 405, 'message': 'Method Not Allowed, excepted status code' }
    ]
    valuePostToTest = [
        { 'excepted': 400, 'message': 'No data given, excepted status code', 'data': {} },
        { 'excepted': 400, 'message': 'Missing secret, excepted status code', 'data': {'institution_name': 'geneve', 'institution_secret': '123456'} },
        { 'excepted': 400, 'message': 'Missing institution_name, excepted status code', 'data': {'secret': '12345', 'institution_secret': '123456'} },
        { 'excepted': 400, 'message': 'Missing institution_secret, excepted status code', 'data': {'secret': '12345', 'institution_name': 'geneve'} },
        { 'excepted': 400, 'message': 'Secret with a S', 'data': {'secrets': '12345', 'institution_name': 'geneve', 'institution_secret': '123456'} },
        { 'excepted': 400, 'message': 'institution_name without _', 'data': {'secret': '12345', 'institutionname': 'geneve', 'institution_secret': '123456'} },
        { 'excepted': 401, 'message': 'Not good secret, excepted status code', 'data': {'secret': '123456', 'institution_name': 'geneve', 'institution_secret': '123456'} },
        { 'excepted': 401, 'message': 'Not good institution name, excepted status code', 'data': {'secret': '12345', 'institution_name': 'tijuana', 'institution_secret': '123456'} },
        { 'excepted': 401, 'message': 'Not good institution secret, excepted status code', 'data': {'secret': '12345', 'institution_name': 'geneve', 'institution_secret': '1234567'} },
        { 'excepted': 200, 'message': 'Good data given, excepted status code', 'data': {'secret': '12345', 'institution_name': 'geneve', 'institution_secret': '123456'} }
    ]
    nbError=test()
    print('')
    print('================================')
    print('{} error occur in the test'.format(nbError))
    print('================================')
