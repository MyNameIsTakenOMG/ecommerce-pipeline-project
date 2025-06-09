# Ecommerce Pipeline Project

## Table of Contents

- Kinesis Pipeline[#kinesis-pipeline]
- Ingestion[#ingestion]

- Virtual Environment and Package Management[#virtual-environment-and-package-management]

## Kinesis Pipeline

- Architecture:

  1. kinesis data stream
  2. kinesis firehose (a placeholder lambda function for stream processing -- enrich or filter data)
  3. s3 bucket for raw data

## Ingestion

- producer: a python script used to send 20 testing records from the dataset to our `Kinesis_Pipeline`.
  > Note: before running the command: `python ingestion/streaming_ingestion/producer.py`, please go download the dataset: **Online Retail.xlsx** from [UCI Machine Learning Repository](https://archive.ics.uci.edu/ml/datasets/Online+Retail), and then put the file under the `/data` folder.

## Virtual Environment and Package Management

- Current Design: For package management, this project is using one single virtual environment, but with multiple requirements.txt files. As such, we could relatively easily manage packages for each of our sub projects as well as the main project. In order to do it, we use a tool called `pip-compile` with multiple `requirements.in` files.

- Future Challenge & Solution: Right now, we are using one single virtual environment for our project, which consists of mutliple sub projects. However, as our project grows, we may encounter issues such as `Potential version conflicts`. And when that moment comes, we could switch to a `Layered` approach with `pip install -e`. In other words, we can make the main project installable as a package, then install it in subprojects using editable mode. By doing this, our code base will be more `Clean, modular, real-Pythonic`.
  > Note: since we are already using `pip-compile`, it will make later migration more smooth because every sub project has its own `requirements.in`. So with this setting, it is safe, compatible, future-proof.
