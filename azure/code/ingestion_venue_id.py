import operations_azure
import pandas as pd


def main():
  categories_path = '<PATH to the cateogires blob>'
  lat_long_path = '<PATH to the lat_long blob>'
  last_run_values_path = '<PATH to the last_run_values_path blob>'
  id_data_path = '<PATH to the id_data_path blob>'

  lat_long = pd.read_csv(lat_long_path)
  category = pd.read_csv(categories_path)
  new_search = operations_azure.VenuesData()
  new_search.last_value(category.iloc[0][0])

  # Getting the venues ids
  while not new_search.end_of_search:
    # Creating a temp list from the categories starting from the last used category
    last_run_values = pd.read_csv(last_run_values_path)
    new_value = last_run_values['values'].values[-1]
    position = category['category'][category['category'] == new_value].index.to_list()
    category_temp_list = category[(position[-1]):]
    new_search.get_id_data(category, lat_long, category_temp_list, id_data_path, last_run_values_path)

  return True
