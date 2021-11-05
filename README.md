# Springboard - Capstone Project

## VENUE INSIGHTS

### Overview

- Collects the data by calling Foursquare Places API
- Stores the data into a database from where it can be analyzed
- The success of a venue is measured by its rating
- This insight can be used to determine a location for a new venue of a specific type and attributes to include in the same to get optimal results

### Installation

**Create a Foursquare App**

[Create an account.](https://foursquare.com/developers/signup)

[Create a new Foursquare App and obtain the client ID and
secret](https://developer.foursquare.com/docs/places-api/getting-started/)

#### Local Version

[Install MySql](https://dev.mysql.com/doc/mysql-installation-excerpt/5.7/en/)

[Create the SQL Schema](https://github.com/maneskiivan/Springboard/blob/master/local/database/create_tables.sql)

This repository includes the [categories](https://github.com/maneskiivan/Springboard/blob/master/local/files/categories.csv) and [lat_long](https://github.com/maneskiivan/Springboard/blob/master/local/files/lat_long.csv) files.

[Update the categories file with the most up-to-date categories](https://developer.foursquare.com/docs/api-reference/venues/categories/)

The lat_long file contains the lattitude and longtitude from all the cities in California

You can update the file to include lattitude and longtitude from other regions to get different results

Update the engine property from the SQLOperations class in the [main.py](https://github.com/maneskiivan/Springboard/blob/master/local/main.py) file with your database login info

Run the main.py file

#### Azure Version

[Create Azure account](https://azure.microsoft.com/en-us/free/?v=b&adobe_mc_sdid=SDID%3D79107E4A5D861A7D-1C28B51C2ED92547%7CMCORGID%3DEA76ADE95776D2EC7F000101%40AdobeOrg%7CTS%3D1635718868&adobe_mc_ref=https%3A%2F%2Fwww.google.com%2F)

[Deploy](https://docs.microsoft.com/en-us/azure/azure-resource-manager/templates/template-tutorial-create-first-template?tabs=azure-powershell) the Azure resources using the [template and paramaters files](https://github.com/maneskiivan/Springboard/tree/master/azure/template)

[Deploy](https://docs.microsoft.com/en-us/azure/azure-functions/create-first-function-vs-code-python) code to Azure Functions

- The first function should include ingestion_venue_id.py and operations_azure.py. [Set a time trigger](https://github.com/maneskiivan/Springboard/tree/master/azure/code/azure_func_ingestion) to run every hour from 00:00 to 23:00. 
- The second function should include transform_load_venue_details.py and operations_azure.py. [Set a time trigger](https://github.com/maneskiivan/Springboard/tree/master/azure/code/azure_func_transform_load) to run at 23:00.
- The triggers are based on the assumption that a free tier developer's account is used to obtain the data from Foursquare.

This repository includes the [categories](https://github.com/maneskiivan/Springboard/blob/master/local/files/categories.csv) and [lat_long](https://github.com/maneskiivan/Springboard/blob/master/local/files/lat_long.csv) files.

[Update the categories file with the most up-to-date categories](https://developer.foursquare.com/docs/api-reference/venues/categories/)

The lat_long file contains the lattitude and longtitude from all the cities in California

You can update the file to include lattitude and longtitude from other regions to get different results

Upload the [categories](https://github.com/maneskiivan/Springboard/blob/master/local/files/categories.csv) and [lat_long](https://github.com/maneskiivan/Springboard/blob/master/local/files/lat_long.csv) files to the blob storage

Upload the [files](https://github.com/maneskiivan/Springboard/tree/master/azure/files) folder to the blob storage.

### Example Analysis

A client wants to find out the best location in California to open a bar and which atributes to include for optimal results.

Here is map of California showing the following average rating per city:
- 6 and below
- between 6 and 8
- 8 and above

![Picture1](https://user-images.githubusercontent.com/74036152/140433384-6834f807-06ab-439f-a3ab-04c34040d4af.png)

First we find all venues with rating above 8 that have "Bar" as their primary category.

Then we group the data per city and find the average rating, popularity and total tips ordered by rating.

Popularity description:
- Measure of a POI's popularity by foot traffic. This score is on a 0 to 1 scale and uses a 6-month span of POI visits. The most popular POI in the geographic area is assigned the score .9999. This score is calculated across all POIs within the same country.

Total Tips description:
- Total recommendations (or warnings) posted by foursquare users on foursquare's site and apps.

| City  | Average Rating | Average Popularity | Average Total Tips   | 
| ------------- | ------------- | --------------- | ---------------- |
|       Whittier|          8.92|0.9568734848539859|               5.0|
|       La Jolla|          8.89| 0.951238505129577|               6.0|
|North Hollywood|          8.89|0.9406555998467995|              19.0|
|    Pismo Beach|          8.85|0.9932291097758676|              17.0|
|        Fairfax|          8.85|0.9171330328134413|              25.0|
|    Paso Robles|          8.85|0.9419249969216203|              11.0|
|  Beverly Hills|          8.85|0.9370693068786837|               4.0|
|    Santa Paula|          8.81|0.9590532248363515|              22.0|
|        Belmont|          8.75|0.9529028386136492|              10.0|
|         Fresno|          8.73|0.9350863205460713|               7.0|
|       Lakeside|          8.73|0.9794969873594084|              26.0|
|      San Mateo|           8.7|0.9095310187111407|              33.0|
|      Oceanside|          8.67|0.9413789997498672|              21.0|
|           Ojai|          8.67|0.8443035917313101|               4.0|
|     Emeryville|          8.66|0.9249143422518536|              45.0|
|    Joshua Tree|          8.66|0.9732232728281742|              47.0|
|     Winchester|           8.6| 0.969908819708304|              16.0|
|        Alameda|           8.6|0.9025801379083179|              25.0|
|      Fullerton|           8.6|0.9505599097482434|               7.0|
|       Glendale|          8.58|0.9295751712498345|              30.0|

<img width="1608" alt="Screen Shot 2021-11-04 at 4 21 57 PM" src="https://user-images.githubusercontent.com/74036152/140433641-4fcb147c-e3a7-49ac-addd-6f943eca164c.png">

Let's analyse the atributes effect on the rating.

Atributes description:
- The venues atributes are predefined by [foursquare](https://docs.foursquare.com/docs/places-data-schema#tags).
- A venue can have one or more atributes associated to it

We group the data per rating and count the atributes ordered by rating.

![atributes1](https://user-images.githubusercontent.com/74036152/140456249-802d586f-5210-417c-abb1-d86f85a9a108.png)

![atributes2](https://user-images.githubusercontent.com/74036152/140456266-314f5f4e-6d5b-4a1c-bbd7-15ed1b2edd66.png)

### Getting Help

[Open a new issue](https://github.com/maneskiivan/Springboard/issues)
