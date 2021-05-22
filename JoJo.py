from .. import loader, utils
import io
import requests
from PIL import Image, ImageDraw, ImageOps

class JojoImagerMod(loader.Module):
	"""JoJo style image maker"""
	strings = {"name": "JoJo"}

	def get_background(self):
		background = requests.get(f"http://johnny.systems/modules/images/jojo.jpg").content
		image = Image.new("RGBA", (1, 1), (0, 0, 0, 0))
		image = Image.open(io.BytesIO(background))
		return image

	def crop_to_circle(self, im):
		im = im.convert("RGBA")
		w, h = im.size
		x = min(w, h)
		im = im.crop([(w-x)//2, (h-x)//2, (w+x)//2, (h+x)//2])
		mask = Image.new("L", im.size, 0)
		ImageDraw.Draw(mask).ellipse((0, 0)+im.size, 255)
		im.putalpha(mask)
		return im

	def resize(self, image, scale = 1):
		image = self.crop_to_circle(image)
		new = image.resize((image.width // scale, image.height // scale))
		return new

	async def jojocmd(self, message):
		"""Используйте: .jojo <реплай>."""
		await message.edit("Загрузка")
		reply = await message.get_reply_message()
		if reply:
			user = await utils.get_user(await message.get_reply_message())
		else:
			user = await message.client.get_me()
		# фон
		image = self.get_background()
		# Обработка своей авы
		pfp = io.BytesIO()
		await message.client.download_profile_photo("me", file=pfp)
		raw_pfp = self.resize(Image.open(pfp), 2)

		image.paste(raw_pfp, (25, image.height // 2 - raw_pfp.height // 2 + 50), raw_pfp)
		# Обработка реплая
		target = io.BytesIO()
		await message.client.download_profile_photo(user, file=target)
		raw_target = self.resize(Image.open(target), 3)
#
		image.paste(raw_target, (image.width - raw_target.width - 25, image.height // 2 - raw_target.height // 2), raw_target)
		#
		output = io.BytesIO()
		output.name = "jojo.jpeg"
		image.save(output, "jpeg")
		output.seek(0)
		await message.client.send_file(message.to_id, output, reply_to=reply)
		await message.delete()