import asyncio
import concurrent.futures
from dataclasses import dataclass

from temporalio import activity
from temporalio.client import Client
from temporalio.worker import Worker
from proto.service_pb2 import HelloRequest, HelloResponse


@dataclass
class ComposeGreetingInput:
    greeting: str
    name: str


@activity.defn(name="print_prto")
async def print_prto(hello_req: HelloRequest) -> HelloResponse:
    activity.logger.info("Running activity with parameter %s" % input)
    hello_res: HelloResponse = HelloResponse(
        message=f"Hello, {hello_req.name}!"
    )
    return hello_res


async def main():
    client = await Client.connect("localhost:7233")

    with concurrent.futures.ThreadPoolExecutor(max_workers=100) as activity_executor:
        worker_instance = Worker(
            client,
            task_queue='protobug',
            workflows=[],
            activities=[print_prto],
            activity_executor=activity_executor,
            debug_mode=True,
        )
        await worker_instance.run()


if __name__ == "__main__":
    asyncio.run(main())