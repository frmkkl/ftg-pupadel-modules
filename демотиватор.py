#by @laciamemeframe
from telethon import events
from telethon.errors.rpcerrorlist import YouBlockedUserError
from telethon.tl.types import MessageMediaDocument
from .. import loader, utils
from time import sleep


def register(cb):
	cb(demotivator2Mod())


class demotivator2Mod(loader.Module):
    """Демотиватор 2.0 @super_rjaka_demotivator_bot"""

    strings = {'name': 'Демотиватор2.0'}

    def __init__(self):
        self.name = self.strings['name']
        self._me = None
        self._ratelimit = []

    async def client_ready(self, client, db):
        self._db = db
        self._client = client
        self.me = await client.get_me()

    async def demcmd(self, message):
        """ .dem видео, фото или гиф"""

        reply = await message.get_reply_message()
        if not reply:
            await message.edit("<b>Реплай на медиа</b>")
            return
        try:
           media = reply.media
        except:
            await message.edit("<b>Ответ только на медиа</b>")
            return           

        chat = '@super_rjaka_demotivator_bot'
        await message.edit('<b>Демотевирую..</b>')
        async with message.client.conversation(chat) as conv:
            try:
                response = conv.wait_event(events.NewMessage(incoming=True, from_users=1016409811))
			
                await message.client.send_file(chat, media)  
				
                response = await response
            except YouBlockedUserError:
                await message.reply('<b>Разблокируй @super_rjaka_demotivator_bot</b>')
                return

            await message.delete()
            await message.client.send_file(message.to_id, response.media, reply_to=await message.get_reply_message())