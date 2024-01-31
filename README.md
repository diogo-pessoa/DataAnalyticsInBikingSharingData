TechProject1
------------

### Introduction

This is a project for the course "Big Data Analytics" at the Atlantic Technological University Donegal.

The Project uses the dataset made public at [Divvy Data](https://divvybikes.com/system-data). The dataset is a collection of data from the bike sharing scheme in Chicago. The data is available in CSV format and is split into two files, one for the trips and one for the stations.


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