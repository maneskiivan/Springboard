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

Update the [main.py](https://github.com/maneskiivan/Springboard/blob/master/local/main.py) file with your database login info

Run the main.py file

### Getting Help

[Open a new issue](https://github.com/maneskiivan/Springboard/issues) 
