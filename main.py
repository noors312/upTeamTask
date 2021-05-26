import asyncio
import time

import aiohttp
import boto3


def get_template_as_string():
    with open('sqs-config.yaml') as f:
        data = f.read()
    return data


async def invoke_lambda():
    async with aiohttp.ClientSession() as session:
        response = await session.post(
            url='https://9u2x0vg65b.execute-api.us-west-1.amazonaws.com/default/',
            data={
                'some_data': 'some_data'
            }
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
    time.sleep(10)
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
