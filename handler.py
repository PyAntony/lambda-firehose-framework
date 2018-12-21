from utils import *


def lambda_handler(event, context):

    output = pipelineEachFunction(
                # get list of records with payloads decoded
                getRecordsAndDecodePayload(event),
                # list of functions
                [transformRecord,
                 filterRecord,
                 prepareRecord]
             )

    return {'records': output}
