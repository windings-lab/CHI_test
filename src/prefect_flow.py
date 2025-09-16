"""
Prefect DAG for weather data processing pipeline.
"""

import os
from datetime import timedelta
from typing import List

from prefect import flow, task
from prefect.tasks import task_input_hash
from prefect.logging import get_run_logger

from src.data.pipeline import DataPipeline

pipeline = DataPipeline()

@task(
    cache_key_fn=task_input_hash,
    cache_expiration=timedelta(hours=1),
    retries=3,
    retry_delay_seconds=60,
    task_run_name="acquire-weather-data-{city}"
)
def acquire_weather_data(city: str) -> dict:
    """
    Acquire weather data for a specific city.
    
    Args:
        city: Name of the city to get weather data for
        
    Returns:
        Raw weather data dictionary
    """
    logger = get_run_logger()
    logger.info(f"Acquiring weather data for {city}")

    raw_data = pipeline.acquire(city)
    
    logger.info(f"Successfully acquired data for {city}")
    return raw_data


@task(
    task_run_name="process-weather-data-{city}"
)
def process_weather_data(raw_data: dict, city: str = None) -> dict:
    """
    Process raw weather data into structured format.
    
    Args:
        raw_data: Raw weather data from API
        city: City name for task naming
        
    Returns:
        Processed data dictionary with metadata
    """
    logger = get_run_logger()
    if city is None:
        city = raw_data.get("city", {}).get("name", "Unknown")
    logger.info(f"Processing weather data for {city}")

    processed_df = pipeline.process(raw_data)
    
    logger.info(f"Successfully processed data for {city}: {len(processed_df)} records")
    return {
        "city": city,
        "data": processed_df,
        "record_count": len(processed_df)
    }


@task(
    task_run_name="save-to-database-{city}"
)
def save_to_database(processed_data: dict, city: str = None) -> bool:
    """
    Save processed weather data to database.
    
    Args:
        processed_data: Processed data dictionary
        city: City name for task naming
        
    Returns:
        True if successful
    """
    logger = get_run_logger()
    if city is None:
        city = processed_data["city"]
    logger.info(f"Saving {processed_data['record_count']} records to database for {city}")

    pipeline.save_to_database(processed_data["data"])
    
    logger.info(f"Successfully saved data to database for {city}")
    return True


@task
def generate_analysis_report() -> dict:
    """
    Generate analysis report from all weather data.
    
    Returns:
        Analysis results dictionary
    """
    logger = get_run_logger()
    logger.info("Generating analysis report")

    pipeline.analyze()
    
    logger.info("Analysis report generated successfully")
    return {"status": "completed"}


@flow(
    name="weather-data-pipeline",
    description="Weather data acquisition, processing, and analysis pipeline",
    version="1.0.0"
)
def weather_pipeline(cities: List[str]) -> dict:
    """
    Main Prefect flow for weather data processing.
    
    Args:
        cities: List of cities to process. Defaults to predefined list.
        
    Returns:
        Pipeline execution summary
    """
    logger = get_run_logger()
    logger.info(f"Starting weather pipeline for {len(cities)} cities: {cities}")
    
    results = {
        "cities_processed": [],
        "total_records": 0,
        "errors": []
    }
    
    # Process each city
    for city in cities:
        try:
            # Acquire data
            raw_data = acquire_weather_data(city)
            
            # Process data
            processed_data = process_weather_data(raw_data, city=city)
            
            # Save to database
            save_success = save_to_database(processed_data, city=city)
            
            if save_success:
                results["cities_processed"].append(city)
                results["total_records"] += processed_data["record_count"]
                logger.info(f"Successfully completed pipeline for {city}")
            else:
                results["errors"].append(f"Failed to save data for {city}")
                
        except Exception as e:
            error_msg = f"Error processing {city}: {str(e)}"
            results["errors"].append(error_msg)
            logger.error(error_msg)
    
    # Generate analysis report
    try:
        generate_analysis_report()
        logger.info("Analysis report generated successfully")
    except Exception as e:
        error_msg = f"Error generating analysis report: {str(e)}"
        results["errors"].append(error_msg)
        logger.error(error_msg)
    
    logger.info(f"Pipeline completed. Processed {len(results['cities_processed'])} cities, "
                f"{results['total_records']} total records, {len(results['errors'])} errors")
    
    return results
