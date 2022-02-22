import json
import boto3
import base64
import os
import io
# Fill this in with the name of your deployed model
ENDPOINT = "image-classification-2022-02-22-17-35-22-482"
runtime = boto3.client('runtime.sagemaker')
def lambda_handler(event, context):
    # Decode the image data
    image = base64.b64decode(event["image_data"])
    # Instantiate a Predictor
    response = runtime.invoke_endpoint(EndpointName=ENDPOINT, ContentType="image/png", Body = image)
    # For this model the IdentitySerializer needs to be "image/png"
    # Make a prediction:
    inferences = response["Body"].read()
    # We return the data back to the Step Function
    event["inferences"] = inferences.decode('utf-8')
    return {
        'statusCode': 200,
        'body': json.dumps(event)
    }