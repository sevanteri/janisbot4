from janisbot4.api.quote_api import get_random_quote

REGEXP = ".*:$"


async def index(message):
    await message.reply(get_random_quote(), reply=False)
