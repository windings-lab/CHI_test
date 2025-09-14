from src.data.pipeline import DataPipeline


def main():
    pipeline = DataPipeline()
    pipeline.acquire()

if __name__ == "__main__":
    main()
