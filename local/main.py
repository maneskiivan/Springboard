import json, requests, keyring, csv, time, logging
from datetime import datetime
import pandas as pd
import numpy as np
from sqlalchemy import create_engine, MetaData, insert, Table


logging.basicConfig(
  filename='files/app.log',
  filemode='a',
  format='%(asctime)s - %(message)s',
  datefmt='%d-%b-%y %H:%M:%S',
  level=logging.INFO
)


class VenuesData:
  """
  Gets the venues ids based on searching all lat_long for all categories
  Gets the details of venues by using the previously obtained venues ids
  """
  def __init__(self):
    self.params = dict(
          client_id=client_id,
          client_secret=client_secret,
          v='20210529'  # <-- specifies the latest date for the API version
        )
    self.venue = dict()
    self.contact = None
    self.location = None
    self.categories = []
    self.price = None
    self.rating = None
    self.stats = None
    self.attributes = []
    self.end_of_search = False
    self.response_code = None


  def get_id_data(self):
    # URL to search venues example with offset
    url = 'https://api.foursquare.com/v2/venues/search'
    last_run_values = pd.read_csv('files/last_run_values.csv')
    # Creating a temp list from the categories starting from the last used category
    new_value = last_run_values['values'].values[-1]
    position = category['category'][category['category'] == new_value].index.to_list()
    category_temp_list = category[(position[-1]):]
    # Create the lat_long generator
    ll_iter = self.ll_generator(lat_long['lat_long'])
    # value to be saved in the last run values file
    category_id = None
    with open('files/id_data.csv', 'a') as csv_file:
      # creating a csv writer object
      csvwriter = csv.writer(csv_file)
      headers = 5000
      # Going over the 5000 requests limit per hour
      while headers > 1:
        for i in category_temp_list['category']:
          category_id = i
          logging.info(f"Runs category ID: {category_id}")
          if headers < 1:
            break
          if self.end_of_search:
            break
          for a in range(1, len(lat_long)):
            try:
              ll = next(ll_iter)
            except StopIteration:
              # Reset the lat_long generator
              ll_iter = self.ll_generator(lat_long['lat_long'])
              logging.info('The lat_long generator was reset')
              ll = next(ll_iter)

            self.params['ll'] = ll
            self.params['categoryId'] = category_id
            self.params['limit'] = 50

            resp = requests.get(url=url, params=self.params)

            try:
              headers = int(dict(resp.headers)['X-RateLimit-Remaining'])
            except:
              logging.warning('The headers did not return a X-RateLimit-Remaining value')

            if headers < 1:
              break
            if category_id == category['category'].tail(1).item() and ll == lat_long['lat_long'].tail(1).item():
              self.end_of_search = True
              break

            data = json.loads(resp.text)
            if data['meta']['code'] != 200:
              logging.warning(f"Error code in response: {data['meta']['code']}")

            try:
              for venue in data['response']['venues']:
                # writing the data rows to the csv file
                csvwriter.writerows(
                  [
                    [venue['id'], str(datetime.now())]
                  ]
                )
            except:
              logging.critical("Did not write into the id_data.csv file")

    # Writing the last category id used in the while loop
    # Will be used to start from there on the next run
    self.last_value(category_id)


  def last_value(self, value):
    with open('files/last_run_values.csv', 'a') as csv_file:
      # creating a csv writer object
      csvwriter = csv.writer(csv_file)
      csvwriter.writerows(
        [
          [value]
        ]
      )
      logging.info("Wrote the last used category ID to the file")


  def ll_generator(self, ll_list):
    """Yields the next value for lat_long"""
    for i in ll_list:
      yield i


  def get_venue_details(self, venue_id):
    url = f'https://api.foursquare.com/v2/venues/{venue_id}'
    resp = requests.get(url=url, params=self.params)
    data = json.loads(resp.text)
    self.response_code = data['meta']['code']
    if self.response_code == 200:
      self.venue['venue_name'] = data['response']['venue']['name']

      if 'url' in data['response']['venue'].keys():
        self.venue['url'] = data['response']['venue']['url']
      else:
        self.venue['url'] = None

      self.contact = data['response']['venue']['contact']

      self.venue['canonical_url'] = data['response']['venue']['canonicalUrl']
      self.venue['verified'] = data['response']['venue']['verified']

      self.location = data['response']['venue']['location']
      if 'labeledLatLngs' in self.location.keys():
        del self.location['labeledLatLngs']
      if 'isServiceAreaBusiness' in self.location.keys():
        del self.location['isServiceAreaBusiness']
      if 'isFuzzed' in self.location.keys():
        del self.location['isFuzzed']
      if 'formattedAddress' in self.location.keys():
        self.location['formattedAddress'] = self.location['formattedAddress'][0]

      categories = data['response']['venue']['categories']
      if categories:
        for i in categories:
          if 'primary' in i.keys():
            self.categories.append({'name': i['name'], 'prim': i['primary']})
          else:
            self.categories.append({'name': i['name'], 'prim': False})
      else:
        pass

      createdat = int(data['response']['venue']['createdAt'])
      createdat = datetime.utcfromtimestamp(createdat).strftime('%Y-%m-%d %H:%M:%S')
      self.venue['createdat'] = createdat

      if 'description' in data['response']['venue'].keys():
        self.venue['venue_desc'] = data['response']['venue']['description']
      else:
        self.venue['venue_desc'] = None

      self.venue['herenow'] = data['response']['venue']['hereNow']['count']

      if 'hours' in data['response']['venue'].keys():
        time_frame = data['response']['venue']['hours']['timeframes']
        self.venue['days'] = time_frame[0]['days']
      else:
        self.venue['days'] =  None

      self.venue['likes'] = data['response']['venue']['likes']['count']
      self.venue['listed'] = data['response']['venue']['listed']['count']
      self.venue['photos'] = data['response']['venue']['photos']['count']

      if 'price' in data['response']['venue'].keys():
        self.price = data['response']['venue']['price']
      else:
        self.price = {'currency': None, 'message': None, 'tier': None}

      if 'rating' in data['response']['venue'].keys():
        self.venue['rating'] = data['response']['venue']['rating']
      else:
        self.venue['rating'] = None

      self.stats = data['response']['venue']['stats']
      self.venue['tips'] = data['response']['venue']['tips']['count']

      attributes = data['response']['venue']['attributes']['groups']
      if attributes:
        for i in attributes:
          self.attributes.append(i['name'])
      else:
        pass


class SqlOperations:
  """
  Connects to the database.
  Writtes to the database.
  """
  def __init__(self):
    try:
      # Define an engine to connect to the database and make a connection
      self.engine = create_engine('mysql+pymysql://root:Welcome1@localhost:3306/springboard_venues')
      self.connection = self.engine.connect()
      # Initialize empty MetaData: metadata
      self.metadata = MetaData()
      self.table = None
      self.running = True
      self.resultproxy = None
    except:
      self.running = False
      logging.critical('Did not connect to the database.')


  def set_table(self, table):
    self.table = Table(table, self.metadata, autoload=True, autoload_with=self.engine)


  def write_to_table(self, values_dict):
    try:
      stmt = insert(self.table).values(values_dict)
      self.resultproxy = self.connection.execute(stmt)
    except:
      logging.critical(f'Did not write to the table\n{values_dict}')
      self.running = False



if __name__ == '__main__':
  client_id = keyring.get_password('foursquare_client_id', 'foursquare_client_id')
  client_secret = keyring.get_password('foursquare_client_secret', 'foursquare_client_secret')

  lat_long = pd.read_csv('files/lat_long.csv')
  category = pd.read_csv('files/categories.csv')
  new_search = VenuesData()
  new_search.last_value(category.iloc[0][0])
  # Getting the venues ids
  while not new_search.end_of_search:
    new_search.get_id_data()
    time.sleep(3600)


  # Reading the venue ids file and filtering for the unique ids
  venues = pd.read_csv('files/id_data.csv')
  unique_venues = venues['venue_id'].unique()

  # Write the first unique venue as the last run value
  new_search.last_value(unique_venues[0])


  # Getting the details for each venue and writing them to the database
  new_sql = SqlOperations()
  new_search.end_of_search = False
  while not new_search.end_of_search:
    # Creating a temp list from the venues ids starting from the last used venue id
    last_run_values = pd.read_csv('files/last_run_values.csv')
    new_value = last_run_values['values'].values[-1]
    position = np.where(unique_venues == new_value)[0][0]
    venue_id_temp_list = unique_venues[position:]
    for venue_id in venue_id_temp_list:
      # Get the details of the venue
      new_search.get_venue_details(venue_id)

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

    # Will sleep for an hour until the hourly limit is reset
    logging.info('Putting the app to sleep until the hourly limit is reset')
    time.sleep(3600)
