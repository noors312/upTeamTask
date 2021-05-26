import asyncio
import time

import aiohttp
import boto3


def get_template_as_string():
    with open('sqs-config.yaml') as f:
        data = f.read()
    return data


async def invoke_lambda():
    lambdaClient = boto3.client('lambda')
    await lambdaClient.invoke_async(
        FunctionName='pythonLambda'
    )


async def main():
    cloudformationClient = boto3.client('cloudformation')
    cloudformation_response = cloudformationClient.create_stack(
        StackName='sqs-lambda-stack',
        TemplateBody=get_template_as_string(),
        OnFailure='DELETE',
        TimeoutInMinutes=5,
        Capabilities=['CAPABILITY_NAMED_IAM']
    )
    time.sleep(30)
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


if __name__ == "__main__":
    asyncio.run(main())
