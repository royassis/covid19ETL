from settings import *
import urllib.request
import pandas as pd
import json
import os

def main(outdir=None):
    print(__file__, 'is running')
    RECORDS_LIMIT = 10000000

    df = pd.read_csv(GOV_RESOURCE_PATH)

    df['datastore_structure'] = df['resource_id'].apply(lambda x: {'resource_id': x,'limit':RECORDS_LIMIT})\
                                            .apply(lambda x: str.encode(json.dumps(x)))

    dfs_files = []
    for _, entry in df.iterrows():
        response  = urllib.request.urlopen(entry["url"], entry['datastore_structure'])
        s = json.loads(response.read())
        records = s["result"]["records"]

        data = pd.DataFrame(records).set_index("_id")

        outfile = ".".join([entry['name'], 'csv'])
        # outpath = os.path.join(GOV_DATA_PATH, outfile)
        dfs_files.append([data,outfile])

    if outdir:
        for df_file in dfs_files:
            df = df_file[0]
            filename = df_file[1]
            fullpath = os.path.join(outdir, filename)
            df.to_csv(fullpath)
        retval = None

    else:
        retval = dfs_files
    return retval

if __name__ == '__main__':
    main()
