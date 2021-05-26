import asyncio

import boto3


def get_template_as_string():
    with open('sqs-config.yaml') as f:
        data = f.read()
    return data


async def invoke_lambda():
    lambdaClient = boto3.client('lambda')
    response = lambdaClient.invoke_async(
        FunctionName='pythonLambda',
        InvokeArgs=b'{"some_data":"some_data"}'
    )
    return response


async def main():
    cloudformationClient = boto3.client('cloudformation')
    cloudformation_response = cloudformationClient.create_stack(
        StackName='sqs-lambda-stack',
        TemplateBody=get_template_as_string(),
        OnFailure='DELETE',
        TimeoutInMinutes=5,
        Capabilities=['CAPABILITY_NAMED_IAM']
    )
    lambdaClient = boto3.client('lambda')
    while True:
        try:
            lambdaClient.get_function(
                FunctionName='pythonLambda'
            )
            responses = await asyncio.gather(
                invoke_lambda(),
                invoke_lambda(),
                invoke_lambda(),
                invoke_lambda(),
                invoke_lambda(),
                invoke_lambda(),
                invoke_lambda(),
                invoke_lambda(),
                invoke_lambda(),
            )
            print(responses)
            break
        except:
            print('No function')
            continue


if __name__ == "__main__":
    asyncio.run(main())
