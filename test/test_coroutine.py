import aiohttp
import asyncio

async def send_request(i):
    print('当前是第%s个协程' % (i+1))
    url = 'https://httpbin.org/get'
    param = {
        'index': i,
    }
    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=param) as response:
            print(await response.text())

if __name__ == '__main__':
    tasks = []
    loop = asyncio.get_event_loop()
    for i in range(10):
        task = asyncio.ensure_future(send_request(i))
        tasks.append(task)
    loop.run_until_complete(asyncio.wait(tasks))