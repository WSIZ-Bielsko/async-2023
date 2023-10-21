from asyncio import run, sleep

import aiohttp


async def check_service(url: str, must_contain_text: str) -> bool:
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                response_text = await resp.text()
                # print(response_text)
                if must_contain_text:
                    return must_contain_text in response_text
                else:
                    return True
    except Exception as e:
        return False


async def main():
    # async with session.get(f'https://www.wsi.edu.pl') as resp:
    # async with session.get(f'https://doha.wsi.edu.pl/uploader') as resp:

    while True:
        val = await check_service(url='https://www.wsi.edu.pl', must_contain_text='Wyższa Szkoła')
        print(val)
        val = await check_service(url='https://doha.wsi.edu.pl/uploader', must_contain_text='WSIZ Uploader')
        print(val)
        await sleep(10)


if __name__ == '__main__':
    run(main())
