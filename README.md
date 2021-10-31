# Springboard - Capstone Project

## VENUE INSIGHTS

### Overview

- Collects the data by calling Foursquare Places API
- Stores the data into a database from where it can be analyzed
- The success of a venue is measured by its rating
- This insight can be used to determine a location for a new venue of a specific type and attributes to include in the same to get optimal results

### Installation

**Create a Foursqaure App**

[Create an account.](https://foursquare.com/developers/signup)

[Create a new Foursquare App and obtain the client ID and
secret](https://developer.foursquare.com/docs/places-api/getting-started/)

### Local Version

[Install MySql](https://dev.mysql.com/doc/mysql-installation-excerpt/5.7/en/)

[Create the SQL Schema](https://github.com/maneskiivan/Springboard/blob/master/local/database/create_tables.sql)

This repository includes the [categories](https://github.com/maneskiivan/Springboard/blob/master/local/files/categories.csv) and [lat_long](https://github.com/maneskiivan/Springboard/blob/master/local/files/lat_long.csv) files.

[Update the categories file with the most up-to-date categories](https://developer.foursquare.com/docs/api-reference/venues/categories/)

The lat_long file contains the lattitude and longtitude from all the cities in California

You can update the file to include lattitude and longtitude from other regions to get different results

Update the engine property from the SQLOperations class in the [main.py](https://github.com/maneskiivan/Springboard/blob/master/local/main.py) file with your database login info

Run the main.py file

### Azure Version

[Create Azure account](https://azure.microsoft.com/en-us/free/?v=b&adobe_mc_sdid=SDID%3D79107E4A5D861A7D-1C28B51C2ED92547%7CMCORGID%3DEA76ADE95776D2EC7F000101%40AdobeOrg%7CTS%3D1635718868&adobe_mc_ref=https%3A%2F%2Fwww.google.com%2F)

[Deploy](https://docs.microsoft.com/en-us/azure/azure-resource-manager/templates/template-tutorial-create-first-template?tabs=azure-powershell) the Azure resources using the [template and paramaters files](https://github.com/maneskiivan/Springboard/tree/master/azure/template)

[Deploy](https://docs.microsoft.com/en-us/azure/azure-functions/create-first-function-vs-code-python) code to Azure Functions

- The first function should include ingestion_venue_id.py and operations_azure.py. Set a time trigger to run every hour from 00:00 to 23:00. 
- The second function should include transform_load_venue_details.py and operations_azure.py. Set a time trigger to run at 23:00.
- The triggers are based on the assumption that a free tier developer's account is used to obtain the data from Foursquare.



### Getting Help

[Open a new issue](https://github.com/maneskiivan/Springboard/issues) 
