from ETL_scripts.extract_worldmeter.extract_worldmeter_data import main as extract_worldmeter_data
from ETL_scripts.transform_worldmeter_data import main as transform_worldmeter_data
from ETL_scripts.extract_gov_data import main as extract_gov_data
from ETL_scripts.extract_gsheets.covid19sheets import main as extract_sheet_data

DATA_DIR = r'D:\PycharmProjects\covid19ETL\DW\raw_data\worldmeter'
CUTOFF_DATE = '2020-02-10'

extract_worldmeter_data(DATA_DIR)
transform_worldmeter_data(DATA_DIR,cutoffdate = CUTOFF_DATE)
a=extract_gov_data(r'D:\PycharmProjects\covid19ETL\DW\raw_data\gov_data')
extract_sheet_data(r'D:\PycharmProjects\covid19ETL\DW\raw_data\gov_data')

