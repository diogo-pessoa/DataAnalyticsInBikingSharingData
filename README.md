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

The project tested on `Google Collab Entrerpise`.

To see a full run of the Whole project, please refer to the notebook [supervisor_bikeshare](notebooks/supervisor_bikeshare.ipynb). 
This notebook calls all other notebooks in the correct order, and loads the images. 

### Notebooks description

This project have multiple notebooks, each with a specific scope. The idea is to simplify the analysis and make it easier to follow.
All notebooks cross-reference each other, accordingly to the flow of the analysis. Using magic runs, such as: `%run 'notebooks/data_collection.ipynb'`

#### Notebooks/

  * [supervisor_bikeshare](notebooks/supervisor_bikeshare.ipynb) - One to rule them all!
    * Calls notebooks in order to run the full analysis. Handy as I don't need to re-run previous steps, when I need to re-run subsets of the analysis.
  * [data_collection.ipynb](notebooks/data_collection.ipynb) - Being mindful of resource limitations, the default call only pulls the 2023 data.
    * Loads helper functions from helper module [divvy_bike_share_data_analysis](divvy_bike_share_data_analysis) to download trip rercords zip files and extract them to a local directory and loading into a PySpark DataFrame.
    * [feature_engineering.ipynb](notebooks/feature_engineering.ipynb)
      * Depends on `%run 'notebooks/data_collection.ipynb'` 
      * calls data_collection.ipynb, then split the data further `DataFrame.sample(0.1)`. Again, being mindful of resource limitations. A full year of trip records can take a while to process.
      * The notebook focus on feature engineering, such as creating new columns, and transforming the data to be used in the model. Removing Nulls and Duplicate rows.
      * An important portion of this notebook is the indexing of features `sampled_df_with_added_features_indexed`. I decided for that since multiple notebooks were repeating this step.
    * [data_exploration](notebooks/data_exploration.ipynb)
      * Depends on `%run 'notebooks/feature_engineering.ipynb'`
      * The notebook focus on the initial data exploration. Therefore, it converts the PySpark DataFrame to a Pandas DataFrame.
        * ```python
          sampled_df_with_added_features_indexed.toPandas()
          ``
      * The notebook is intended to be used to understand the data, visualize findings and patterns.
    * [regression_model.ipynb](notebooks/classification_model.ipynb)
      * Depends on `%run 'notebooks/feature_engineering.ipynb'` 
      * The notebook focus on training a regression model using PySpark. The model is trained using the `sampled_df_with_added_features_indexed` DataFrame.
      * I've also split the training in to contexts, working days and non-working days. I've decided for the split, due to performance issues. The model was taking too long to train(local laptop).
      * The model is trained using the `sampled_df_with_added_features_indexed` DataFrame.
    * [sillhouette_index_scores.ipynb](notebooks/sillhouette_score.ipynb)
      * Depends on `%run 'notebooks/feature_engineering.ipynb'`
      * The notebook focus on the Silhouette analysis of the dataset. The goal is to find the optimal number of clusters for the dataset.
    * [clustering_analysis.ipynb](notebooks/clustering_analysis.ipynb)
      * Depends on `%run 'notebooks/feature_engineering.ipynb'`
      * `<Pending>`

### Questions

* Which stations are the most used for collections?
* Which stations are busier during certain periods of the day?
    * During feature engineering. the day_period column will be added to the dataset to help target this question.
        * [bike_stations.py](divvy_bike_share_data_analysis/bike_stations.py)#categorize_time_of_day(hour)
* Which destinations are the most popular among users(by membership type)?
* Which periods of the day are these stations most visited?
* Which stations should be unloaded while restocking high-demand stations during peak hours?



#### Using the Notebook
  
The notebook is intended to be used in a Jupyter environment. The notebook is divided into sections. 
Having said that, the Notebook uses helper functions from the module [divvy_bik_share_data_analysis](divvy_bike_share_data_analysis) to simplify the notebook content.

Here are a few important points:
* Using `dotenv` to load certain environment variables, without explicity declaring sensitive information in the notebook.
* Python version is 3.9
  * I loaded a virtual environment and had the dependencies listed here: [requirements.txt](requirements.txt)
    * Install venv: `python -m venv venv` (make sure to run this using python3.9
    * Activate the virtual environment: `source venv/bin/activate`
    * Install dependencies:  `pip install -r requirements.txt`
  * Create a `.env` file:
    * for now the only required entry is the `IMAGE_PATH`. This is the path to save plot figures and load then to our LaTeX report.
      * The `.env` file should be in the root of the project.
        * Example:
          ```dotenv
             IMAGES_PATH='../Reports/TechReport/images/'
             DATA_COLLECTION_DIR='../data_collection/'
          ```
  * PySpark preset Schema for Divvy Trip Data:
    * The schema example is defined in the [divvy-tripdata-schema.yaml](documents/divvy-tripdata-schema-example.yaml).
      * Copy this file to the DATA_COLLECTION_DIR and rename it to `divvy-tripdata-schema.yaml`
      * The function [`load_divvy_trip_data`](divvy_bike_share_data_analysis/utils_pyspark.py#L51) will use this file to create a PySpark StructType object.

##### Pylint & Unit Tests

* Pylint
  * The project uses pylint to check the code for errors and style issues.
  * To run pylint, use the following command:
    * `pylint $(git ls-files '*.py') `
* Unit Tests
  * The project uses the `unittest` module to run tests.
  * To run the tests, use the following command:
    * `python -m unittest discover -s tests/ -p '*_test.py'`


#### DataSet Schema

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
* [PySpark Pipeline](https://spark.apache.org/docs/latest/api/python/reference/api/pyspark.ml.Pipeline.html)
* [Spark ML Lib Pipeline main guide](https://spark.apache.org/docs/latest/ml-pipeline.html)

* Referenced articles:
  * [Traffic prediction in a bike-sharing system](https://dl.acm.org/doi/abs/10.1145/2820783.2820837)
  * [Bicycle-Sharing System Analysis and Trip Prediction](https://ieeexplore.ieee.org/abstract/document/7517792)
  * [Bike-sharing systems: Accessibility and availability](https://www.sciencedirect.com/science/article/pii/S0965856419301063)
