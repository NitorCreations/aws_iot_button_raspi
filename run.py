import time
import os
import json
import awsiotclient as iot
import countdown

thingState = {}


def handleShadowGet(payload, responseStatus, token):
    print("get")
    print(payload)
    global thingState
    jp = json.loads(payload)
    thingState = jp
    state = jp.get('state')
    if state:
        desired = state.get('desired')
        if desired:
            updateShadow(desired.get('pushedAt') * 1000,
                         desired.get('intervalSeconds') * 1000,
                         desired.get('pusher'))


def handleShadowDelta(payload, responseStatus, token):
    # payload is a JSON string ready to be parsed using json.loads(...)
    # in both Py2.x and Py3.x
    global thingState
    print("printing thingstate")
    print(thingState)
    print("end printing thignstate")
    print(responseStatus)
    jp = json.loads(payload)
    print("delta: " + str(payload))
    pushedAt, intervalMillis, pusher = None, None, None
    if jp.get('state') and jp['state'].get('pusher'):
        pusher = jp['state']['pusher']
    if jp.get('state') and jp['state'].get('intervalSeconds'):
        intervalMillis = jp['state']['intervalSeconds'] * 1000
    if jp.get('state') and jp['state'].get('pushedAt'):
        pushedAt = jp['state']['pushedAt'] * 1000
    if not pushedAt:
        return
    if not intervalMillis:
        print(thingState)
        intervalMillis = \
            thingState['state']['reported']['intervalSeconds'] * 1000
    if not pusher:
        if thingState['state']['reported']['pusher']:
            pusher = thingState['state']['reported']['pusher']
        else:
            pusher = "Unknown"
    updateShadow(pushedAt, intervalMillis, pusher)
    countdown.init(pushedAt, intervalMillis)


def handleShadowUpdate(payload, responseStatus, token):
    # payload is a JSON string ready to be parsed using json.loads(...)
    # in both Py2.x and Py3.x
    if responseStatus == "timeout":
        print("Update request " + token + " time out!")
    if responseStatus == "accepted":
        print("Update request with token: " + token + " accepted!")
        print(payload)
    if responseStatus == "rejected":
        print("Update request " + token + " rejected!")
        print(payload)
        print(responseStatus)


def updateShadow(pushedAtMillis, durationMillis, pusher=None):
    global thingState
    if not pushedAtMillis:
        return
    pusher = pusher if pusher else clientId
    durationMillis = durationMillis if durationMillis else 60000
    JSONState = {"state": {
                "reported": {
                    "pushedAt": int(round(pushedAtMillis/1000, 0)),
                    "pusher": pusher,
                    "intervalSeconds": int(round(durationMillis/1000, 0))
                    },
                "desired": None
                }}
    thingState['state'] = JSONState['state']
    deviceShadowHandler.shadowUpdate(
        json.dumps(JSONState), handleShadowUpdate, 5)


clientId = os.environ['IOT_CLIENT_ID_PREFIX'] + os.environ['RESIN_DEVICE_UUID']
awsIotClient = iot.getClient(
    os.environ['IOT_HOST'],
    os.environ['AWS_ROOT_CA_PATH'],
    os.environ['PRIVATE_KEY_PATH'],
    os.environ['CERTIFICATE_PATH'],
    clientId)

awsIotClient.connect()

# Create a deviceShadow with persistent subscription
deviceShadowHandler = awsIotClient.createShadowHandlerWithName(
    os.environ['THING_NAME'], True)

deviceShadowHandler.shadowGet(handleShadowGet, 5)

# Listen on deltas
deviceShadowHandler.shadowRegisterDeltaCallback(handleShadowDelta)

countdown.duration = int(os.environ['COUNTDOWN_LENGTH'])
countdown.push_callback = updateShadow

if os.environ.get('TEST_RUN'):
    countdown.init(countdown.millis(), countdown.duration)


while True:
    time.sleep(countdown.tick())
