# -*- coding: utf-8 -*-
"""harvard_hackathon_main.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1tIyv4MMGA2j7Q-tdNgz8NVOQKDWN3fHJ

# Imports
"""

!pip install pandas numpy matplotlib seaborn gspread import_ipynb

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import gspread

from google.colab import drive
from google.colab import auth
from google.auth import default
from oauth2client.client import GoogleCredentials

drive.mount('/content/drive')

"""# Google Sheet Functions"""

def read_google_sheet(sheet_url, sheet_name='Sheet1'):
  """Reads a Google Sheet into a pandas DataFrame.

  Args:
    sheet_url: The URL of the Google Sheet.
    sheet_name: The name of the worksheet to read from.
      Defaults to 'Sheet1'.

  Returns:
    A pandas DataFrame containing the sheet data.
  """

  # Authenticate with Google
  creds, _ = default()
  gc = gspread.authorize(creds)

  # Open the spreadsheet by URL
  spreadsheet = gc.open_by_url(sheet_url)

  # Select the worksheet by name
  worksheet = spreadsheet.worksheet(sheet_name)

  # Get all data as a list of lists
  data = worksheet.get_all_values()

  # Convert to a pandas DataFrame
  df = pd.DataFrame(data[1:], columns=data[0])

  return df


def write_to_google_sheet(df, sheet_url, sheet_name='Sheet1'):
  """Writes a pandas DataFrame to a Google Sheet.

  Args:
    df: The pandas DataFrame to write.
    sheet_url: The URL of the Google Sheet.
    sheet_name: The name of the worksheet to write to.
      Defaults to 'Sheet1'.
  """

  # Authenticate with Google Colab
  from google.colab import auth
  auth.authenticate_user()
  import gspread
  from gspread_dataframe import get_as_dataframe, set_with_dataframe
  from google.auth import default

  creds, _ = default()
  gc = gspread.authorize(creds)

  # Open the spreadsheet by URL
  try:
    spreadsheet = gc.open_by_url(sheet_url)
  except gspread.exceptions.SpreadsheetNotFound:
    spreadsheet = gc.create(sheet_name) # Creates a new spreadsheet if it doesn't exist
    spreadsheet.share('default', perm_type='anyone', role='writer') # Make it public

  # Select or create the worksheet
  try:
    worksheet = spreadsheet.worksheet(sheet_name)
  except gspread.exceptions.WorksheetNotFound:
    worksheet = spreadsheet.add_worksheet(title=sheet_name, rows=df.shape[0] + 1, cols=df.shape[1])

  # Write the DataFrame to the worksheet
  set_with_dataframe(worksheet, df, include_index=False, include_column_header=True, resize=True)

file_url = 'https://docs.google.com/spreadsheets/d/1Zz3e4QPMA4rStYARsrvF_Vxoz36f7OYfYIJchZXazAk/edit?gid=233684049#gid=233684049'

df = read_google_sheet(file_url)

print(df.head())

from google.colab import auth
auth.authenticate_user()
import gspread
from google.auth import default

# Revoke existing credentials
creds, _ = default()
creds.refresh(request)  # This will raise an exception, invalidating the credentials

"""# Sheet Operations"""

import pandas as pd
import numpy as np

def sample_sheet_data(sheet_url, sheet_name='Sheet1', p=0.1):
  """Reads a Google Sheet and returns a DataFrame with sampled rows.

  Args:
    sheet_url: The URL of the Google Sheet.
    sheet_name: The name of the worksheet to read from.
      Defaults to 'Sheet1'.
    p: The probability of retaining a row. Defaults to 0.1.

  Returns:
    A pandas DataFrame containing the sampled sheet data.
  """
  df = read_google_sheet(sheet_url, sheet_name)
  # Create a boolean mask for sampling
  mask = np.random.rand(len(df)) < p
  # Apply the mask to select rows
  sampled_df = df[mask]
  return sampled_df

# Samples 1/10 of the genes into a new sheet

file_url = "https://docs.google.com/spreadsheets/d/1m6x2s9Tagb7Y2J0dS2KzQ7DXVNPocBpGqJkx74a06-Y/edit?gid=622288382#gid=622288382"

df = read_google_sheet(file_url, "Processed_Data")
sample_df = sample_sheet_data(file_url, "Processed_Data", 0.1)
write_to_google_sheet(sample_df, file_url, "Sampled_Data_10")

import pandas as pd

# 1. Read the data from the Google Sheet
file_url = 'https://docs.google.com/spreadsheets/d/1Zz3e4QPMA4rStYARsrvF_Vxoz36f7OYfYIJchZXazAk/edit?gid=233684049#gid=233684049'
df = read_google_sheet(file_url)

# 2. Select the desired columns
selected_columns = ['gene_symbol', 'hgnc_id', 'disease_label', 'mondo_id']
new_df = df[selected_columns]

# 3. Check for duplicate hgnc_id and mondo_id pairs
duplicates = new_df[new_df.duplicated(subset=['hgnc_id', 'mondo_id'], keep=False)]
if not duplicates.empty:
  print("Duplicate hgnc_id and mondo_id pairs found:")
  print(duplicates[['hgnc_id', 'mondo_id']])
else:
  print("No duplicate hgnc_id and mondo_id pairs found.")

# 4. Write the new DataFrame to a new Google Sheet
# Create a new Google Sheet and get its URL (replace with your desired URL)
new_sheet_url = 'https://docs.google.com/spreadsheets/d/1m6x2s9Tagb7Y2J0dS2KzQ7DXVNPocBpGqJkx74a06-Y/edit?gid=0#gid=0'
write_to_google_sheet(new_df, new_sheet_url, sheet_name='Processed_Data')
print(f"Data written to: {new_sheet_url}")

file_url = 'https://docs.google.com/spreadsheets/d/1m6x2s9Tagb7Y2J0dS2KzQ7DXVNPocBpGqJkx74a06-Y/edit?gid=1214743318#gid=1214743318'

df = read_google_sheet(file_url, "testing")

print(df.head())

def gene_2_pheno(hgnc_id, mondo_id):
  """
  takes a gene and a disease and outputs the 4-vector
  """
  raise NotImplemented

OUTPUT_SHEET = "https://docs.google.com/spreadsheets/d/1m6x2s9Tagb7Y2J0dS2KzQ7DXVNPocBpGqJkx74a06-Y/edit?gid=992144994#gid=992144994"

def update_sheet(model, sheet, name, file_url=OUTPUT_SHEET):
  """
  add a new column with name using the function model 4-vector
  """
  # 1. Read the data from the Google Sheet
  df = read_google_sheet(file_url, sheet)

  # 2. Apply the model function to create the new column
  df[name] = df.apply(lambda row: model(row['hgnc_id'], row['mondo_id']), axis=1)

  # 3. Write the updated DataFrame back to the Google Sheet
  write_to_google_sheet(df, file_url, sheet)

def test_function(hgnc_id, mondo_id):
  return [1,2,3,4]

update_sheet(test_function, "processed_data_test", "test2")

import requests

def get_mondo_id(disease_name):
    # Define the OLS API endpoint for searching ontology terms
    api_url = "https://www.ebi.ac.uk/ols/api/search"
    # Set the parameters for the API request
    params = {
        "q": disease_name,  # Query with the disease name
        "ontology": "mondo",  # Search within the Mondo Disease Ontology
        "exact": "false"  # Perform an exact match search
    }
    # Send a GET request to the OLS API
    response = requests.get(api_url, params=params)
    # Raise an exception if the request was unsuccessful
    response.raise_for_status()
    # Parse the JSON response
    data = response.json()
    # Check if any terms were found
    if data["response"]["numFound"] > 0:
        # Retrieve the MONDO ID from the first search result
        mondo_id = data["response"]["docs"][0]["obo_id"]
        return mondo_id
    else:
        return None

# Test the function with the disease name "ABCD1-related adrenoleukodystrophy"
disease_name = "ABCD1-related adrenoleukodystrophy"
mondo_id = get_mondo_id(disease_name)
if mondo_id:
    print(f"The MONDO ID for '{disease_name}' is {mondo_id}.")
else:
    print(f"No MONDO ID found for '{disease_name}'.")

# Test the function with the disease name "ABCD1-related adrenoleukodystrophy"
disease_name = "X-linked cerebral adrenoleukodystrophy"
mondo_id = get_mondo_id(disease_name)
if mondo_id:
    print(f"The MONDO ID for '{disease_name}' is {mondo_id}.")
else:
    print(f"No MONDO ID found for '{disease_name}'.")

import requests

def get_mondo_term_data(mondo_id):
    """
    Fetch term details for a given MONDO ID using the OLS API.
    Returns synonyms and xrefs (cross-references).
    """
    base_url = f"https://www.ebi.ac.uk/ols/api/ontologies/mondo/terms/http%253A%252F%252Fpurl.obolibrary.org%252Fobo%252F{mondo_id.replace(':', '_')}"

    response = requests.get(base_url)

    if response.status_code != 200:
        print(f"Failed to fetch data for {mondo_id}")
        return None

    data = response.json()
    embedded = data.get('_embedded', {}).get('terms', [])

    if not embedded:
        print(f"No data found for {mondo_id}")
        return None

    term_data = embedded[0]  # Extract the first match
    synonyms = term_data.get('synonyms', [])
    xrefs = term_data.get('annotation', {}).get('database_cross_reference', [])

    return synonyms, xrefs


def check_mondo_equivalence(mondo_id1, mondo_id2):
    """
    Determines if two MONDO terms refer to the same disease by comparing
    synonyms and cross-references.
    """
    synonyms1, xrefs1 = get_mondo_term_data(mondo_id1) or ([], [])
    synonyms2, xrefs2 = get_mondo_term_data(mondo_id2) or ([], [])

    # Check for common synonyms
    common_synonyms = set(synonyms1).intersection(synonyms2)

    # Check for common database cross-references
    common_xrefs = set(xrefs1).intersection(xrefs2)

    if common_synonyms or common_xrefs:
        return True, common_synonyms, common_xrefs

    return False, [], []


# Example usage
mondo_id1 = 'MONDO:0018544'
mondo_id2 = 'MONDO:0010247'

equivalent, shared_synonyms, shared_xrefs = check_mondo_equivalence(mondo_id1, mondo_id2)

print(f"Are {mondo_id1} and {mondo_id2} equivalent? {equivalent}")
if shared_synonyms:
    print(f"Shared synonyms: {shared_synonyms}")
if shared_xrefs:
    print(f"Shared cross-references: {shared_xrefs}")