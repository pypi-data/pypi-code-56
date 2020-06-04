import asyncio

import uvicorn
from aiocronjob.webapp.api import app
from aiocronjob.manager import manager


async def first_task():
    for i in range(20):
        print("first task log", i)
        await asyncio.sleep(10)


async def second_task():
    print("second task started")
    for i in range(5):
        await asyncio.sleep(2)
        print("from second task")
    raise Exception("second task exception")


manager.register(
    async_callable=first_task, name="First task", crontab="23 * * * *"
)

manager.register(
    async_callable=second_task, name="Second task", crontab="23 * * * *"
)


async def handle_exception(job_name: str, exc: Exception):
    print(f"An exception occurred for job {job_name}: {exc}")


async def handle_cancellation(job_name: str):
    print(f"{job_name} is cancelled...fuck")


async def on_shutdown():
    print("All services stopped.")


async def on_startup():
    print("The machine started.")


manager.set_on_job_cancelled_callback(handle_cancellation)
manager.set_on_job_exception_callback(handle_exception)
manager.set_on_shutdown_callback(on_shutdown)
manager.set_on_startup_callback(on_startup)


if __name__ == "__main__":
    uvicorn.run(app=app, host="0.0.0.0", port=5000, log_level="info")
