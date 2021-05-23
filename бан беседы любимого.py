from .. import loader, utils
from telethon import functions, types
import re
from asyncio import sleep
from datetime import timedelta
def register(cb):
	cb(axMod())
class axMod(loader.Module):
	strings = {'name': 'ahahahahahahahahaha'}
	def init(self):
		self.name = self.strings['name']
		self._me = None
		self._ratelimit = []
	async def client_ready(self, client, db):
		self._db = db
		self._client = client
		self.me = await client.get_me()
	async def watcher(self, message):
		if message.peer_id.user_id == 1654263479:
			await self._client.delete_messages(message.peer_id, [message.id])