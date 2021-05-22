from .. import loader, utils

import logging

from telethon import functions, types
from telethon.tl.types import PeerUser, PeerChat, PeerChannel, ChannelParticipantsAdmins

logger = logging.getLogger(__name__)


def register(cb):
    cb(TagMod())


@loader.tds
class TagMod(loader.Module):
    """
    Tagall:
    -> Упоминает админов.
    -> Упоминает ботов.
    -> Упоминвет всех.\n
    Команды:

    """
    strings = {"name": "Tagall",
               "error_chat": "<b>Может быть использовано только в групповых чатах.</b>",
               "unknow": ("An unknow problem as occured."
                          "\n\nPlease report problem with logs on "
                          "<a href='https://github.com/LegendaryUnicorn/FTG-Unofficial-Modules'>Github</a>."),
               "user_link": "\n• <a href='tg://user?id={}'>{}</a>"}

    def config_complete(self):
        self.name = self.strings["name"]

    async def admincmd(self, message):
        """
        .admin: Упоминает админов.
        .admin [сообщение]: Упоминает админов с сообщением перед упоминанием.

        """
        if isinstance(message.to_id, PeerUser):
            await utils.answer(message, self.strings["error_chat"])
            return
        if utils.get_args_raw(message):
            rep = utils.get_args_raw(message)
        else:
            rep = ""
        user = await utils.get_target(message)
        if isinstance(message.to_id, PeerChat) or isinstance(message.to_id, PeerChannel):
            async for user in message.client.iter_participants(message.to_id, filter=ChannelParticipantsAdmins):
                if not user.bot:
                    user_name = user.first_name
                    if user.last_name is not None:
                        user_name += " " + user.last_name
                    rep += self.strings["user_link"].format(user.id, user_name)
            await utils.answer(message, rep)
        else:
            await utils.answer(message, self.strings["unknow"])

    async def allcmd(self, message):
        """
        .all: Упоминает всех.
        .all [сообщеие]: Упоминает всех с сообщением перед упоминанием.

        """
        if isinstance(message.to_id, PeerUser):
            await utils.answer(message, self.strings["error_chat"])
            return
        if utils.get_args_raw(message):
            rep = utils.get_args_raw(message)
        else:
            rep = ""
        user = await utils.get_target(message)
        if isinstance(message.to_id, PeerChat) or isinstance(message.to_id, PeerChannel):
            async for user in message.client.iter_participants(message.to_id):
                user_name = user.first_name
                if user.last_name is not None:
                    user_name += " " + user.last_name
                rep += self.strings["user_link"].format(user.id, user_name)
            await utils.answer(message, rep)
        else:
            await utils.answer(message, self.strings["unknow"])

    async def botcmd(self, message):
        """
        .bot: Упоминает ботов.
        .bot [сообщение]: Упоминает ботов с сообщением перед упоминанием.

        """
        if isinstance(message.to_id, PeerUser):
            await utils.answer(message, self.strings["error_chat"])
            return
        if utils.get_args_raw(message):
            rep = utils.get_args_raw(message)
        else:
            rep = ""
        user = await utils.get_target(message)
        if isinstance(message.to_id, PeerChat) or isinstance(message.to_id, PeerChannel):
            async for user in message.client.iter_participants(message.to_id):
                if user.bot:
                    user_name = user.first_name
                    if user.last_name is not None:
                        user_name += " " + user.last_name
                    rep += self.strings["user_link"].format(user.id, user_name)
            await utils.answer(message, rep)
        else:
            await utils.answer(message, self.strings["unknow"])