TechProject1
------------

### Introduction

This is a project for the course "Big Data Analytics" at the Atlantic Technological University Donegal.

The Project uses the dataset made public at [Divvy Data](https://divvybikes.com/system-data). The dataset is a collection of data from the bike sharing scheme in Chicago. The data is available in CSV format and is split into two files, one for the trips and one for the stations.

The goal is to make the project usable locally by loading a sample of the dataset, then using Pandas for speed and simplicity of the analysis. Then, use pySpark and synapse to train a model and make predictions. review performance, go back to feature engineering to improve performance.

When the model is ready, the project will be deployed to `<pending decision, over databricks or Collab>`. When that's done we'll run the model against the full dataset.

### Questions

* Which stations are the most used for collections?
* Which stations are busier during certain periods of the day?
  * During feature engineering. the day_period column will be added to the dataset to help target this question.
    * [bike_stations.py](divvy_bike_share_data_analysis/bike_stations.py)#categorize_time_of_day(hour)
* Which destinations are the most popular among users(by membership type)?
* Which periods of the day are these stations most visited?
* Which stations should be unloaded while restocking high-demand stations during peak hours?

### Tools and technologies

* Python 3.9.3
* PySpark
* Jupyter Notebook
* Pandas
* seaborn
* synapse

dependencies listed here: [requirements.txt](requirements.txt)

### Dataset Description

When loading the dataset the [divvy-tripdata-schema.yaml](documents/divvy-tripdata-schema-example.yaml)

#### Content:

```yaml
data_set: divvy-tripdata
version: 1.0.0
description: Divvy trip data
columns:
  ride_id: string
  rideable_type: string
  started_at: datetime
  ended_at: datetime
  start_station_name: string
  start_station_id: string
  end_station_name: string
  end_station_id: string
  start_lat: float
  start_lng: float
  end_lat: float
  end_lng: float
  member_casual: string
```

### Supporting module divvy_bik_share_data_analysis

The module [divvy_bik_share_data_analysis](divvy_bik_share_data_analysis.py) is intended to simplify the notebook with the analysis. By removing the initial data loading and csv parsing from the notebook, the notebook content focus on pyspark DataFrames.

Functions in the module:
        <Draft>