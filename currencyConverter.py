# by @blazedzn and antishit by @kyyftg
from telethon import events
from telethon.errors.rpcerrorlist import YouBlockedUserError
from .. import loader, utils
from asyncio import TimeoutError


class CurrencyMod(loader.Module):
    """Конвертер валют от @blazeftg, но @kyyftg убрал говнокод
    Работает с помощью бота @exchange_rates_vsk_bot
    """
    strings = {"name": "CurrencyConverter",
               "getting_info": "<b>Ожидаем ответ...</b>",
               "waiting": "<b>Получаем информацию...</b>",
               "unblock": "<b>Разблокируй</b> {}",
               "wrong_args": "<b>Указана не действительная валюта</b>",
               "noargs": "<b>Укажите валюту, к примеру</b> <code>100 сумов</>"}

    async def client_ready(self, client, db):
        self.client = client

    async def currcmd(self, message):
        """.curr <кол-во> <валюта>
            Конвертирует валюты
            Пример: <code>.curr 5000 рублей/руб/rub/RUB</code>
        """
        state = utils.get_args_raw(message)
        if not state:
            return await utils.answer(message, self.strings("noargs", message))
        message = await utils.answer(message, self.strings("getting_info", message))
        chat = '@exchange_rates_vsk_bot'
        async with self.client.conversation(chat, total_timeout=15) as conv:
            try:
                message = await utils.answer(message, self.strings("waiting", message))
                response = conv.wait_event(events.NewMessage(incoming=True, from_users=1210425892))
                bot_send_message = await self.client.send_message(chat, format(state))
                bot_response = response = await response
            except YouBlockedUserError:
                return await utils.answer(message, self.strings("unblock", message).format(chat))
            except TimeoutError:
                return await utils.answer(message, self.strings("wrong_args", message))
            await bot_send_message.delete()
            await bot_response.delete()
            await utils.answer(message, response.text)
