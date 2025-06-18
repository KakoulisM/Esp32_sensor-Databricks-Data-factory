# Esp32_sensor-Databricks-Data-factory
# IoT Sensor Data Pipeline

This repository contains the code and infrastructure setup for an end-to-end IoT sensor data pipeline that collects data from ESP32 devices, ingests it via a Flask API, processes and transforms it in Azure Databricks, and manages automation through Azure Data Factory (ADF).

---

## Architecture Overview

1. **ESP32 Devices**  
   Collect temperature and humidity data and send JSON payloads via HTTP POST to a Flask API server.

2. **Flask API Server**  
   Receives sensor data, logs it locally, and uploads files to Azure Data Lake Storage (ADLS).

3. **Azure Data Lake Storage (ADLS)**  
   Raw sensor data is stored here under the `demo/raw` container.

4. **Azure Databricks**  
   - **Ingestion Notebook:** Reads raw JSON files from ADLS.  
   - **Transformation Notebook:** Cleans, splits timestamp, and aggregates data by 30-minute intervals.  
   - **Presentation Notebook:** Prepares aggregated data tables for reporting and visualization.

5. **Azure Data Factory (ADF)**  
   Automates the pipelines for ingestion, transformation, and presentation by triggering Databricks notebooks in sequence.

---

## Repository Structure
/flask-api
- app.py # Flask API server code
- requirements.txt # Python dependencies

/databricks-notebooks
/ingestion
- ingestion.ipynb # Reads raw JSON files from ADLS
/transformation
- transform.ipynb # Cleans and aggregates data
/presentation
- presentation.ipynb # Creates tables for reporting

/adf-pipelines
- ingestion-pipeline.json # Exported ADF pipeline JSON
- transform-pipeline.json # Exported ADF pipeline JSON
- presentation-pipeline.json # Exported ADF pipeline JSON


---

## Setup Instructions 
python app.py
After the file is run then it will start creating a file for measurements
Before you run the saving_and_loading you need to configure the tenant_id, client_id and secret as long as your storage account, directory name and file system from AZURE
python saving_and_loading
After this file is run ( you can trigger it automatically through the day to have updated values in your project ) it sends a backup file to your azure blob you can use
Azure Databricks

    Upload notebooks from /databricks-notebooks folder.

    Configure cluster and linked services for ADLS access.

    Run notebooks manually or via ADF.
Azure Data Factory

    Import pipelines from /adf-pipelines.

    Link pipelines to corresponding Databricks notebooks.

    Schedule or trigger pipelines in sequence for automation.   
Notes

    Ensure your ADLS storage account is mounted correctly in Databricks.

    Secrets such as client IDs and secrets are managed via Azure Key Vault and accessed securely in Databricks.

    JSON files from the ESP32 must follow the expected schema (array of objects with timestamp, humidity, temperature_c).   

For questions or support, please reach out to Minas at kakoulisminas@hotmail.com.    
