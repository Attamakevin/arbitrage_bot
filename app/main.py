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
TOKEN = '6898409938:AAE52Sl5huP7kE-t3AKZHrZ45ky3PO40a9Q'
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start_command(message):
    chat_id = message.chat.id
    buttons = [
        types.InlineKeyboardButton("💹 Start DCK Arbitrage", callback_data='arbitrade'),
        types.InlineKeyboardButton("📊 Token Analytics", url='https://t.me/Dex_checkTradingBot/Coin_Analytics'),
	types.InlineKeyboardButton("❓ Help", callback_data='help'),
    ]

    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(*buttons)

    bot.send_message(
        chat_id,
        "Dexcheck Trading Bot | Website\n\n"
        " Welcome to DexCheckArbitrage!\n\n"
        "Elevate Your Profits! 🚀\n"

        "Unlock Smart Trading, Maximize Gains.\n"

        "✨ Automated Profits, 24/7 Analysis.\n"
        "🌐 Diverse Cryptos, Seamless Trading.\n"
        "🚀 User-Friendly Interface.\n"
        "🔒 Secure & Transparent.\n"

        "Ready to Elevate? Sign up Now!\n\n"

        "Trade Smart. Profit Smarter.\n"
        "<b>Select chain below to get started</b>\n",
        reply_markup=keyboard,
        parse_mode='HTML'
    )

@bot.callback_query_handler(func=lambda call: True)
def button_click(call):
    try:
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
        elif button_data == 'withdraw':
            withdraw_command(call.message)
        elif button_data == 'authenticator':
             authentication(call.message)
        elif button_data == 'send_message':
            message_support(call.message)
        elif button_data == 'bsc':
            check_balance_command(call.message)
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
            callback_query(call.message)
        print("Update processed successfully.")
    except Exception as e:
        print(f"Error in button_click: {e}")

# Add this function to handle the 'done' action
def done_action(message):
    # Handle the 'done' action here
    bot.send_message(message.chat.id, "You clicked 'Done Connecting'.")
support_chats = {}
@bot.message_handler(commands=['contact_support'])
def message_support(message):
    chat_id = message.chat.id
    user_id = message.from_user.id

    # Check if the user already initiated a support chat
    if user_id in support_chats:
        bot.send_message(chat_id, "You're already in contact with support.")
    else:
        # Create a new private chat with support
        support_message = (
            "🆘 <b>User Needs Support</b> 🆘\n"
            f"User: {html.escape(message.from_user.first_name)} (@{message.from_user.username})\n"
            f"Chat ID: {message.chat.id}\n"
            "Please provide assistance."
        )

        # Create a temporary support chat ID
        support_chat_id = -user_id

        # Store the support chat ID in the dictionary
        support_chats[user_id] = support_chat_id

        # Inform the user that their request has been sent to support
        bot.send_message(chat_id, "Your support request has been sent. Assistance will be provided shortly.")

        # Send the support message to the temporary chat ID
        bot.send_message(support_chat_id, support_message, parse_mode='HTML')

# This command can be used by support to reply to users
@bot.message_handler(func=lambda message: message.chat.id in support_chats.values())
def support_reply(message):
    # Extract the user ID corresponding to the support chat
    user_id = [k for k, v in support_chats.items() if v == message.chat.id][0]

    # Reply to the user
    bot.send_message(user_id, f"Support: {message.text}")
@bot.message_handler(commands=['help_command'])
def help_command(message):
    # Generate the "Contact Support" button dynamically
    support_button = types.InlineKeyboardButton(text='📩 Contact Support', url='https://t.me/kelvinejike')
    back_to_main_menu_button = types.InlineKeyboardButton("⬅️ Back to Main Menu", callback_data='start')
    reply_markup = types.InlineKeyboardMarkup([[support_button, back_to_main_menu_button]])
    
    # Reply to the user with the "Help" message and the "Contact Support" button
    bot.send_message(chat_id=message.chat.id, text=" Help ❓ Have questions? We're here to assist you!", reply_markup=reply_markup)


def create_switch_chain_button():
    return types.InlineKeyboardButton("Switch Chain", callback_data='start')

def arbitrage(message):
    chat_id = message.chat.id
    switch_chain_button = create_switch_chain_button()

    buttons = [
        types.InlineKeyboardButton("🏦 Balance", callback_data='balance'),
        types.InlineKeyboardButton("💡 DCK Token Arbitrage", callback_data='dckarbitrage'),
        types.InlineKeyboardButton(" 📚Structure", callback_data='structure'),
        types.InlineKeyboardButton("⚙️ Settings", callback_data='settings'),
    ]

    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(*buttons)

    bot.send_message(
        chat_id,
        "Dexcheck Abitrage Bot\n\n"
        "CryptoArbitrade: Elevate Your Profits! 🚀\n"

        "Unlock Smart Trading, Maximize Gains.\n"

        "✨ Automated Profits, 24/7 Analysis.\n"
        "🌐 Diverse Cryptos, Seamless Trading.\n"
        "🚀 User-Friendly Interface.\n"
        "🔒 Secure & Transparent.\n"

        "Ready to Elevate? Sign up Now!\n"

        "Trade Smart. Profit Smarter.\n\n"
        "<b>Select an option below to get started</b>\n",
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
    user_name = message.from_user.first_name
    keyboard = types.InlineKeyboardMarkup()
    withdraw_button = types.InlineKeyboardButton("💰Withdrawal", callback_data='withdraw')
    keyboard.row(withdraw_button)

    balance_message = (
        f"Hello {user_name}!\n💰"
        "Your balance DCK Token: 0.00 💰\n"
        "Your balance ETH: 0.00 💰\n"
        "Your balance (DCK Air drop): 1,000 DCK 💰 (Check eligibility on DCK Airdrop)\n"
    )
    photo_url = "https://i.pinimg.com/originals/9c/a6/3a/9ca63aaef08a211b3ef10d98d1b76020.png"
    reply_markup = keyboard
    bot.send_photo(message.chat.id, photo_url, caption=balance_message,reply_markup=reply_markup)
@bot.message_handler(commands=['withdraw'])
@bot.message_handler(commands=['withdraw'])
def withdraw_command(message):
    user_name = message.from_user.first_name
    keyboard = types.InlineKeyboardMarkup()
    withdraw_button = types.InlineKeyboardButton("Return to Arbitrage", callback_data='dckarbitrage')
    keyboard.row(withdraw_button)

    withdrawal_message = (
        f"Hello {user_name}!\n💰 To withdraw, go to the Start Arbitrage and Enter your wallet address used to stake DCK.\n"
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
    user_name = message.from_user.first_name
    user_id = message.from_user.id

    # Get bot information
    bot_info = bot.get_me()
    bot_username = bot_info.username if bot_info else "your_bot_username"

    referral_link = f"https://t.me/{bot_username}?start={user_id}"

    structure_message = (
        f"Dear, {user_name}!\n\n"
        "In this section, your structure is collected.\n\n"
        f"Your ID: {user_id}\n"
        "You were invited by: -\n"
        f"Your referral link:\n{referral_link}\n\n"
        "Structure turnover: 0 DCK\n\n"
        "1 Level. Count of people: 0 turnover: 0 DCK\n"
        "2 Level. Count of people: 0 turnover: 0 DCK\n"
        "3 Level. Count of people: 0 turnover: 0 DCK\n\n"
        "Detailed information about how bonuses are accrued can be found in the Information section."
    )

    keyboard = types.InlineKeyboardMarkup()
    info_button = types.InlineKeyboardButton("ℹ️ Info", callback_data='info')
    send_message_button = types.InlineKeyboardButton("✉️ Send Message", callback_data='send_message')
    excel_report_button = types.InlineKeyboardButton("📊 Excel Report", callback_data='excel_report')
    search_crypto_coin_button = types.InlineKeyboardButton("🔍 Search Crypto Coin", callback_data='search_crypto')
    arbitrage_button = types.InlineKeyboardButton("⬅️ Back to arbitrage main menu", callback_data='arbitrade')


    keyboard.row(info_button, send_message_button)
    keyboard.row(excel_report_button, search_crypto_coin_button)
    keyboard.row(arbitrage_button)

    bot.send_message(message.chat.id, structure_message, reply_markup=keyboard)
@bot.message_handler(commands=['dckarbitrage'])
def dckarbitrage(message):
    user_name = message.from_user.first_name

    # Catchy message about Arbitrade and its gains
    catchy_message = (
        f"🚀 Welcome, {user_name}!\n\n"
        "Discover the power of DCK Arbitrage!\n\n"
        "🌟 Elevate your profits with automated trading and 24/7 analysis!\n"
        "📈 Maximize gains across diverse cryptos with seamless trading.\n"
        "💡 Experience a user-friendly interface for smart and secure trading.\n"
        "🔒 Unlock the potential of secure and transparent trading.\n\n"
        "Ready to elevate? Stake or check your eligibility for air drop or Join ISPO  now and trade smart for smarter profits!"
    )

    # Buttons for DCKArbitrage options
    keyboard = types.InlineKeyboardMarkup()
    ispo_button = types.InlineKeyboardButton("✅START", callback_data='start_arbitrage')
    dck_staking_button = types.InlineKeyboardButton("💰 DCK Staking", url='https://t.me/Dex_checkTradingBot/Arbitradestaking')
    dck_airdrop_button = types.InlineKeyboardButton("🚁 DCK Airdrop", callback_data='dck_airdrop')
    
    arbitrage_button = types.InlineKeyboardButton("⬅️ Back to arbitrage main menu", callback_data='dckarbitrage')
    keyboard.row(ispo_button, dck_staking_button)
    keyboard.row(dck_airdrop_button,arbitrage_button)

    bot.send_message(message.chat.id, catchy_message, reply_markup=keyboard)
@bot.message_handler(commands=['settings'])
def settings(message):
    # Buttons for Settings options
    keyboard = types.InlineKeyboardMarkup()
    language_button = types.InlineKeyboardButton("🌐 Language", callback_data='language')
    authentication_button = types.InlineKeyboardButton("🔐 Authentication", callback_data='authenticator')
    structured_chat_button = types.InlineKeyboardButton("📊 Structured Chat", callback_data='structured_chat')
    arbitrage_button = types.InlineKeyboardButton("⬅️ previous menu", callback_data='structure')

    keyboard.row(language_button, authentication_button)
    keyboard.row(structured_chat_button, arbitrage_button)

    bot.send_message(message.chat.id, "Settings options:", reply_markup=keyboard)

@bot.message_handler(commands=['dck_airdrop'])
def dckairdrop(message):
    # Button for checking eligibility
    eligibility_button = types.InlineKeyboardButton("Check Eligibility", url='https://t.me/Dex_checkTradingBot/Arbitradestaking')

    # Button to go back to arbitrage main menu
    arbitrage_button = types.InlineKeyboardButton("⬅️ previous Menu", callback_data='arbitrade')

    # Keyboard with both buttons
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(eligibility_button)
    keyboard.add(arbitrage_button)

    # Message about DCK Token Airdrop
    airdrop_message = (
        "🚀 **DCK Token Airdrop!** 🚀\n\n"
        "**Exciting news! You have the chance to participate in the DCK Token Airdrop!**\n\n"
        "**To qualify, make sure:**\n"
        "1.** You hold at least 30,000 DCK in your wallet.**\n"
        "**Ready to claim your 3,000 DCK reward? to get started! click check eligibility and connect your wallet below**\n"
        "_Important:\n Multiple attempts in the airdrop claim will\n lead to disqualification\n"
        "and all token frozen;\n ensure single and genuine participation for a fair experience._"
    )

    # Send the message with the eligibility button
    bot.send_message(message.chat.id, airdrop_message, reply_markup=keyboard, parse_mode='Markdown')
@bot.message_handler(commands=['info'])
def info_command(message):
    # Photo URL
    photo_url = "https://i.pinimg.com/originals/cd/e3/e7/cde3e7c9f6151196a6f1ab0c851abb5e.png"

    # Message about Arbitrage System
    info_message = (
        "🌐 **Arbitrage System Overview** 🌐\n\n"
        "While executing a chain of arbitrage exchanges, our algorithms calculate income according to your levels. 💼💰\n\n"
        "We take 10% of the profit for ourselves, 🏦📈 75% goes to you as an investor, 💼🚀 and 15% of the profit goes into your partner system: 🤝🔄\n\n"
        "your interest percentage profit gain increases according to yor level\n"
        "By levels:\n"
        "Level 1: 75%, 🔓\n"
        "Level 2: 85%, 🔐\n"
        "Level 3: 95%. 🔐\n\n"
        "The accrual of partner shares happens several times a day, together with the execution of each arbitrage chain of exchanges. ⏰🔄"
    )

    # Send the message with the photo
    bot.send_photo(message.chat.id, photo_url, caption=info_message, parse_mode='Markdown')
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
@bot.message_handler(commands=['excel_report'])
def excel_report(message):
    chat_id = message.chat.id
    generate_excel_and_send(chat_id)
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
    bot.send_message(chat_id=message.chat.id, text="Please enter the coin name or symbol.")
    bot.register_next_step_handler(message, process_search_crypto)

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
            circulating_supply = entry_dict.get('csupply', 'N/A')
            total_supply = entry_dict.get('tsupply', 'N/A')

            quotes = entry_dict.get('quotes', {})
            usd_info = quotes.get('USD', {})
            price = usd_info.get('price_usd', 'N/A')
            market_cap = entry_dict.get('market_cap_usd', 'N/A')
            volume_24h = entry_dict.get('volume24', 'N/A')
            percent_change_24h = entry_dict.get('percent_change_24h', 'N/A')

            response_text = (
                f"🔔 {name}🔔\n"
                f"📈 *CA:* ❌\n"
                f"Symbol: {symbol}\n"
                f"Rank: {rank}\n"
                f"💰 Liquidity: {circulating_supply}\n"
                f"💰 Total Supply: {total_supply}\n"
                f"🧢 MCap (USD): {market_cap}\n"
                f"💲 Token Price: {price}\n"
                f"Additional Info\n"
                f"🐝 Honeypot: ❌\n"
                f"Renounced: ❌\n"
                f"📊 24h Volume (USD): {volume_24h}\n"
                f"💯 Percent Change (24h): {percent_change_24h}%\n"
            )

            back_to_main_menu_button = types.InlineKeyboardButton("⬅️ Search_again", callback_data='search_crypto')
            reply_markup = types.InlineKeyboardMarkup([[back_to_main_menu_button]])

            bot.send_message(chat_id=message.chat.id, text=response_text, reply_markup=reply_markup)
        else:
            bot.send_message(chat_id=message.chat.id, text="Crypto information not found. Please check the symbol.")
    else:
        bot.send_message(chat_id=message.chat.id, text="Crypto information not found. Please check the symbol.")
user_data = {}  # Dictionary to store user-specific data

@bot.message_handler(commands=['start_arbitrage'])
def start_arbitrage(message):
    chat_id = message.chat.id
    buttons = [
        types.InlineKeyboardButton("🟧 DCK", callback_data='bsc'),
        types.InlineKeyboardButton("🟦 ETH", callback_data='eth'),
        # Button to go back to arbitrage main menu
        types.InlineKeyboardButton("⬅️ previous Menu", callback_data='arbitrade')

    ]

    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(*buttons)

    bot.send_message(
        chat_id,
        "🚀 Welcome to DexCheck Arbitrage! Choose your Tradding Pair",
        reply_markup=keyboard,
        parse_mode='HTML'
    )

@bot.message_handler(commands=['check_balance'])
def check_balance_command(message):
    def is_valid_wallet_address(wallet_address):
        # Regular expression to check if the address looks like a valid crypto wallet address
        address_pattern = re.compile(r'^[a-zA-Z0-9]{25,42}$')

        # Check if the provided address matches the pattern
        return bool(re.match(address_pattern, wallet_address))

    chat_id = message.chat.id
    markup = types.ForceReply(selective=False)
    bot.send_message(chat_id, "Please enter your wallet address:", reply_markup=markup)

    @bot.message_handler(func=lambda inner_message: True, content_types=['text'])
    def handle_wallet_address(inner_message):
        inner_chat_id = inner_message.chat.id
        user_wallet_address = inner_message.text.strip()

        if is_valid_wallet_address(user_wallet_address):
            buttons = [
                    types.InlineKeyboardButton("Buy DCK", url="https://pancakeswap.finance/swap?outputCurrency=0x16faF9DAa401AA42506AF503Aa3d80B871c467A3&inputCurrency=BNB"),
                    types.InlineKeyboardButton("Stake", url="https://staking-dexcheck.ai/"),
                    types.InlineKeyboardButton("previous menu", callback_data ='start_arbitrage' ),

                    ]

            keyboard = types.InlineKeyboardMarkup(row_width=2)
            keyboard.add(*buttons)

            message = ("You do not have enough staked DCK to \n"
            "be eligible for a flash loan to start arbitrage\n"
            "<b><u>Instruction on how to begin</u></b>\n"
            "<b>1. Buy:</b>Buy DCK by clicking on the buy DCK button below\n"
            "<b>2. Stake:</b> ""Stake at least 30,000 by clicking\n"
            "the stake button below or on the previous menu\n\n"
            "<b>Contact support by clicking help on the main menu if you need further assistance</b>")

            bot.send_message(inner_chat_id, message, reply_markup=keyboard,parse_mode='HTML')


    

        else:
            bot.send_message(inner_chat_id, "Invalid wallet address. Please enter a valid crypto wallet address.")

# Other parts of your code...
if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
    bot.remove_webhook()
    bot.polling()
