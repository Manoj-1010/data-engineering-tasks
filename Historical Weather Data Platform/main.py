from pyspark.sql import SparkSession
from extract.extractor import WeatherDataExtractor
from transform.processor import WeatherDataProcessor
from gold.processor import GoldProcessor


def create_spark_session() -> SparkSession:
    """
    Create and configure the Spark session.
    """

    return (
        SparkSession.builder
        .appName("Historical Weather Data Platform")
        .getOrCreate()
    )


def main() -> None:
    """
    Run the complete weather data pipeline.
    """

    # spark = create_spark_session()

    try:
        print("=" * 60)
        print("Weather Data Pipeline")
        print("=" * 60)

        print("\n[1/3] Extracting Bronze data...")
        # WeatherDataExtractor().collect()

        print("\n[2/3] Building Silver dataset...")
        # WeatherDataProcessor(
        #     spark
        # ).run()
        
        print("\n[3/3] Building Gold datasets...")
        GoldProcessor(
            spark
        ).run()


    finally:
        print("\nPipeline completed successfully.")
        # spark.stop()


if __name__ == "__main__":
    main()