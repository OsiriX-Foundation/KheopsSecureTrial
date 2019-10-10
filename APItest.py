#!/usr/bin/env python
import requests
import sys

def getStatusCode(url, excepted, headers):
    response = requests.get(API + url, headers=headers)
    if response.status_code == excepted:
        return 0, response.status_code
    else:
        return 1, response.status_code

def postStatusCode(url, excepted, data, headers):
    response = requests.post(API + url, data=data, headers=headers)
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
    url="/secutrialtoken"
    nbError=0
    for value in valueGetToTest:
        res = getStatusCode(url, value['excepted'], value['headers'])
        manageResult(res, value)
        nbError+=res[0]

    for value in valuePostToTest:
        res = postStatusCode(url, value['excepted'], value['data'], value['headers'])
        manageResult(res, value)
        nbError+=res[0]
    return nbError

def main():
    nbError=test()
    if (nbError > 0):
        raise Exception('{} error occur in the test'.format(nbError))

if __name__ == "__main__":
    valueGetToTest = [
        { 'excepted': 400, 'message': 'Referer error, excepted status code', 'headers': {'referer': 'https://demo.kheops.online'} },
        { 'excepted': 405, 'message': 'Method Not Allowed, excepted status code', 'headers': {'referer': 'https://test.kheops.online/test'} }
    ]
    valuePostToTest = [
        { 'excepted': 400, 'message': 'No data given, excepted status code', 'data': {}, 'headers': {'referer': 'https://test.kheops.online'} },
        { 'excepted': 400, 'message': 'No referer header', 'data': {}, 'headers': {} },
        { 'excepted': 400, 'message': 'Missing secret, excepted status code', 'data': {'institution_name': 'geneve', 'institution_secret': '123456', 'grant_type': 'urn:x-kheops:params:oauth:grant-type:secutrial'}, 'headers': {'referer': 'https://test.kheops.online'} },
        { 'excepted': 400, 'message': 'Missing institution_name, excepted status code', 'data': {'secret': '12345', 'institution_secret': '123456', 'grant_type': 'urn:x-kheops:params:oauth:grant-type:secutrial'}, 'headers': {'referer': 'https://test.kheops.online'} },
        { 'excepted': 400, 'message': 'Missing institution_secret, excepted status code', 'data': {'secret': '12345', 'institution_name': 'geneve', 'grant_type': 'urn:x-kheops:params:oauth:grant-type:secutrial'}, 'headers': {'referer': 'https://test.kheops.online'} },
        { 'excepted': 400, 'message': 'Not good grant type, excepted status code', 'data': {'secret': '12345', 'institution_name': 'geneve', 'institution_secret': '1234567'}, 'headers': {'referer': 'https://test.kheops.online'} },
        { 'excepted': 400, 'message': 'Secret with a S', 'data': {'secrets': '12345', 'institution_name': 'geneve', 'institution_secret': '123456', 'grant_type': 'urn:x-kheops:params:oauth:grant-type:secutrial'}, 'headers': {'referer': 'https://test.kheops.online'} },
        { 'excepted': 400, 'message': 'institution_name without _', 'data': {'secret': '12345', 'institutionname': 'geneve', 'institution_secret': '123456', 'grant_type': 'urn:x-kheops:params:oauth:grant-type:secutrial'}, 'headers': {'referer': 'https://test.kheops.online'} },
        { 'excepted': 400, 'message': 'Not good secret, excepted status code', 'data': {'secret': '123456', 'institution_name': 'geneve', 'institution_secret': '123456', 'grant_type': 'urn:x-kheops:params:oauth:grant-type:secutrial'}, 'headers': {'referer': 'https://test.kheops.online'} },
        { 'excepted': 400, 'message': 'Not good institution name, excepted status code', 'data': {'secret': '12345', 'institution_name': 'tijuana', 'institution_secret': '123456', 'grant_type': 'urn:x-kheops:params:oauth:grant-type:secutrial'}, 'headers': {'referer': 'https://test.kheops.online'} },
        { 'excepted': 400, 'message': 'Not good institution secret, excepted status code', 'data': {'secret': '12345', 'institution_name': 'geneve', 'institution_secret': '1234567', 'grant_type': 'urn:x-kheops:params:oauth:grant-type:secutrial'}, 'headers': {'referer': 'https://test.kheops.online'} },
        { 'excepted': 400, 'message': 'Not good grant type, excepted status code', 'data': {'secret': '12345', 'institution_name': 'geneve', 'institution_secret': '1234567', 'grant_type': 'urn:x-kheops:params:oauth:grant-type:secutriall'}, 'headers': {'referer': 'https://test.kheops.online'} },
        { 'excepted': 200, 'message': 'Good data given, excepted status code', 'data': {'secret': '12345', 'institution_name': 'geneve', 'institution_secret': '123456', 'grant_type': 'urn:x-kheops:params:oauth:grant-type:secutrial'}, 'headers': {'referer': 'https://test.kheops.online'} },
        { 'excepted': 200, 'message': 'Good data given (second secret), excepted status code', 'data': {'secret': '12345', 'institution_name': 'geneve', 'institution_secret': '654321', 'grant_type': 'urn:x-kheops:params:oauth:grant-type:secutrial'}, 'headers': {'referer': 'https://test.kheops.online'} },
        { 'excepted': 200, 'message': 'Good data given (Other institution), excepted status code', 'data': {'secret': '12345', 'institution_name': 'paris', 'institution_secret': '123456', 'grant_type': 'urn:x-kheops:params:oauth:grant-type:secutrial'}, 'headers': {'referer': 'https://test.kheops.online'} },
        { 'excepted': 200, 'message': 'Good data given (second secret), excepted status code', 'data': {'secret': '12345', 'institution_name': 'paris', 'institution_secret': '654321', 'grant_type': 'urn:x-kheops:params:oauth:grant-type:secutrial'}, 'headers': {'referer': 'https://test.kheops.online'} }
    ]
    API = "http://127.0.0.1:8080" if (len(sys.argv) == 1) else sys.argv[1]
    try:
        response = requests.get(API)
    except Exception as err:
        raise Exception('Can\'t access to {} \n{}'.format(API, err))
    else:
        main()
