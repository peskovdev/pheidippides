from aiogram import Dispatcher, types  # type: ignore

from ..converter import convert_to_cmd_message
from ..crypto_api_service import get_all_coins, get_specific_coins
from ..static import chooseSticker


async def cmd_start(message: types.Message) -> None:
    bot_name = (await message.bot.get_me()).username
    switch_kb = types.InlineKeyboardMarkup()
    switch_kb.add(
        types.InlineKeyboardButton(
            text=f"Try @{bot_name}", switch_inline_query_current_chat=""
        )
    )

    await message.answer(
        "Project developed by @peskovdev\n\n"
        "This bot provides cryptocurrency rates!\n\n"
        "Enter /getcrypto to output a short list of cryptocurrencies, "
        "or /getallcoins for extended output.\n\n"
        "You can also subscribe and unsubscribe to daily crypto-rate "
        "with commands: /subscribe, /unsubscribe.\n\n"
        f"And don't forget to try <code>@{bot_name}</code> operator "
        "by clicking the button below!",
        parse_mode=types.ParseMode.HTML,
        reply_markup=switch_kb,
    )


async def cmd_getcrypto(message: types.Message) -> None:
    coins = await get_specific_coins(["bitcoin", "ethereum", "monero"])
    sticker_file_id = chooseSticker(coins)
    msg = convert_to_cmd_message(coins)
    await message.answer_sticker(sticker_file_id)
    await message.answer(msg, parse_mode=types.ParseMode.HTML)


async def cmd_getallcoins(message: types.Message) -> None:
    coins = await get_all_coins()
    sticker_file_id = chooseSticker(coins)
    msg = convert_to_cmd_message(coins)
    await message.answer_sticker(sticker_file_id)
    await message.answer(msg, parse_mode=types.ParseMode.HTML)


def register_handlers_common(dp: Dispatcher) -> None:
    dp.register_message_handler(cmd_start, commands="start")
    dp.register_message_handler(cmd_getcrypto, commands="getcrypto")
    dp.register_message_handler(cmd_getallcoins, commands="getallcoins")
