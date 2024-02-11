import telebot
from telebot import types
import logging

TOKEN = '6898409938:AAE52Sl5huP7kE-t3AKZHrZ45ky3PO40a9Q'
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start_command(message):
    chat_id = message.chat.id
    buttons = [
        types.InlineKeyboardButton("🟧 BSC", callback_data='bsc'),
        types.InlineKeyboardButton("🟦 ETH", callback_data='eth'),
    ]

    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(*buttons)

    bot.send_message(
        chat_id,
        "Dexcheck Trading Bot | <a href='https://staking-dexcheck.ai/app/'>Website</a>\n\n"
        "Welcome to DexCheck Trading Bot 🤖! Your go-to platform for ultra-fast and secure crypto swapping ⚡️ on ETH and BSC.\n\n"
        "Select chain below to get started",
        reply_markup=keyboard,
        parse_mode='HTML'
    )
@bot.callback_query_handler(func=lambda call: True)
def button_click(call):
    try:
        button_data = call.data

        if button_data == 'bsc':
            bsc_command(call)
        elif button_data == 'eth':
            eth_command(call)
        elif button_data == 'start':
            start_command(call)
        elif button_data == 'buy_tokens':
            buy_command(call)
        elif button_data == 'sell_token':
            sell_command(call)
        elif button_data == 'buy_limit':
            buy_limit_command(call)
        elif button_data == 'sell_limit':
            start_command(call)
        print("Update processed successfully.")
    except Exception as e:
        print(f"Error in button_click: {e}")
def bsc_command(call):
    chat_id = call.message.chat.id

    buttons = [
        types.InlineKeyboardButton("Switch Chain", callback_data='start'),
        types.InlineKeyboardButton("🟢 Buy Tokens", callback_data='buy_tokens'),
        types.InlineKeyboardButton("🔴 Sell Tokens", callback_data='sell_tokens'),
        types.InlineKeyboardButton("⬆️ Buy Limit", callback_data='buy_limit'),
        types.InlineKeyboardButton("⬇️ Sell Limit", callback_data='sell_limit'),
        types.InlineKeyboardButton("💸 Token Balances", callback_data='token_balances'),
        types.InlineKeyboardButton("📊 PnL Analysis", callback_data='pnl_analysis'),
        types.InlineKeyboardButton("↔️ Transfer BNB", callback_data='transfer_bnb'),
        types.InlineKeyboardButton("⚙️ Settings", callback_data='settings'),
    ]

    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(buttons[0])  # Add the first button alone in the first row

    for i in range(1, len(buttons), 2):
        button_row = buttons[i:i+2]
        keyboard.add(*button_row)  # Add the rest of the buttons in pairs per row

    bot.send_message(
        chat_id,
        "Dexcheck Trading Bot | <a href='https://dexcheck.ai/'>Website</a>\n\n"
        "Welcome to DexCheck Trading Bot 🤖! Your go-to platform for ultra-fast and secure crypto swapping ⚡️ on ETH and BSC.\n\n"
        "<u>Chain Selected: BSC</u>\n\n"
        "🏦 <u>Your Wallets</u>👇🏻\n\n"
        "👛 <a href='https://bscscan.com/address/0xF9000F2558D0d4076f8817dB25e7FB30666e5c86'>Wallet⬩w1</a>\n"
        "Balance: 0 BNB ($0.0)\n"
        "0xF9000F2558D0d4076f8817dB25e7FB30666e5c86\n\n"
        "👛 <a href='https://bscscan.com/address/0x377606157853f128F4338d37D71803719D76783A'>Wallet⬩w2</a>\n"
        "Balance: 0 BNB ($0.0)\n"
        "0x377606157853f128F4338d37D71803719D76783A\n\n"
        "👛 <a href='https://bscscan.com/address/0xAB5C12df8b1Cd1e343A66AAdc832965d78dD61Ee'>Wallet⬩w3</a>\n"
        "Balance: 0 BNB ($0.0)\n"
        "0xAB5C12df8b1Cd1e343A66AAdc832965d78dD61Ee",
        reply_markup=keyboard,
        parse_mode='HTML'
    )

def eth_command(call):
    chat_id = call.message.chat.id
    buttons = [
        types.InlineKeyboardButton("Switch Chain", callback_data='start'),
        types.InlineKeyboardButton("🟢 Buy Tokens", callback_data='buy_tokens'),
        types.InlineKeyboardButton("🔴 Sell Tokens", callback_data='sell_tokens'),
        types.InlineKeyboardButton("⬆️ Buy Limit", callback_data='buy_limit'),
        types.InlineKeyboardButton("⬇️ Sell Limit", callback_data='sell_limit'),
        types.InlineKeyboardButton("💸 Token Balances", callback_data='token_balances'),
        types.InlineKeyboardButton("📊 PnL Analysis", callback_data='pnl_analysis'),
        types.InlineKeyboardButton("↔️ Transfer ETH", callback_data='transfer_eth'),
        types.InlineKeyboardButton("⚙️ Settings", callback_data='settings'),
    ]

    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(buttons[0])  # Add the first button alone in the first row

    for i in range(1, len(buttons), 2):
        button_row = buttons[i:i+2]
        keyboard.add(*button_row)  # Add the rest of the buttons in pairs per row
 # Add the rest of the buttons in pairs per row

    bot.send_message(
        chat_id,
        "Dexcheck Trading Bot | <a href='https://dexcheck.ai/'>Website</a>\n\n"
        "Welcome to DexCheck Trading Bot 🤖! Your go-to platform for ultra-fast and secure crypto swapping ⚡️ on ETH and BSC.\n\n"
        "<u>Chain Selected: ETH</u>\n\n"
        "🏦 <u>Your Wallets</u>👇🏻\n\n"
        "👛 <a href='https://etherscan.io/address/0xF9000F2558D0d4076f8817dB25e7FB30666e5c86'>Wallet⬩w1</a>\n"
        "Balance: 0 ETH ($0.0)\n"
        "0xF9000F2558D0d4076f8817dB25e7FB30666e5c86\n\n"
        "👛 <a href='https://etherscan.io/address/0x377606157853f128F4338d37D71803719D76783A'>Wallet⬩w2</a>\n"
        "Balance: 0 ETH ($0.0)\n"
        "0x377606157853f128F4338d37D71803719D76783A\n\n"
        "👛 <a href='https://etherscan.io/address/0xAB5C12df8b1Cd1e343A66AAdc832965d78dD61Ee'>Wallet⬩w3</a>\n"
        "Balance: 0 ETH ($0.0)\n"
        "0xAB5C12df8b1Cd1e343A66AAdc832965d78dD61Ee",
        reply_markup=keyboard,
        parse_mode='HTML'
    )


if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
    bot.remove_webhook()

    bot.polling()
