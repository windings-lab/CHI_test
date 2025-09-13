import asyncio

from data_pipeline import DataPipeline


async def main():
    pipeline = DataPipeline()
    await pipeline.acquire()

if __name__ == "__main__":
    asyncio.run(main())
