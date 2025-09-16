from src.prefect_flow import weather_pipeline

def main():
    """
    Main entry point for the weather data pipeline.
    Uses Prefect for workflow orchestration.
    """
    # Run the Prefect flow
    cities = ["Kyiv", "London", "New York", "Paris", "Rome", "Seoul", "Tokyo"]
    result = weather_pipeline(cities)
    
    print("=" * 50)
    print("WEATHER PIPELINE EXECUTION SUMMARY")
    print("=" * 50)
    print(f"Cities processed: {len(result['cities_processed'])}")
    print(f"Total records: {result['total_records']}")
    print(f"Errors: {len(result['errors'])}")
    
    if result['cities_processed']:
        print(f"\nSuccessfully processed cities: {', '.join(result['cities_processed'])}")
    
    if result['errors']:
        print(f"\nErrors encountered:")
        for error in result['errors']:
            print(f"  - {error}")
    
    print("=" * 50)

if __name__ == "__main__":
    main()
