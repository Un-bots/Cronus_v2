import asyncio
from pyrogram import filters, enums
from pyrogram.enums import ChatMemberStatus
from pyrogram.errors import FloodWait
from DAXXMUSIC import app

chatQueue = []
stopProcess = False


def is_admin(member):
    return member.status in (
        ChatMemberStatus.ADMINISTRATOR,
        ChatMemberStatus.OWNER,
    )


# ---------------- ZOMBIES CLEAN ---------------- #

@app.on_message(filters.command(["zombies", "clean"]))
async def remove_deleted(_, message):
    global stopProcess

    try:
        user = await app.get_chat_member(message.chat.id, message.from_user.id)
        if not is_admin(user):
            return await message.reply("👮🏻 | ᴏɴʟʏ ᴀᴅᴍɪɴs ᴄᴀɴ ᴜsᴇ ᴛʜɪs ᴄᴏᴍᴍᴀɴᴅ.")

        bot = await app.get_chat_member(message.chat.id, app.id)
        if not is_admin(bot):
            return await message.reply("❌ | ɪ ɴᴇᴇᴅ ᴀᴅᴍɪɴ ʀɪɢʜᴛs ᴛᴏ ᴄʟᴇᴀɴ ᴅᴇʟᴇᴛᴇᴅ ᴜsᴇʀs.")

        if message.chat.id in chatQueue:
            return await message.reply("⏳ | ᴄʟᴇᴀɴᴜᴘ ᴀʟʀᴇᴀᴅʏ ʀᴜɴɴɪɴɢ ʜᴇʀᴇ. ᴜsᴇ /sᴛᴏᴘ ᴛᴏ ᴄᴀɴᴄᴇʟ.")

        if len(chatQueue) >= 30:
            return await message.reply("🚫 | ᴍᴀxɪᴍᴜᴍ ᴀᴄᴛɪᴠᴇ ᴄʟᴇᴀɴᴜᴘs ʀᴇᴀᴄʜᴇᴅ. ᴛʀʏ ʟᴀᴛᴇʀ.")

        chatQueue.append(message.chat.id)
        deleted = []

        async for member in app.get_chat_members(message.chat.id):
            if member.user.is_deleted:
                deleted.append(member.user)

        if not deleted:
            chatQueue.remove(message.chat.id)
            return await message.reply("✅ | ɴᴏ ᴅᴇʟᴇᴛᴇᴅ ᴀᴄᴄᴏᴜɴᴛs ғᴏᴜɴᴅ.")

        msg = await message.reply(
            f"🧹 | ғᴏᴜɴᴅ {len(deleted)} ᴅᴇʟᴇᴛᴇᴅ ᴀᴄᴄᴏᴜɴᴛs.\n⏳ | ᴄʟᴇᴀɴɪɴɢ sᴛᴀʀᴛᴇᴅ..."
        )

        count = 0
        stopProcess = False

        for user in deleted:
            if stopProcess:
                break
            try:
                await app.ban_chat_member(message.chat.id, user.id)
                count += 1
                await asyncio.sleep(10)
            except:
                pass

        await msg.delete()
        await message.reply(f"✅ | ʀᴇᴍᴏᴠᴇᴅ {count} ᴅᴇʟᴇᴛᴇᴅ ᴀᴄᴄᴏᴜɴᴛs.")
        chatQueue.remove(message.chat.id)

    except FloodWait as e:
        await asyncio.sleep(e.value)


# ---------------- STOP ---------------- #

@app.on_message(filters.command("stop"))
async def stop_clean(_, message):
    global stopProcess
    stopProcess = True
    await message.reply("🛑 | ᴄʟᴇᴀɴᴜᴘ ᴘʀᴏᴄᴇss sᴛᴏᴘᴘᴇᴅ.")


# ---------------- ADMINS LIST ---------------- #

@app.on_message(filters.command(["admins", "staff"]))
async def admins(_, message):
    text = f"👥 ɢʀᴏᴜᴘ sᴛᴀғғ – {message.chat.title}\n\n"

    async for member in app.get_chat_members(
        message.chat.id, filter=enums.ChatMembersFilter.ADMINISTRATORS
    ):
        if member.user.is_bot:
            continue
        if member.status == ChatMemberStatus.OWNER:
            text += f"👑 ᴏᴡɴᴇʀ : {member.user.mention}\n"
        else:
            text += f"👮 ᴀᴅᴍɪɴ : {member.user.mention}\n"

    await message.reply(text)


# ---------------- BOTS LIST ---------------- #

@app.on_message(filters.command("bots"))
async def bots(_, message):
    bots = []
    async for member in app.get_chat_members(
        message.chat.id, filter=enums.ChatMembersFilter.BOTS
    ):
        bots.append(member.user.username)

    if not bots:
        return await message.reply("🤖 | ɴᴏ ʙᴏᴛs ғᴏᴜɴᴅ.")

    text = "🤖 ʙᴏᴛs ɪɴ ᴛʜɪs ɢʀᴏᴜᴘ :\n\n"
    text += "\n".join(f"• @{b}" for b in bots if b)
    text += f"\n\nᴛᴏᴛᴀʟ : {len(bots)}"

    await message.reply(text)
