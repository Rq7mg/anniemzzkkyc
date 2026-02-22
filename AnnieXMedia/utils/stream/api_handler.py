import aiohttp
import config

async def get_video_from_api(youtube_id):
    user_api = getattr(config, "VIDEO_API_URL", None)
    apis = []
    if user_api:
        base_api = user_api.rstrip("/")
        apis.append(f"{base_api}/yt?link=https://www.youtube.com/watch?v={youtube_id}")
    
    apis.extend([
        f"https://api.youtubify.com/download?url={youtube_id}",
        f"https://api.youtubify.com/download?url=https://www.youtube.com/watch?v={youtube_id}",
        f"https://fallen-api.vercel.app/api/yt?url=https://www.youtube.com/watch?v={youtube_id}"
    ])
    
    async with aiohttp.ClientSession() as session:
        for api_url in apis:
            try:
                async with session.get(api_url, timeout=8) as response:
                    if response.status == 200:
                        data = await response.json()
                        res_url = data.get("url") or data.get("link") or (data.get("data", {}).get("url") if isinstance(data.get("data"), dict) else None)
                        if res_url:
                            return res_url
            except Exception:
                continue
    return None
