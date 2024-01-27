import asyncio
from asyncio import run


async def main():
    rd, wr = await asyncio.open_connection('wsi.edu.pl', 443, ssl=True, ssl_handshake_timeout=0.2)
    print('opened')
    # app_state = await rd.read(100)
    # print('read: ', app_state.decode())
    # wr.close()
    # await wr.wait_closed()


if __name__ == '__main__':
    run(main())
