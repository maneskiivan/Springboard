import operations_azure
import pandas as pd


lat_long = pd.read_csv('files/lat_long.csv')
lat_long = pd.DataFrame(lat_long.iloc[-3:], columns=['lat_long'])
category = pd.read_csv('files/categories.csv')
category_temp_list = pd.DataFrame(['52f2ab2ebcbc57f1066b8b4a'], columns=['category'])


def test_get_venue_id():
  new_test = operations_azure.VenuesData()
  new_test.headers = 1
  new_test.get_id_data(category, lat_long, category_temp_list)


venues = pd.read_csv('files/id_data.csv')
venues = venues['venue_id']
venue_id = venues.iloc[-1]


def test_get_venue_details():
  new_test = operations_azure.VenuesData()
  new_test.get_venue_details(venue_id)


def test_set_table():
  new_test = operations_azure.SqlOperations()
  new_test.set_table('stats')


def test_write_to_table():
  new_test = operations_azure.SqlOperations()
  new_test.write_to_table({'key': 'value'})

