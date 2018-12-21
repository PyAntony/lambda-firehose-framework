import sys
import json
from handler import *


def modifyPayload(payload):
    '''Transform and return payload.'''
    #payload = **YOUR TRANSFORMATION HERE**

    #print(payload) -> add a print statement if you want to
    #review the payload before/after modification in CloudWatch logs.

    return payload


def filterLogic(payload, drop_record=False):
    '''Drop record if logic returns True.'''
    #drop_record = **YOUR LOGIC HERE** (must return a boolean)

    return drop_record


def test_lambda():
    '''
    Read json file, apply transformation, and print and save
    output without encoding payload back to base64.
    '''
    try:
        fname = sys.argv[1]
    except:
        print("Handler test mode. Usage: "
         "'python3 main.py <sample json file name>'")
        return

    myEvent = updateDict(getFirehoseEvent(), 'records',
                         prepareSampleRecords(getJsonSamples(fname))
              )

    output = decodeOutputPayloads(lambda_handler(myEvent, ''))

    saveOutputJson(output)
    print(json.dumps(output, indent=3, sort_keys=True))


if __name__ == '__main__':
    test_lambda()
