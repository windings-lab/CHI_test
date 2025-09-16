from src.data.pipeline import DataPipeline


def main():
    pipeline = DataPipeline()
    raw_data = pipeline.acquire()
    data = pipeline.process(raw_data)

if __name__ == "__main__":
    main()
