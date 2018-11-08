import asyncio
from pprint import pprint
from concurrent.futures import ProcessPoolExecutor
from bx import Bx


async def _fetch_balance(addresses):
    print('_fetch_balance')
    loop = asyncio.get_running_loop()

    coros = [
        Bx.fetch_balance(address, f='json')
        for address in addresses
    ]

    d, p = await asyncio.wait(coros, loop=loop)
    d = [n.result() for n in d]
    return d


def fetch_balance(addresses):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    future = loop.run_until_complete(_fetch_balance(addresses))
    loop.close()
    return future


async def main():
    N = 1_000
    M = 100
    addresses = ['13CxJjFzG5C7qawLHjAzr3ykV2p277yrCJ' for i in range(N)]
    results = []
    loop = asyncio.get_running_loop()

    with ProcessPoolExecutor() as pool:
        coros = []

        for i in range(0, len(addresses), M):    
            coro = loop.run_in_executor(pool, fetch_balance, addresses[i:i + M])
            coros.append(coro)
        
        for coro in asyncio.as_completed(coros):
            rs = await coro
            results.extend(rs)

    pprint(results)


asyncio.run(main())
