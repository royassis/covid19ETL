from aiohttp import ClientSession
import asyncio
import re
import pandas as pd
from datetime import datetime
from ETL_scripts.extract_worldmeter.settings import  *
import time
import aiohttp


async def fetch_html(url: str, session: ClientSession, **kwargs) -> str:
    resp = await session.request(method="GET", url=url, **kwargs)
    resp.raise_for_status()
    html = await resp.text()
    return html

async def to_file(url,session,i,urls_len) -> None:

    logger.info(f'sending get request to file {i+1} from {urls_len}')
    try:
        html = await fetch_html(url,session)
    except (
            aiohttp.ClientError,
            aiohttp.http_exceptions.HttpProcessingError,
    ) as e:
        logger.error(
            "aiohttp exception for %s [%s]: %s",
            url,
            getattr(e, "status", None),
            getattr(e, "message", None),
        )
        return None
    except Exception as e:
        logger.exception(
            "Non-aiohttp exception occured:  %s", getattr(e, "__dict__", {})
        )
        return None

    else:
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
    conn = aiohttp.TCPConnector(limit=10)
    urls_len = len(urls)
    async with ClientSession(connector=conn) as session:
        tasks = []
        for i,url in enumerate(urls):
            tasks.append(
                to_file(url=url, session=session, i=i, urls_len= urls_len, **kwargs)
            )
        await asyncio.gather(*tasks)

def main(urls):

    s = time.perf_counter()
    asyncio.run(bulk_crawl_and_write(urls=urls))
    elapsed = time.perf_counter() - s
    print(f"{__file__} executed in {elapsed:0.2f} seconds.")

if __name__ == '__main__':
    main()







