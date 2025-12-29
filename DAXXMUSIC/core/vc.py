import asyncio
from pytgcalls import PyTgCalls
from pytgcalls.types.input_stream import (
    AudioPiped,
    AudioVideoPiped,
)
from pytgcalls.types.input_stream.quality import (
    HighQualityAudio,
    MediumQualityVideo,
)
from pyrogram import Client

class VoiceCall:
    def __init__(self, app: Client):
        self.app = app
        self.call = PyTgCalls(app)
        self.active_chats = set()

    async def start(self):
        await self.call.start()
        print("🎧 VC engine started")

    async def join_audio(self, chat_id: int, stream_url: str):
        await self.call.join_group_call(
            chat_id,
            AudioPiped(
                stream_url,
                HighQualityAudio(),
            ),
        )
        self.active_chats.add(chat_id)

    async def join_video(self, chat_id: int, stream_url: str):
        await self.call.join_group_call(
            chat_id,
            AudioVideoPiped(
                stream_url,
                HighQualityAudio(),
                MediumQualityVideo(),
            ),
        )
        self.active_chats.add(chat_id)

    async def leave(self, chat_id: int):
        if chat_id in self.active_chats:
            await self.call.leave_group_call(chat_id)
            self.active_chats.remove(chat_id)
