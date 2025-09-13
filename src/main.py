import asyncio

from pipeline import Pipeline


async def main():
    pipeline = Pipeline()
    await pipeline.acquire()

if __name__ == "__main__":
    asyncio.run(main())
