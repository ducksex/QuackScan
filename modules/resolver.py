import asyncio
import dns.resolver
from .utils import chunked


async def resolve_name(name: str):
    loop = asyncio.get_running_loop()
    try:
        result = await loop.run_in_executor(None, dns.resolver.resolve, name, 'A')
        return name, [r.to_text() for r in result]
    except Exception:
        return name, []

async def resolve_subdomains(domain, wordlist, concurrency):
    with open(wordlist) as f:
        subs = [line.strip() + '.' + domain for line in f if line.strip()]
    results = []
    sem = asyncio.Semaphore(concurrency)
    async def worker(name):
        async with sem:
            nm, addrs = await resolve_name(name)
            if addrs:
                results.append({'subdomain': nm, 'ips': addrs})
    await asyncio.gather(*(worker(s) for s in subs))
    return results
