import aiohttp
from pyrogram import filters
from DAXXMUSIC import app


@app.on_message(filters.command("ip"))
async def ip_info(_, message):
    if len(message.command) != 2:
        return await message.reply_text(
            "❌ **Invalid Usage**\n\n"
            "Please provide an IP address.\n"
            "**Example:** `/ip 8.8.8.8`",
            quote=True,
        )

    ip_address = message.command[1]

    url = f"https://api.safone.dev/ipinfo?ip={ip_address}"

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, timeout=10) as resp:
                if resp.status != 200:
                    return await message.reply_text(
                        "❌ Unable to fetch IP information right now.",
                        quote=True,
                    )

                data = await resp.json()

        info = (
            f"🌐 **IP Information**\n\n"
            f"**IP:** `{data.get('ip', 'N/A')}`\n"
            f"**Country:** {data.get('country', 'N/A')}\n"
            f"**City:** {data.get('city', 'N/A')}\n"
            f"**ISP:** {data.get('isp', 'N/A')}\n\n"
            f"🔍 _Fetched by @kira_probot"
        )

        await message.reply_text(info, quote=True)

    except aiohttp.ClientError:
        await message.reply_text(
            "❌ Network error occurred while fetching IP details.",
            quote=True,
        )
    except Exception:
        await message.reply_text(
            "❌ Failed to fetch IP information.",
            quote=True,
        )
