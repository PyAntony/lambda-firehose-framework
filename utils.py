import json
import base64
import uuid
import time
from functools import reduce
from main import modifyPayload, filterLogic


def updateDict(d, key, new_val):
    '''
    Update dictionary key with new value. Add key-value
    pair if it doesn't exist
    '''
    new_d = d.copy()
    new_d[key] = new_val
    return new_d


def decodeFromBase64(payload):
    '''
    Decode payloads from base64 and convert to python object using the
    json module.
    '''
    return json.loads(base64.b64decode(payload).decode('utf-8'))


def encodeToBase64(payload):
    '''
    Encode payload to base64 and then decode to unicode (utf-8).
    '''
    return base64.b64encode(json.dumps(payload).encode('utf-8')).decode('utf-8')


def getRecordsAndDecodePayload(event):
    '''
    Decode payloads from event records. Return the list of records.
    Record format in list -> event["records"]:
    {
        "recordId": Id_number
        "approximateArrivalTimestamp": timestamp
        # payload is encoded in base64
        "data": "eyJuYW1lIjlsgftFwDLygcog=="
    }
    '''
    return [
        updateDict(record, 'data', decodeFromBase64(record['data']))
        for record in event['records']
    ]


def transformRecord(record):
    '''Wrapper to update payload in record.'''
    return updateDict(record, 'data', modifyPayload(record['data']))


def filterRecord(record):
    '''
    Wrapper to add 'status' key to record to indicate Firehose
    we are dropping it.
    '''
    return updateDict(record, 'status',
                      'Dropped' if filterLogic(record['data']) else 'Ok')


def prepareRecord(record):
    '''Prepare record with Firehose requiered keys.'''
    return {
        'recordId': record['recordId'],
        'result': record['status'],
        'data': encodeToBase64(record['data'])
    }


def pipelineEachFunction(records, functions):
    '''
    Apply reduce to each record by passing them trough a pipeline
    of functions.
    '''
    return list(reduce(lambda record, func: map(func, record),
                       functions,
                       records)
           )


def getFirehoseEvent():
    '''Read Firehose event schema from a local file.'''
    with open('test_files/FirehoseFormat.txt', 'r') as file:
        return json.loads(file.read())


def getJsonSamples(fname):
    '''Read json samples from local file.'''
    with open(f'test_files/input/{fname}', 'r') as file:
        return [json.loads(line, encoding='UTF-8') for line in
                file.read().strip().split('\n')]


def prepareSampleRecords(dicts):
    '''Encode each json sample to base64.'''
    def prepareSample(dc):

        return {'recordId': str(uuid.uuid4()),
                'approximateArrivalTimestamp': time.time(),
                'data': encodeToBase64(dc)
               }

    return [prepareSample(dc) for dc in dicts]


def decodeOutputPayloads(output):
    '''
    Return output object with all payloads in records decoded
    from base64.
    '''
    newRecords = (
        updateDict(dc, 'data', decodeFromBase64(dc['data']))
        for dc in output['records']
    )

    return updateDict(output, 'records', list(newRecords))


def saveOutputJson(output, fname='sampleOutput.json'):
    '''Save json object to local file.'''
    with open(f'test_files/{fname}', 'w') as ofile:
        json.dump(output, ofile)
