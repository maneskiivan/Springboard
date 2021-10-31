import pandas as pd
import numpy as np
import operations_azure
import logging


logging.basicConfig(
  filename='files/app.log',
  filemode='a',
  format='%(asctime)s - %(message)s',
  datefmt='%d-%b-%y %H:%M:%S',
  level=logging.INFO
)


def main():
  id_data_path = '<PATH to the id_data_path blob>'
  last_run_values_path = '<PATH to the last_run_values_path blob>'
  container_name = '<The name of the container>'
  # Reading the venue ids file and filtering for the unique ids
  venues = pd.read_csv(id_data_path)
  unique_venues = venues['venue_id'].unique()

  # Getting the details for each venue and writing them to the database
  new_search = operations_azure.VenuesData()
  # Write the first unique venue as the last run value
  new_search.last_value(unique_venues[0])
  new_sql = operations_azure.SqlOperations()
  while not new_search.end_of_search:
    # Creating a temp list from the venues ids starting from the last used venue id
    last_run_values = pd.read_csv(last_run_values_path)
    new_value = last_run_values['values'].values[-1]
    position = np.where(unique_venues == new_value)[0][0]
    venue_id_temp_list = unique_venues[position:]
    for venue_id in venue_id_temp_list:
      # Get the details of the venue
      new_search.get_venue_details(venue_id, container_name)

      # The for loop will break when the hourly/daily limit is reached
      if new_search.response_code == 429:
        new_search.last_value(venue_id)
        break

      # Write the details to the database
      new_sql.set_table('stats')
      new_sql.write_to_table(new_search.stats)
      stats_pk = new_sql.resultproxy.inserted_primary_key[0]


      new_sql.set_table('location')
      new_sql.write_to_table(new_search.location)
      location_pk = new_sql.resultproxy.inserted_primary_key[0]


      new_sql.set_table('category')
      categories_pk = list()
      for category in new_search.categories:
        new_sql.write_to_table(category)
        categories_pk.append(new_sql.resultproxy.inserted_primary_key[0])
      new_search.categories.clear()


      new_sql.set_table('contact')
      new_sql.write_to_table(new_search.contact)
      contact_pk = new_sql.resultproxy.inserted_primary_key[0]


      new_sql.set_table('price')
      new_sql.write_to_table(new_search.price)
      price_pk = new_sql.resultproxy.inserted_primary_key[0]


      new_sql.set_table('venue')
      new_search.venue['contact_id'] = contact_pk
      new_search.venue['location_id'] = location_pk
      new_search.venue['stats_id'] = stats_pk
      new_search.venue['price_id'] = price_pk
      new_sql.write_to_table(new_search.venue)
      venue_pk = new_sql.resultproxy.inserted_primary_key[0]


      new_sql.set_table('categories')
      categories = dict()
      for i in categories_pk:
        categories['category_id'] = i
        categories['venue_id'] = venue_pk
        new_sql.write_to_table(categories)


      new_sql.set_table('attributes')
      attributes = dict()
      for attribute in new_search.attributes:
        attributes['name'] = attribute
        attributes['venue_id'] = venue_pk
        new_sql.write_to_table(attributes)


      # The for loop will break when the last unique venue id completes running
      # This will cause the app the finish as well by breaking the while loop
      if venue_id == unique_venues[-1]:
        new_search.end_of_search = True
        break

    # break the while loop
    break
