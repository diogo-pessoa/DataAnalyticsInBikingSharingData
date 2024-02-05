TechProject1
------------

### Introduction

This is a project for the course "Big Data Analytics" at the Atlantic Technological University Donegal.

The Project uses the dataset made public at [Divvy Data](https://divvybikes.com/system-data). The dataset is a
collection of data from the bike sharing scheme in Chicago. The data is available in CSV format and is split into two
files, one for the trips and one for the stations.

The goal is to make the project usable locally by loading a sample of the dataset, then using Pandas for speed and
simplicity of the analysis. Then, use pySpark and synapse to train a model and make predictions. review performance, go
back to feature engineering to improve performance.

When the model is ready, the project will be deployed to `<pending decision, over databricks or Collab>`. When that's
done we'll run the model against the full dataset.

### Questions

* Which stations are the most used for collections?
* Which stations are busier during certain periods of the day?
    * During feature engineering. the day_period column will be added to the dataset to help target this question.
        * [bike_stations.py](divvy_bike_share_data_analysis/bike_stations.py)#categorize_time_of_day(hour)
* Which destinations are the most popular among users(by membership type)?
* Which periods of the day are these stations most visited?
* Which stations should be unloaded while restocking high-demand stations during peak hours?

### Tools and technologies

* Python 3.8.5
* PySpark 3.0.1
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

The module [divvy_bik_share_data_analysis](divvy_bik_share_data_analysis.py) is intended to simplify the notebook with
the analysis. By removing the initial data loading and csv parsing from the notebook, the notebook content focus on
pyspark DataFrames.

Functions in the module:
<Draft>

### References and links to resources used

* [Divvy Data](https://divvybikes.com/system-data)
* [Divvy Data License](https://www.divvybikes.com/data-license-agreement)
* [Confusion Matrix scikit-learn user-guide](https://scikit-learn.org/stable/modules/model_evaluation.html#confusion-matrix)
* [Sillhoute index Analysis scikit-learn](https://scikit-learn.org/stable/auto_examples/cluster/plot_kmeans_silhouette_analysis.html)
* [PCA scikit-learn](https://scikit-learn.org/stable/auto_examples/decomposition/plot_pca_iris.html#sphx-glr-auto-examples-decomposition-plot-pca-iris-py)
* [PCA Towards Science article PCA discussion](https://towardsdatascience.com/a-one-stop-shop-for-principal-component-analysis-5582fb7e0a9c)
* [Optimal K=n for kmeans clustering ML tutorial](https://pub.towardsai.net/get-the-optimal-k-in-k-means-clustering-d45b5b8a4315)**
* PySpark Functions:
    * [udf](https://spark.apache.org/docs/3.1.3/api/python/reference/api/pyspark.sql.functions.udf.html)
    * [dayofweek](https://spark.apache.org/docs/3.1.3/api/python/reference/api/pyspark.sql.functions.dayofweek.html)
    * [hour](https://spark.apache.org/docs/3.1.3/api/python/reference/api/pyspark.sql.functions.hour.html)
    * [col](https://spark.apache.org/docs/3.1.3/api/python/reference/api/pyspark.sql.functions.col.html)
* [PySpark StructType](https://spark.apache.org/docs/3.1.3/api/python/reference/api/pyspark.sql.types.StructType.html#pyspark.sql.types.StructType)
* [PySpark SQL User-guides](https://spark.apache.org/docs/latest/sql-programming-guide.html)
* [PySpark MLlib User-guides](https://spark.apache.org/docs/latest/ml-guide.html)
* [PySpark Functions User-guides](https://spark.apache.org/docs/3.1.2/api/python/user_guide/arrow_pandas.html#pandas-udfs-a-k-a-vectorized-udfs)
* [Traffic prediction in a bike-sharing system](https://dl.acm.org/doi/abs/10.1145/2820783.2820837)
* [Bicycle-Sharing System Analysis and Trip Prediction](https://ieeexplore.ieee.org/abstract/document/7517792)