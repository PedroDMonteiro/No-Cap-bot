from io import BytesIO
from discord import File
import requests
import aiohttp


async def get_file_from_url(url: str,name: str)-> File:
    async with aiohttp.ClientSession().get(url) as response:
        buffer = BytesIO(response.content)
        return File(fp=buffer,filename=name)

async def save_url(url: str, path: str) -> bool:
    async with aiohttp.ClientSession().get(url) as response:
        buffer = BytesIO(response.content)
        with open(path, "wb") as binary_file:
            binary_file.write(buffer.getvalue())
