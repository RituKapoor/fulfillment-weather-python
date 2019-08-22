# -*- coding:utf8 -*-
# !/usr/bin/env python
# Copyright 2017 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""This is a sample for a weather fulfillment webhook for an Dialogflow agent
This is meant to be used with the sample weather agent for Dialogflow, located at
https://console.dialogflow.com/api-client/#/agent//prebuiltAgents/Weather

This sample uses the WWO Weather Forecast API and requires an WWO API key
Get a WWO API key here: https://developer.worldweatheronline.com/api/
"""

import json

from flask import Flask, request, make_response, jsonify

from forecast import Forecast, validate_params

app = Flask(__name__)
log = app.logger


@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)

    print("Request: Ritu")
    print(json.dumps(req, indent=4))

    res = processRequest(req)

    res = json.dumps(res, indent=4)
    print(res)
    r = make_response(jsonify({'fulfillmentText': res}))
    return r


def processRequest(req):

    try:
        action = req.get('queryResult').get('action')
    except AttributeError:
        return 'json error'

    print(action)

    if action == 'bot_register_user_demo':
        res = registerUser(req)
    else:
        log.error('Unexpected action.')

    #data = json.loads(result)

    return res


def registerUser(req):
    """Returns a string containing text with a response to the user
    with the weather forecast or a prompt for more information

    Takes the city for the forecast and (optional) dates
    uses the template responses found in weather_responses.py as templates
    """

    head = parameters = req['queryResult']['parameters']
    print(head)
    print('Dialogflow Parameters:')
    print(json.dumps(head, indent=4))

    # headers = {'phone': head.get('phone'),
    #             'name': head.get('name'),
    #             'email': head.get('email')
    #             }
    # print("****************************")
    # print(headers)
    # cal = submit_form_demo('bot_register_user_demo', headers)
    response = {
        "speech": "Please enter the OTP sent on your phone number.",
        "displayText": "Please enter the OTP sent on your phone number.",
        # "contextOut": [],
        "source": "apiai-webhook-sample"
    }

    return response


def submit_form_demo(action_name, headers):
    print("**************############**************")

    baseurl = "http://139.59.38.156/Api_new/"
    endurl = "?client_id=demobot&key=0a77716196b04d69b22792a119c3cdca"
    print(action_name)
    yql_url = baseurl + action_name
    print(yql_url)
    print(headers)
    headers['client_id'] = 'demobot'
    headers['key'] = '0a77716196b04d69b22792a119c3cdca'
    gcontext = ssl.SSLContext(ssl.PROTOCOL_TLSv1)  # Only for gangstars
    response = requests.get(yql_url, params=headers)
    print(response)
    return response


def verify_user_demo(action_name, code, phone):
    print("verify_user demo: ")
    baseurl = "http://139.59.38.156/Api_new/"
    endurl = "?client_id=demobot&key=0a77716196b04d69b22792a119c3cdca"

    yql_url = baseurl + action_name + endurl + \
        '&code=' + str(code) + '&phone=' + str(phone)
    print(yql_url)

    gcontext = ssl.SSLContext(ssl.PROTOCOL_TLSv1)  # Only for gangstars
    response = urllib.request.urlopen(yql_url, context=gcontext).read()
    print("verify_user result: ")
    print(response)

    return response.decode('utf-8')


def makeWebhookResult(text, data):
    quick_replies = []

    for reply in data:
        quick_replies.append(
            {
                "content_type": "text",
                "title": reply,
                "payload": reply
            })

    facebook_message = {
        "text": text,
        "quick_replies": quick_replies
    }

    print(json.dumps(facebook_message))
    print(data)

    return {
        "fulfillmentText": "",
        "payload": {"facebook": facebook_message, "fb": {"title": text, "replies": data}},
        # "contextOut": [],
        "source": "apiai-v2-webhook-sample"
    }


def show_university(headers, phone, email):
    url = 'http://139.59.9.205:8002/v1/search/new'
    gcontext = ssl.SSLContext(ssl.PROTOCOL_TLSv1)  # Only for gangstars
    # response = requests.get(url, headers=headers)
    #response = json.loads(requests.get(url)).get('results')
    # http://139.59.9.205:8002/v1/search/new?toefl=90&q=mechanical & auto&country=uk
    #headers['country'] = 'uk'
    #headers['q'] = 'mechanical and automation'
    #headers['toefl'] = '70'
    response = requests.get(url, params=headers).json().get('results')
    # print(url)
    # print(headers)
    # print(response)
    source = 'https://mu-assets.s3.amazonaws.com/new/brand/univ/'
    elements = []
    count = 0
    if(not response):
        return
    for i in response:
        if(count == 10):
            break

        image_url = i.get('course')[0].get('img')

        if(image_url == None):
            image_url = "full/MU_default.png"
        courses = []
        for course in i.get('course'):
            courses.append({
                'pk': course.get('pk'),
                'name': course.get('name'),
                'country': course.get('univ').get('code')
            })

        elements.append(
            {
                "title": i.get('university'),
                "image_url": source + image_url,
                "courses": courses,
                "count": i.get('count')
            })

        count = count + 1

    facebook_message = {
        "attachment": {
            "type": "template",
            "payload": {
                "template_type": "generic",
                "elements": elements
            }
        }
    }
    return {
        "speech": "",
        "displayText": "",
        "data": {"facebook": facebook_message, "fb": elements},
        # "contextOut": [],
        "source": "apiai-weather-webhook-sample"
    }


def send_email_to_lead(headers, phone, email):
    url = 'http://139.59.9.205:8002/v1/search/new'
    gcontext = ssl.SSLContext(ssl.PROTOCOL_TLSv1)  # Only for gangstars
    # response = requests.get(url, headers=headers)
    #response = json.loads(requests.get(url)).get('results')
    # http://139.59.9.205:8002/v1/search/new?toefl=90&q=mechanical & auto&country=uk
    #headers['country'] = 'uk'
    #headers['q'] = 'mechanical and automation'
    #headers['toefl'] = '70'
    response = requests.get(url, params=headers).json().get('results')
    # print(url)
    # print(headers)
    # print(response)
    source = 'https://mu-assets.s3.amazonaws.com/new/brand/univ/'
    elements = []
    count = 0
    if(not response):
        return
    for i in response:
        if(count == 10):
            break

        image_url = i.get('course')[0].get('img')

        if(image_url == None):
            image_url = "full/MU_default.png"
        courses = []
        for course in i.get('course'):
            courses.append({
                'pk': course.get('pk'),
                'name': course.get('name'),
                'country': course.get('univ').get('code')
            })

        elements.append(
            {
                "title": i.get('university'),
                "image_url": source + image_url,
                "courses": courses,
                "count": i.get('count')
            })

        count = count + 1

    facebook_message = {
        "attachment": {
            "type": "template",
            "payload": {
                "template_type": "generic",
                "elements": "mail_send"
            }
        }
    }
    #baseurl = "http://localhost:8888/mu-beta/index.php/Api_new/"
    baseurl = "https://app.meetuniversity.com/Api_new/"
    yql_url = baseurl + 'bot_email_prediction'
    print(yql_url)
    headers = {}
    headers['client_id'] = 'mubot'
    headers['key'] = '0a77716196b04d69b22792a119c3cdca'
    headers['phone'] = phone
    headers['email'] = email
    headers['data'] = str(json.dumps(elements, separators=(',', ':')))

    gcontext = ssl.SSLContext(ssl.PROTOCOL_TLSv1)  # Only for gangstars
    response = requests.get(yql_url, params=headers)
    print(response)
    return {
        "speech": "",
        "displayText": "",
        "data": {"facebook": facebook_message, "fb": "mail_send"},
        # "contextOut": [],
        "source": "apiai-weather-webhook-sample"
    }


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
