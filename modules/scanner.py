import asyncio
import httpx
from .utils import chunked


async def fetch(client, sub):
    url = f'https://{sub["subdomain"]}'
    try:
        resp = await client.get(url, timeout=10)
        sub['status'] = resp.status_code
        sub['title'] = resp.text.split('<title>')[1].split('</title>')[0] if '<title>' in resp.text else ''
    except Exception:
        sub['status'] = None
        sub['title'] = ''
    return sub

async def scan_http(subs, concurrency):
    results = []
    sem = asyncio.Semaphore(concurrency)
    async with httpx.AsyncClient(follow_redirects=True) as client:
        async def work(sub):
            async with sem:
                results.append(await fetch(client, sub))
        await asyncio.gather(*(work(s) for s in subs))
    return results
