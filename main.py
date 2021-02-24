import asyncio
import aiohttp
import json



async def get_json(client, url):
    async with client.get(url) as response:
        assert response.status == 200
        return await response.read()

async def get_reddit_top(subreddit, client):
    url = f"https://www.reddit.com/r/{subreddit}/top.json?sort=top&t=day&limit=5"
    data = await get_json(client, url)

    j = json.loads(data.decode('utf-8'))
    for i in j['data']['children']:
        score = i['data']['score']
        title = i['data']['title']
        link = i['data']['url']
        print(f"{score}: {title} ({link})")
    
    print(f"Done: {subreddit}")

async def get_reddits(loop):  
    client = aiohttp.ClientSession(loop=loop)

    python_task = asyncio.create_task(get_reddit_top('python', client))
    programming_task = asyncio.create_task(get_reddit_top('programming', client))
    conservative_task = asyncio.create_task(get_reddit_top('conservative', client))

    await python_task
    await programming_task
    await conservative_task

    await client.close() 

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    

    # asyncio.ensure_future(get_reddit_top('python', client))
    # asyncio.ensure_future(get_reddit_top('programming', client))
    # asyncio.ensure_future(get_reddit_top('conservative', client))

    # loop.run_forever()

    # asyncio.ensure_future(get_reddit_top('python', client))
    # asyncio.ensure_future(get_reddit_top('programming', client))
    # asyncio.ensure_future(get_reddit_top('conservative', client))

    loop.run_until_complete(get_reddits(loop))
    loop.stop()
    # client.close()

    print('done')