# requires: requests
from .. import loader, utils
import requests


@loader.tds
class nkapimdMod(loader.Module):
    """Отправить фото из сайта nekos.life"""
    strings = {"name": "NekosLife",
               "idk": "<b>Нет такой категории, список:</b> <code>nklist</code>"}

    @loader.owner
    async def nkcmd(self, m):
        """Отправить фото/гиф\nПо умолчанию neko\nМожно указать другую категорию"""
        args = utils.get_args_raw(m)
        if args:
            typ = args if args in types_of else None
        else:
            typ = "neko"
        if typ is None:
            return await utils.answer(m, self.strings("idk", m))
        reply = await m.get_reply_message()
        await m.client.send_file(m.chat_id, requests.get(f"https://nekos.life/api/v2/img/{typ}").json()["url"],
                                 reply_to=reply.id if reply else None)
        if m.out:
            await m.delete()

    @loader.owner
    async def nklistcmd(self, m):
        """Список доступных категорий"""
        await utils.answer(m, "Доступные категории:\n" + "\n".join([f"<code>{i}</code>" for i in types_of]))


types_of = ['femdom', 'tickle', 'classic', 'ngif', 'erofeet', 'meow', 'erok', 'poke', 'les', 'hololewd', 'lewdk',
            'keta', 'feetg', 'nsfw_neko_gif', 'eroyuri', 'kiss', '_8ball', 'kuni', 'tits', 'pussy_jpg', 'cum_jpg',
            'pussy', 'lewdkemo', 'lizard', 'slap', 'lewd', 'cum', 'cuddle', 'spank', 'smallboobs', 'goose',
            'Random_hentai_gif', 'avatar', 'fox_girl', 'nsfw_avatar', 'hug', 'gecg', 'boobs', 'pat', 'feet', 'smug',
            'kemonomimi', 'solog', 'holo', 'wallpaper', 'bj', 'woof', 'yuri', 'trap', 'anal', 'baka', 'blowjob',
            'holoero', 'feed', 'neko', 'gasm', 'hentai', 'futanari', 'ero', 'solo', 'waifu', 'pwankg', 'eron',
            'erokemo']
