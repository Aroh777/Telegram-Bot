from telethon import TelegramClient, events
import re

# Use your Bot Token here
bot_token = '7543946963:AAEc3UsZfPD2LzHp3RffVIAOHTX6U8qBPSE'

# Replace with your actual channel IDs
source_channel = -1002571426501  # Channel A
destination_channel = -1002746323155  # Channel B

# List of filter terms to skip
FILTER_TERMS = ["yash"]

# Your custom link to add (HTML formatted)
CUSTOM_LINK = '🔗 <a href="https://broker-qx.pro/sign-up/?lid=652808">Join Free VIP REGISTER HERE</a>'

# Create a bot client
client = TelegramClient(None, api_id=25601487, api_hash='9e9a5b8a58f866d49f3d997a87d73997').start(bot_token=bot_token)

def add_custom_link_if_otc(text):
    if re.search(r'\botc\b', text, flags=re.IGNORECASE):
        # Remove existing links
        text = re.sub(r'https?://\S+|t\.me/\S+', '', text)
        # Remove existing custom link line
        text = re.sub(r"(🔗\s*Join\s*Free\s*VIP\s*REGISTER\s*HERE.*)", '', text, flags=re.IGNORECASE)
        # Append custom link
        text = text.strip() + f"\n\n{CUSTOM_LINK}"
    return text.strip()

@client.on(events.NewMessage(chats=source_channel))
async def forward_message(event):
    message_text = event.message.message or ""

    # Skip filtered messages
    if any(term.lower() in message_text.lower() for term in FILTER_TERMS):
        print(f"Message skipped (filtered): {message_text[:50]}..." if message_text else "Message skipped (no text)")
        return

    # Update caption if needed
    updated_text = add_custom_link_if_otc(message_text)

    try:
        if event.message.media:
            # Forward media with updated caption
            await client.send_file(
                destination_channel,
                file=event.message.media,
                caption=updated_text if updated_text else None,
                parse_mode='html'
            )
        else:
            # Forward regular text message
            await client.send_message(destination_channel, updated_text, parse_mode='html')

        print(f"✅ Message forwarded: {updated_text[:50]}..." if updated_text else "✅ Media forwarded (no caption)")
    except Exception as e:
        print(f"❌ Failed to forward message: {e}")

async def main():
    print("✅ Bot is starting...")
    print(f"📌 Filtering messages containing: {', '.join(FILTER_TERMS)}")
    print("🤖 Bot is now running!")

client.loop.run_until_complete(main())
client.run_until_disconnected()
