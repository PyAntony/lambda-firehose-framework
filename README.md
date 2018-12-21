# AWS Lambda-Firehose Framework

This framework helps to easily create and test AWS lambda functions that work with Kinesis Firehose events. You don’t need to spend time understanding the appropriate input or output formats or decoding/encoding from or to base64. Just implement 2 functions, 1 for payload transformation and 1 for record filtering. Your function is then ready to be shipped. 

## Overview

There are 3 modules:

- handler.py which contains the lambda handler (nothing to adjust here):
```python
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
```

- main.py where the user adds the code. There are 2 functions here to implement, 1 to modify the payload and 1 to filter the record according to logic:
```python
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
```
This module contains a third function that will be used in test mode.

- utils.py with all the utility functions.

**Test mode:** mode to review the output of the handler after your code has been inserted in the functions mentioned. It will print and save the output json file after transformation and filtering. 

## Instructions

- Clone this repository.

- Enter your custom code for transformation and filtering in the functions indicated (remember: filtering occurs after transformation).

- Zip the python modules and your lambda function is ready to be deployed using your favorite method.

**Test mode:**

- Clone this repository and enter your custom code for transformation and filtering.

- Insert a properly formatted json file with some sample records you are sending to you Firehose instance in the “test_files/input” directory.

- navigate to repository and run "python3 main.py \<sample json file name\>".

- the output records will the printed to screen and saved with name 'sampleOutput.json' in the “test_files” directory. Sample output:

![pic1](https://github.com/PyAntony/aws-lambda-firehose/blob/master/images/pic1.png)
 
## Additional Notes

- Note that the handler name to use is “handler.lambda_handler”.

- This framework was tested with Python 3.7 environment. Other environments are not guaranteed.

- If test mode throws json errors make sure the json file you are using is properly formatted: dictionary-like objects separated with new character “\n”, no commas in between, and no empty line at the end. There is a sample file (sample1.json) in the “test_files/input” directory.

- If you try to use the default event template sample (Amazon Kinesis Data Firehose) when testing using the AWS Lambda UI you will get an error (JSONDecodeError) . The reason is the payload used in the template: *'Hello, this is a test 123.'*. This is not in valid json format; hence, the json library can’t load it (json.loads(payload)). Just use the test mode provided. If you really want to test it using the UI you need to change the record payload (‘data’ key) with a proper json object encoded with base64 (function to encode is found in the “utils” module).

- Note that records indicated to be filtered are not actually filtered, they are only marked with the ‘Dropped’ keyword in the ‘result’ key. You will see them printed in the screen and in the 'sampleOutput.json'. For more information go to the documentation: https://docs.aws.amazon.com/firehose/latest/dev/data-transformation.html

## To Do

- [ ] Expand this Framework from Firehose-only format to custom formats by using different templates. 
