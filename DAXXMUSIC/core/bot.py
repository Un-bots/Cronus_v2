from pyrogram import Client, errors
from pyrogram.enums import ChatMemberStatus

import asyncio
import config
from ..logging import LOGGER


class DAXX(Client):
    def __init__(self):
        LOGGER(__name__).info("Starting Bot...")
        super().__init__(
            name="KIRA",
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            bot_token=config.BOT_TOKEN,
            in_memory=True,
            max_concurrent_transmissions=7,
        )

    async def start(self):
        await super().start()

        # ===== BOT INFO =====
        self.id = self.me.id
        self.name = f"{self.me.first_name} {self.me.last_name or ''}".strip()
        self.username = self.me.username
        self.mention = self.me.mention

        # ===== SEND START MESSAGE (RETRY + FLOODWAIT SAFE) =====
        if config.LOGGER_ID:
            for _ in range(5):
                try:
                    await self.send_message(
                        chat_id=config.LOGGER_ID,
                        text=(
                            f"<u><b>» {self.mention} ʙᴏᴛ sᴛᴀʀᴛᴇᴅ :</b></u>\n\n"
                            f"ɪᴅ : <code>{self.id}</code>\n"
                            f"ɴᴀᴍᴇ : {self.name}\n"
                            f"ᴜsᴇʀɴᴀᴍᴇ : @{self.username}"
                        ),
                    )
                    break
                except errors.FloodWait as e:
                    await asyncio.sleep(e.value)
                except (errors.ChannelInvalid, errors.PeerIdInvalid):
                    LOGGER(__name__).error(
                        "Bot cannot access the log group/channel. "
                        "Add the bot to LOGGER_ID and give permission."
                    )
                    break
                except Exception as ex:
                    LOGGER(__name__).warning(
                        f"Log message retry failed: {type(ex).__name__}"
                    )
                    await asyncio.sleep(2)

        # ===== ADMIN CHECK (NO HARD EXIT) =====
        try:
            member = await self.get_chat_member(config.LOGGER_ID, self.id)
            if member.status != ChatMemberStatus.ADMINISTRATOR:
                LOGGER(__name__).error(
                    "Bot is not ADMIN in the log group/channel. Please promote it."
                )
        except Exception as ex:
            LOGGER(__name__).warning(
                f"Admin check skipped: {type(ex).__name__}"
            )

        LOGGER(__name__).info(f"Music Bot Started as {self.name}")

    async def stop(self):
        LOGGER(__name__).info("Stopping Bot...")
        await super().stop()
