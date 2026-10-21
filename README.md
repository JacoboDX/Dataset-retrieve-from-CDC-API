# DATASET Provisional COVID-19 Deaths by Sex and Age
## Description
Script to download a dataset from CDC via API.
[Dataset](https://data.cdc.gov/National-Center-for-Health-Statistics/Provisional-COVID-19-Deaths-by-Sex-and-Age/9bhg-hcku/about_data)

Created for the final module of my Python specialization (University of Michigan).
## Requirements
Created on Python ver 3.13. No external libraries needed.

Database not included (created on first running).
## Features
1. Asks the user two things on running:
    -   Enter url. You can enter a different url to work with another dataset. By default (pressing Enter on request) runs with this [dataset](https://data.cdc.gov/National-Center-for-Health-Statistics/Provisional-COVID-19-Deaths-by-Sex-and-Age/9bhg-hcku/about_data)
    -   How many 1000 rows pages to download (limit of the API for each call)
2. Creates a db (`cdccovid.sqlite`) with 5 tables. Normalized tables avoid repeating the same text multiple times.
    -   `age_group`: lists all the values for age_group.
    -   `metodo`: lists all the values for metodo (metodo=Group:Indicator of whether data measured by Month, by Year, or Total).
    -   `sex`: lists all the values for sex.
    -   `state`: lists all the values for state.
    -   `Dataset`: presents all the information using the foreign keys for previous 4 tables.
3. Running the script again doesn't delete the tables or the db, adds the new data to the existing db.
## Usage
```
python data_retrieve_json.py
```