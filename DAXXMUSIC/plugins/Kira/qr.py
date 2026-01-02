from pyrogram import Client, filters
from pyrogram.types import Message
import qrcode
from DAXXMUSIC import app
import io


# Function to create a QR code
def generate_qr_code(text):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(text)
    qr.make(fit=True)

    img = qr.make_image(fill_color="white", back_color="black")

    # Save the QR code to bytes
    img_bytes = io.BytesIO()
    img.save(img_bytes, format="PNG")
    img_bytes.seek(0)
    return img_bytes


@app.on_message(filters.command("qr"))
def qr_handler(client: Client, message: Message):
    if len(message.command) < 2:
        return message.reply_text(
            "❌ **ᴜsᴀɢᴇ:**\n`/qr <ᴛᴇxᴛ ᴏʀ ʟɪɴᴋ>`\n\n"
            "Example:\n`/qr https://google.com`",
            quote=True,
        )

    input_text = " ".join(message.command[1:])
    qr_image = generate_qr_code(input_text)

    message.reply_photo(
        qr_image,
        caption=(
            "📌 **ǫʀ ᴄᴏᴅᴇ ɢᴇɴᴇʀᴀᴛᴇᴅ**\n\n"
            f"🔗 `{input_text}`\n\n"
            "✨ ɢᴇɴᴇʀᴀᴛᴇᴅ ʙʏ @kira_probot"
        ),
    )
