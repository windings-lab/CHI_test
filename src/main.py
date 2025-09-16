from src.data.pipeline import DataPipeline

def main():
    cities = ["Kyiv", "London", "New York", "Paris", "Rome", "Seoul", "Tokyo"]
    pipeline = DataPipeline()

    for city in cities:
        raw_data = pipeline.acquire(city)
        data_frame = pipeline.process(raw_data)
        pipeline.save_to_database(data_frame)

    pipeline.analyze()

if __name__ == "__main__":
    main()
