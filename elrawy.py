import asyncio
import nest_asyncio
import schedule
import time
from telethon import TelegramClient
from telethon.errors import SessionPasswordNeededError, FloodWaitError

# Allow nesting of event loops
nest_asyncio.apply()

# Replace with your Telegram API ID and API hash
api_id = '29686695'
api_hash = '127b00ff9bc362284fcafc2587ac066a'

# Initialize Telethon client
client = TelegramClient('test1', api_id, api_hash)

static_keywords = [
    'banknxteg', ' aib ', ' efg ', '.com.sa',
    'egypt', 'cairo', 'misr', ' nbe ', ' cib ', ' qnb ', ' alahly ',
    'fawry', 'efinance', 'saudi', ' ksa ', ' sdif ', ' SAMA ',
    'arab', 'arab bank', 'national commercial bank', 'rajhi',
    'faisal', 'sabb', 'riyad bank', ' bsf ', 'alinma',
    'albilad', 'bank albilad', 'albaraka', 'mashreq',
    'emirates', ' uae ', 'hsbc', 'citibank',
    'hajj', 'mecca', 'riyadh', 'dammam', 'jeddah',
    'vision 2030', 'arab national bank',
    'egfincirt', ' cbe ', 'myegbank', ' bdc ', 'du caire',
    'scbank', '.eg', '.com.eg', '.gov.sa', '.gov.eg',
    'alahlybank', 'cibeg.com', 'ahliunited.com', 'bankaudi.com.eg',
    'bank-abc', 'banquemisr', 'bmonline',
    'faisalbank', 'hsbc', 'qnbalahli', 'scbank'
]

channel_ids = ['breachdetector', 'ransomlook', 'RansomFeedNews', 'TheDarkWebInformer',
               'cyberthint', 'yildizthreatnews', 'RansomwareNewsVX', 'ransomwarelive', 'Venari_By_BetterCyber']

forward_channel_id = 'ElrawyDM1'  # Replace with the actual ID of the channel to forward to

async def is_message_identical(message_text):
    """Check if the message text already exists in the forward channel."""
    messages = await client.get_messages(forward_channel_id, limit=500)
    for msg in messages:
        if msg.text and message_text.lower() in msg.text.lower():
            return True
    return False

async def search_and_alert(channel_id):
    """Search for static keywords in messages from a specific channel."""
    try:
        messages = await client.get_messages(channel_id, limit=500)
        for message in messages:
            if message.text:
                for keyword in static_keywords:
                    if keyword.lower() in message.text.lower():
                        if not await is_message_identical(message.text):
                            await client.send_message(forward_channel_id,
                                                       f"===> Keyword [{keyword}] Found : === \n {message.text}")
                            await asyncio.sleep(5)  # Delay after sending a message
                        break
    except FloodWaitError as e:
        print(f"Rate limit hit. Waiting for {e.seconds} seconds.")
        await asyncio.sleep(e.seconds)
    except Exception as e:
        print(f"Error while searching in channel {channel_id}: {e}")

async def run_tasks():
    """Run the search and alert tasks for all channels."""
    async with client:
        for channel_id in channel_ids:
            await search_and_alert(channel_id)
            await asyncio.sleep(5)  # Pause between channel searches

def job():
    """Scheduled job to run every 5 hours."""
    print("Running scheduled job...")
    asyncio.run(run_tasks())

if __name__ == "__main__":
    # Schedule the job to run every 5 hours
    schedule.every(1).seconds.do(job)
    # Keep the script running
    while True:
        schedule.run_pending()
        time.sleep(1)
