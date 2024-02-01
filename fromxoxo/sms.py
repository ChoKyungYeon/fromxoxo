import hmac, hashlib, base64
import time, requests, json
try:
    from fromxoxo.settings.local import SENS_ACCESS_KEY, SENS_SECRET_KEY, SENS_SERVICE_KEY
except:
    from fromxoxo.settings.deploy import SENS_ACCESS_KEY, SENS_SECRET_KEY, SENS_SERVICE_KEY

contact_phone = '01057325834'

SENS_ACCESS_KEY = SENS_ACCESS_KEY
SENS_SECRET_KEY = SENS_SECRET_KEY
SENS_SERVICE_KEY = SENS_SERVICE_KEY
url = "https://sens.apigw.ntruss.com"
uri = f"/sms/v2/services/{SENS_SERVICE_KEY}/messages"


def make_signature(SENS_SECRET_KEY, SENS_ACCESS_KEY, timestamp, uri):
    SENS_SECRET_KEY = bytes(SENS_SECRET_KEY, 'UTF-8')
    method = "POST"
    message = method + " " + uri + "\n" + timestamp + "\n" + SENS_ACCESS_KEY
    message = bytes(message, 'UTF-8')
    signingKey = base64.b64encode(hmac.new(SENS_SECRET_KEY, message, digestmod=hashlib.sha256).digest())
    return signingKey


def Send_SMS(to, contents):
    timestamp = str(int(time.time() * 1000))
    header = {
        "Content-Type": "application/json; charset=utf-8",
        "x-ncp-apigw-timestamp": timestamp,
        "x-ncp-iam-access-key": SENS_ACCESS_KEY,
        "x-ncp-apigw-signature-v2": make_signature(SENS_SECRET_KEY, SENS_ACCESS_KEY, timestamp, uri)
    }
    data = {
        "type": "SMS",
        "from": contact_phone,
        "content": '[From.XoXo]' + contents,
        "subject": "SENS",
        "messages": [
            {
                "to": to,
            }
        ]
    }
    try:
        response = requests.post(url + uri, headers=header, data=json.dumps(data))
    except:
        pass
