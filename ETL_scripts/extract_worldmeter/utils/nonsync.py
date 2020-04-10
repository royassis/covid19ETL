from aiohttp import ClientSession
import asyncio
import re
import pandas as pd
from datetime import datetime
from ETL_scripts.extract_worldmeter.settings import  *



async def fetch_html(url: str, session: ClientSession, **kwargs) -> str:
    """GET request wrapper to fetch page HTML.

    kwargs are passed to `session.request()`.
    """
    resp = await session.request(method="GET", url=url, **kwargs)
    resp.raise_for_status()
    html = await resp.text()
    return html

async def to_file(url,session) -> None:

    html = await fetch_html(url,session)

    container = pd.read_html(html, match=READ_HTML_MATCH_PARAM)
    df = container[-1]
    df['ref'] = url
    date_str = re.search('\d{8}', url).group()
    date_obj = datetime.strptime(date_str, '%Y%m%d')
    df['date'] = date_obj

    date_repr_to_file = date_obj.strftime('%b-%d-%Y')

    outfile = date_repr_to_file + '.csv'
    outpath = os.path.join(OUTPUT_PATH, outfile)
    df.to_csv(outpath)


async def bulk_crawl_and_write( urls: list, **kwargs) -> None:
    """Crawl & write concurrently to `file` for multiple `urls`."""
    async with ClientSession() as session:
        tasks = []
        for url in urls:
            tasks.append(
                to_file(url=url, session=session, **kwargs)
            )
        await asyncio.gather(*tasks)

def main(urls):
    asyncio.run(bulk_crawl_and_write(urls=urls))

if __name__ == '__main__':
    main()