from src.data.pipeline import DataPipeline


def main():
    pipeline = DataPipeline()
    raw_data = pipeline.acquire()
    data_frame = pipeline.process(raw_data)
    pipeline.save_to_database(data_frame)

if __name__ == "__main__":
    main()
