import json, requests, keyring, csv, logging, os
from datetime import datetime
from sqlalchemy import create_engine, MetaData, insert, Table
from azure.cosmos import CosmosClient, PartitionKey, exceptions
from azure.keyvault.secrets import SecretClient
from azure.identity import DefaultAzureCredential


logging.basicConfig(
  filename='files/app.log',
  filemode='a',
  format='%(asctime)s - %(message)s',
  datefmt='%d-%b-%y %H:%M:%S',
  level=logging.INFO
)


keyVaultName = '<KeyVault Name>'
KVUri = f"https://{keyVaultName}.vault.azure.net"
credential = DefaultAzureCredential()
client = SecretClient(vault_url=KVUri, credential=credential)
client_id_name = '<Client ID Name>'
client_secret_name = '<Client Secret Name>'
client_id = client.get_secret(client_id_name)
client_secret = client.get_secret(client_secret_name)


class SqlOperations:
  """
  Connects to the database.
  Writtes to the database.
  """
  def __init__(self):
    try:
      # Define an engine to connect to the database and make a connection
      self.engine = create_engine('<Connection to Azure SQL>')
      self.connection = self.engine.connect()
      # Initialize empty MetaData: metadata
      self.metadata = MetaData()
      self.table = None
      self.running = True
      self.resultproxy = None
      self.cdb_url = '<Cosmos DB URL>'
      self.cdb_key = '<Cosmos DB Key>'
      self.cdb_client = CosmosClient(self.cdb_url, credential=self.cdb_key)
      database_name = 'springboard_venues'
      self.cdb_database = self.cdb_client.get_database_client(database_name)
      self.cdb_container = None
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


  def create_cdb_container(self, container_name):
    try:
      self.cdb_container = self.cdb_database.create_container(
        id=container_name,
        partition_key=PartitionKey(path="/productName")
      )
    except exceptions.CosmosResourceExistsError:
      self.cdb_container = self.cdb_database.get_container_client(container_name)
    except exceptions.CosmosHttpResponseError:
      raise


  def write_to_cdb(self, body):
    try:
      self.cdb_container.upsert_item(json.load(body))
    except:
      raise


class VenuesData(SqlOperations):
  """
  Gets the venues ids based on searching all lat_long for all categories
  Gets the details of venues by using the previously obtained venues ids
  """
  def __init__(self):
    SqlOperations().__init__()
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
    self.headers = 5000


  def get_id_data(self, category, lat_long, category_temp_list, id_data_path, last_run_values_path):
    # URL to search venues example with offset
    url = 'https://api.foursquare.com/v2/venues/search'
    # Create the lat_long generator
    ll_iter = self.ll_generator(lat_long['lat_long'])
    # value to be saved in the last run values file
    category_id = None
    with open(id_data_path, 'a') as csv_file:
      # creating a csv writer object
      csvwriter = csv.writer(csv_file)
      # Going over the 5000 requests limit per hour
      while self.headers > 1:
        for i in category_temp_list['category']:
          category_id = i
          logging.info(f"Runs category ID: {category_id}")
          if self.headers < 1:
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
              self.headers = int(dict(resp.headers)['X-RateLimit-Remaining'])
            except:
              logging.warning('The headers did not return a X-RateLimit-Remaining value')

            if self.headers < 1:
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
    self.last_value(category_id, last_run_values_path)


  def last_value(self, value, last_run_values_path):
    with open(last_run_values_path, 'a') as csv_file:
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
      yield


  def get_venue_details(self, venue_id, container_name):
    url = f'https://api.foursquare.com/v2/venues/{venue_id}'
    resp = requests.get(url=url, params=self.params)
    data = json.loads(resp.text)
    self.create_cdb_container(container_name)
    self.write_to_cdb(data)
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
        self.venue['days'] = None

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
