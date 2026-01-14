# kurwy api wyłączyli
tenor_urls = [
    "https://tenor.com/view/speech-bubble-sticker-gif-11167073420346215522",
    "https://tenor.com/view/speech-bubble-gif-25355282",
    "https://tenor.com/view/rock-discord-speech-bubble-chat-bubble-indoor-gif-11796528907649782685",
    "https://tenor.com/view/boy-kisser-gif-275689654530739008",
    "https://tenor.com/view/boy-kiss-er-gif-8460759050764009590",
    "https://tenor.com/view/sigma-boy-gif-7111495482624159509",
    "https://tenor.com/view/lache-moi-bulle-chat-gif-15817423430329387709",
    "https://tenor.com/view/cute-speech-bubble-gif-1071349457091991916",
    "https://tenor.com/view/speech-bubble-gif-16678730642182240634",
    "https://tenor.com/view/old-man-ai-generated-meme-funny-transparent-gif-15501244949052344496",
    "https://tenor.com/view/reaction-gif-6058430764022399046",
    "https://tenor.com/view/speech-bubble-zesty-gif-5226080315601189252",
    "https://tenor.com/view/speech-bubble-angry-birds-discord-gif-5080697591851033272",
    "https://tenor.com/view/zayle-6-gif-4207490283154963518",
    "https://tenor.com/view/speech-bubble-gif-7968118555005578949",
    "https://tenor.com/view/speech-bubble-boykisser-gif-1584602926298665747",
    "https://tenor.com/view/baldis-basics-speech-bubble-meme-black-guy-gif-16213112242897221020",
    "https://tenor.com/view/fish-fish-kiss-kiss-chat-bubble-discord-gif-27600133",
    "https://tenor.com/view/speech-bubble-discord-discord-mod-funny-discord-meme-gif-14339557102693950415",
    "https://tenor.com/view/speech-bubble-bunny-gif-26425903",
        ]

import aiohttp
from bs4 import BeautifulSoup

async def get_tenor_gif(search_term: str) -> str:
    url = f"https://tenor.com/search/{search_term}-gifs"

    async with aiohttp.ClientSession() as session:
            html = await (await session.get(url)).text()

    soup = BeautifulSoup(html, "html.parser")
    gifs = []

    for img in soup.find_all("img"):
        src = img.get("src")
        if src and src.endswith(".gif"):
            gifs.append(src)

    return random.choice(gifs) if gifs else None

