from io import BytesIO
from discord import File
import requests
import aiohttp

class Utils:
    async def get_file_from_url(url: str,name: str)-> File:
        async with aiohttp.ClientSession().get(url) as response:
            buffer = BytesIO(response.content)
            return File(fp=buffer,filename=name)

    async def save_url(url: str, path: str) -> bool:
        async with aiohttp.ClientSession().get(url) as response:
            buffer = BytesIO(response.content)
            with open(path, "wb") as binary_file:
                binary_file.write(buffer.getvalue())

    def is_iterable(obj: any) -> bool:
        try:
            iter(obj)
            return True
        except Exception as err:
            return False
    
    # return Ah Bm Cs
    def format_seconds(seconds: int) -> str:
        hours = int((seconds - seconds%3600)/3600)
        minutes = int((seconds%3600 - seconds%60)/60)
        seconds = seconds%60

        t = ""
        if hours:
            t += f"{hours:02}h "
            
        if minutes or hours:
            t += f"{minutes:02}m "
            
        t += f"{seconds:02}s"
        
        return t
