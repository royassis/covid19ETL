from ETL_scripts.extract_worldmeter.extract_worldmeter_data import main as extract_worldmeter_data
from ETL_scripts.extract_gov_data import main as extract_gov_data
from ETL_scripts.transform_worldmeter_data import main as transform_worldmeter_data

extract_worldmeter_data()
transform_worldmeter_data()
extract_gov_data()

