from .functions import *

# Enable sheets api at: https://developers.google.com/sheets/api/quickstart/python
# Choose desktop app
# Download the client configuration file and place in the folder of this script

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']
ser = create_service(SCOPES)

# The ID and range of a sample spreadsheet.
SAMPLE_SPREADSHEET_ID = '1Y-ieLWMDzFzzeJKW-SygD90dBH80d4x0db8I3UFNj_c'

SHEET_NAME = 'חולים מאומתים/ישוב'
RANGE = 'A3:U'
SAMPLE_RANGE_NAME = f'{SHEET_NAME}!{RANGE}'

def main(outpath = None):

    SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']
    service = create_service(SCOPES)
    # Call the Sheets API
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                range=SAMPLE_RANGE_NAME).execute()

    df = values_to_df(result)

    if outpath:
        df.to_csv(outpath)
        retval = None
    else:
        retval = df

    return retval


if __name__ == '__main__':
    main()
