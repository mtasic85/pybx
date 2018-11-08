import sys
import json
import asyncio


class BxError(BaseException):
    pass


async def run(argv):
    cmd = ' '.join(argv)
    loop = asyncio.get_running_loop()
    
    proc = await asyncio.create_subprocess_shell(
        cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
        loop=loop,
    )

    stdout, stderr = await proc.communicate()
    return stdout, stderr


async def bx_command(bx_subcmd, *args, **kwargs):
    # fix bx sub command
    bx_subcmd = bx_subcmd.replace('_', '-')
    # fix kwargs
    kwargs = [f'-{k} {v}' for k, v in kwargs.items()]
    
    # pack bx args in correct order
    argv = ['bx', bx_subcmd, *kwargs, *args]

    # execute
    stdout, stderr = await run(argv)
    stdout = stdout.decode()
    stderr = stderr.decode()

    if stderr:
        raise BxError(stderr)

    try:
        r = json.loads(stdout)
    except ValueError as e:
        r = stdout

    return r


class _Bx:
    def __init__(self):
        pass


    def __getattr__(self, attr):
        f = lambda *args, **kwargs: bx_command(attr, *args, **kwargs)
        return f


Bx = _Bx()


if __name__ == '__main__':
    coro = run(sys.argv[1:])
    asyncio.run(coro)
