import asyncio
from pprint import pprint
from bx import Bx


async def _fetch_balance(addresses):
    coros = [
        Bx.fetch_balance(address, f='json')
        for address in addresses
    ]

    d, p = await asyncio.wait(coros)
    return d, p


async def main():
    N = 1_000
    M = 100
    addresses = ['13CxJjFzG5C7qawLHjAzr3ykV2p277yrCJ' for i in range(N)]
    done = []
    pending = []
    loop = asyncio.get_running_loop()

    for i in range(0, len(addresses), M):
        d, p = await _fetch_balance(addresses[i:i + M])
        done.extend(d)
        pending.extend(p)

    results = [n.result() for n in done]
    pprint(results)


asyncio.run(main())
