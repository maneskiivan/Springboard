# Springboard - Capstone Project

## VENUE INSIGHTS

### Overview

This project uses Foursquare's Places API to obtain data for
venues based on their location and write the details
into a database, so they can be analyzed.

The analyzed details provide insights on their impact to
the success of the venue. The success of a venue it is measured
by its rating. This can be used to determine where to open 
and what to include in a new venue of a specific type for best results.

### Installation

**Requirements**

python -m venv .venv
source .venv/bin/activate

pip3 install SQLAlchemy
pip3 install requests
pip3 install pandas
pip3 install keyring

**Create a Foursqaure App**

[Create an account.](https://foursquare.com/developers/signup)

[Create a new Foursquare App and obtain the client ID and
secret](https://developer.foursquare.com/docs/places-api/getting-started/)

### Let's get it started

[Create the SQL Schema](https://github.com/maneskiivan/Springboard/blob/main/files/create_tables.sql)

python3 main.py

### Getting Help

[Open a new issue](https://github.com/maneskiivan/Springboard/issues) 
