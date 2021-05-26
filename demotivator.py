#by @krabodyan
from telethon.events import NewMessage
from telethon.errors.rpcerrorlist import YouBlockedUserError
from asyncio.exceptions import TimeoutError, CancelledError
from .. import loader, utils


def register(cb):
	cb(DemotivatorMod())
	

CHAT = "IvIy_bot"


class DemotivatorMod(loader.Module):
    """Демотиватор от крабодяна"""

    strings = {'name': 'Демотиватор'}
    
    async def client_ready(self, client, _):
        self.client = client
        await client.send_message(CHAT, "/start") # не ну а хуле нет собственно
           
    async def demcmd(self, message):
        """ .dem <текст> <реплай на гифку/кругляш/стикер/фото>"""
        if self.client._conversations.get(1376531590) is not None:
        	return await message.edit("<b>подожди перед тем как создавать новый демотиватор.</b>")

        reply = await message.get_reply_message()
        if not reply or not reply.media or not any([
        	True for _ in ('sticker', 'photo', 'video', 'video_note')
        	if getattr(reply, _, None) is not None
        	]):
        	return await message.edit("<b>нужен реплай на фотку/видео/стикер!</b>")
        if reply.file.size / 1024 / 1024 > 4:
        	return await message.edit("<b>бот принимает видео до 4 мб</b>")
        args = utils.get_args_raw(message) or reply.message
        if not args:
        	return await message.edit('<b>укажи аргументы после команды...</b>')
        if len(args) > 500:
        	return await message.edit("<b>бот принимает текст длинной до 500 символов</b>")

        await message.edit("<b>демотивирую...</b>")
        async with self.client.conversation(CHAT, timeout=160) as conv:
            try:
                response = conv.wait_event(NewMessage(incoming=True, from_users=CHAT))
                msg = await reply.forward_to(CHAT)
                await msg.reply(f"/demoti {args}")
                response = await response
                if not response.media:
                	if response.raw_text.startswith("[400]"):
                		return await message.edit("<b>демотиваторы можно создавать раз в 10 секунд, пожалейте сервер</b>")
                	response = await conv.wait_event(NewMessage(incoming=True, from_users=CHAT))
                
            except YouBlockedUserError:
                return await message.edit(f'<b>Разблокируй @{CHAT}</b>')

            except (TimeoutError, CancelledError):
            	return await message.edit("<b>бот не ответил => @krabodyan ебланище</b>")
            
            if response.media is None:
            	
            	return await message.edit("<b>что-то пошло не так.</b>")
            
            await self.client.send_file(message.to_id, response.media, reply_to=reply)
            await message.delete()
            
