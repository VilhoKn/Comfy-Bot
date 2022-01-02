#DISCORD IMPORTS

import discord
from discord.ext import commands
from discord.utils import get
from discord.commands import Option

#OTHER IMPORTS

import sys

sys.path.append("/home/pi/Documents/")

from bot_token import TOKEN, DBL_TOKEN, WEBHOOK_URL

import aiohttp
from webhook import send_webhook
import time
import datetime
import os
import json
import asyncio
import random

#SETUP

cooldowns = {"train":60, "water":30, "find":60, "shop":25, "feed":15, "depression":86400}

custom_cooldowns = {}

TEST_IDS = []

WAVE_LINKS = ["https://c.tenor.com/NjsosaK61UIAAAAC/anime-girl.gif", "https://c.tenor.com/e48wByvWU-IAAAAC/anime-hi.gif", "https://c.tenor.com/S6V1PHV-PQUAAAAC/kuroha-shida-kuroha.gif", "https://c.tenor.com/MIXsMsU90KMAAAAC/hey-hello.gif", "https://c.tenor.com/o9Ak0TpPek0AAAAC/aikatsu-aikatsu-hello.gif", "https://c.tenor.com/ywCocDUt31QAAAAC/anime-wave.gif", "https://c.tenor.com/2mvMfV8_KW0AAAAC/kakashi-hatake-naruto.gif", "https://c.tenor.com/svW4PXq7zDYAAAAC/nanami-waving.gif", "https://c.tenor.com/H4xLf6epW-wAAAAC/anime-wave.gif", "https://c.tenor.com/aLPboFIM8K0AAAAd/smile-wave.gif", "https://c.tenor.com/lFM90Yjpl_4AAAAC/anime-wave.gif", "https://c.tenor.com/9l2tWpfn9yQAAAAd/anime-wave.gif", "https://c.tenor.com/rWN4ZHFLknoAAAAC/bye-hi.gif", "https://c.tenor.com/-AzbRX2AC2IAAAAC/liella-love-live.gif", "https://media3.giphy.com/media/F99PZtJC8Hxm0/giphy.gif?cid=ecf05e47uq1vi4qfuuy90yi8ytrxo15qafg6h1kbj8jxm6ci&rid=giphy.gif&ct=g", "https://i.gifer.com/bB.gif", "https://image.myanimelist.net/ui/5LYzTBVoS196gvYvw3zjwP0G4-gP6b2rXqiFUVocLJ8", "https://media3.giphy.com/media/S5L3aOgVqbzhK/giphy.gif", "https://i.imgur.com/xTsSaaC.gif", "https://i.imgur.com/wjaKPmk.gif", "https://i.imgur.com/foSkpOV.gif", "https://i.imgur.com/AlDSSsV.gif", "https://i.imgur.com/TXlp1YT.gif", "https://i.imgur.com/1FtD50k.gif", "https://i.imgur.com/lgbPwfk.gif"]

GIFT_LINKS = ["https://c.tenor.com/ogeFggroUIsAAAAC/toradora-taiga.gif", "https://c.tenor.com/9VlbkbzetVUAAAAC/present-for-you.gif", "https://c.tenor.com/F4g9-zQh91YAAAAC/give-kameko.gif", "https://c.tenor.com/ypyi6EUdcTUAAAAC/clannad-nagisa-furukawa.gif", "https://c.tenor.com/_60jRviVHP0AAAAC/yazawa-nico-yazawa.gif", "https://c.tenor.com/rVKehOf6nmIAAAAC/cuddles-gift.gif", "https://image.myanimelist.net/ui/5pjpFizOF0WqHWXSGonzMRiNJD0LnM9ffyHAtIEkVxqTkpiTH5viVRnMvNaCsf8VKuLvX-7EV9P_Gx1kB7vDbZ3uA-pa5hkrbKkktiuhZQk", "https://giffiles.alphacoders.com/198/198766.gif", "https://gifimage.net/wp-content/uploads/2018/10/anime-gift-gif-4.gif", "https://c.tenor.com/WIKFrbjjJRoAAAAd/nekopara-tying-up.gif", "https://lh5.googleusercontent.com/proxy/UJbPEaGRRpqpzvSXetm_ulR1vA3Ay8M68trNhX39JNeqirMz-rWVt__kwYkyrebAKKbF_XmKacKsEjUOq0yPK1opvr-DkBQ-UI_B1HIRy5KtoV7Nz41Reem0NCIEI4kCwshlQoTY6B4pDs3ltCsOCh_fPk4Vd66uI8DMeqWN7qMxHWEYt0RIHD_q0OnW2POAevXcIHTfbzFIYyDMbE7DDjmerdtvo9DqnS3KZ3QbwKAT77WmfhcjUcmPvIG4dXho3ekXI1Efz3CXLM25lo7v=s0-d", "https://pa1.narvii.com/5755/c86a21e370abd85dfd4e0f975bfeeb4f53db30eb_hq.gif", "http://ift.tt/2B9E3WP", "http://31.media.tumblr.com/d7d11ca01c4f1ba12dcad654af7f407e/tumblr_mflvroWg6X1r3qwdqo1_400.gif", "https://lh5.googleusercontent.com/proxy/cVcKWEzZQhLdoafdv53QibYimYw2a-zo120maxEkT86j7WINy67BsCHgzNCiZymy0S3zN1z_LSFbsrF1zB2A5kHeV62oQFGkbUmrlryk8VzXioY95VLh-Vfj349ByHEq0pjPG6ZgWvE6eedhcMjZG9t9cwOH1c0A3m3w_EpH1UobN0e34DUrEGjv85-RAjQVMKDhL114PY3ATF4wJmaem-WpyGPkkcNZGoKXxZBxk8oA1IZgU0BOXjbWTKERuTJawQ=s0-d"]


KISS_LINKS = []
pre_kiss = "https://purrbot.site/img/sfw/kiss/gif/kiss_x.gif"
banned_kisses =  []

for i in range(1, 112):
	i = str(i)
	if i in banned_kisses:
		continue
	if len(i) == 1:
		KISS_LINKS.append(pre_kiss.replace("x", f"00{i}"))
	elif len(i) == 2:
		KISS_LINKS.append(pre_kiss.replace("x", f"0{i}"))
	else:
		KISS_LINKS.append(pre_kiss.replace("x", i))

HUG_LINKS = []
pre_hug = "https://purrbot.site/img/sfw/hug/gif/hug_x.gif"
banned_hugs =  []

for i in range(1, 93):
	i = str(i)
	if i in banned_hugs:
		continue
	if len(i) == 1:
		HUG_LINKS.append(pre_hug.replace("x", f"00{i}"))
	elif len(i) == 2:
		HUG_LINKS.append(pre_hug.replace("x", f"0{i}"))
	else:
		HUG_LINKS.append(pre_hug.replace("x", i))

DUCK_IMAGE = []
pre_duck = "https://random-d.uk/api/x.jpg"
banned_ducks =  []

for i in range(1, 283):
	i = str(i)
	if i in banned_hugs:
		continue
	DUCK_IMAGE.append(pre_duck.replace("x", i))



with open("../files/text/on_message_trigger_words.txt", "r") as f:
	f_lines = f.readlines()
	ON_MESSAGE_TRIGGER_WORDS = []
	for i in f_lines:
		ON_MESSAGE_TRIGGER_WORDS.append(i.strip("\n"))
	ON_MESSAGE_TRIGGER_WORDS = ON_MESSAGE_TRIGGER_WORDS[:-1]

with open("../files/text/quotes.txt", "r") as f:
	f_lines = f.readlines()
	QUOTES = []
	for i in f_lines:
		QUOTES.append(i.strip("\n"))

with open("../files/text/find_sentences.txt", "r") as f:
	f_lines = f.readlines()
	FIND_SENTENCES = []
	for i in f_lines:
		FIND_SENTENCES.append(i.strip("\n"))

with open("../files/text/cat_image_links.txt", "r") as f:
	f_lines = f.readlines()
	CAT_IMAGE = []
	for i in f_lines:
		CAT_IMAGE.append(i.strip("\n"))

with open("../files/text/dog_image_links.txt", "r") as f:
	f_lines = f.readlines()
	DOG_IMAGE = []
	for i in f_lines:
		DOG_IMAGE.append(i.strip("\n"))

with open("../files/text/bunny_image_links.txt", "r") as f:
	f_lines = f.readlines()
	BUNNY_IMAGE = []
	for i in f_lines:
		BUNNY_IMAGE.append(i.strip("\n"))

with open("../files/text/meme_links.txt", "r") as f:
	f_lines = f.readlines()
	MEMES = []
	for i in f_lines:
		MEMES.append(i.strip("\n"))

with open("../files/text/cheerup_links.txt", "r") as f:
	f_lines = f.readlines()
	CHEERUP = []
	for i in f_lines:
		CHEERUP.append(i.strip("\n"))

with open("../files/text/pet_names.txt", "r") as f:
	f_lines = f.readlines()
	PET_NAMES = []
	for i in f_lines:
		PET_NAMES.append(i.strip("\n"))

with open("../files/text/thumbnail_links.txt", "r") as f:
	f_lines = f.readlines()
	THUMBNAILS = dict()
	for i in f_lines:
		t, l = i.strip("\n").split("-")
		THUMBNAILS[t] = l

#OTHER VARIABLES

värit = {"red" : 0xfc9a9a, "orange" : 0xf8be92, "yellow" : 0xfcefa9, "green" : 0xacebb9, "blue" : 0xafd1f8, "purple" : 0xd5bcf3, "pink" : 0xf5bad5, "white" : 0xFFFFFF}
c = 0xefd8d0
red = 0xfc9a9a
orange = 0xf8be92
yellow = 0xfcefa9 
green = 0xacebb9 
blue = 0xafd1f8 
purple = 0xd5bcf3 
pink = 0xf5bad5
black = 0x000000
white = 0xFFFFFF
bot_role_c = 0xf774b0


PETS_1 = ["mouse", "sheep", "squirrel", "rooster", "pig", "frog"]
PETS_2 = ["cat", "dog", "bunny", "monkey", "chicken"]
PETS_3 = ["polarbear", "bear", "tiger", "elephant", "turtle"]


FOODS = {"circle fruit" : 15, "triangle fruit" : 30, "square fruit" : 40, "star fruit" : 65, "small mushroom" : 10, "big mushroom" : 20, "watermelon" : 20, "bread" : 20, "lemon" : 20}

FOODS_UP = {"Circle fruit":":green_circle:", "Triangle fruit":":small_red_triangle:", "Square fruit":":purple_square:", "Star fruit":":star:", "Small mushroom":":mushroom:", "Big mushroom":":mushroom:", "Watermelon":":watermelon:", "Bread":":bread:", "Lemon":":lemon:"}

VÄRIT_UP = []

for text in värit.keys():
	fixed_name_t = text[0]
	rest = text[1:]
	fixed_name = f"{fixed_name_t.upper()}{rest}"
	VÄRIT_UP.append(fixed_name)


class pet_account:
	def __init__(self, **kwargs):
		self.__dict__.update(kwargs)


class profile_account:
	def __init__(self, **kwargs):
		self.__dict__.update(kwargs)


class bank_account:
	def __init__(self, **kwargs):
		self.__dict__.update(kwargs)


#BOT VARIABLES

bot = discord.Bot()

#EVENTS

@bot.event
async def on_guild_join(guild):
	try:
		print(f"Comfy joined '{guild.name}', Count: {guild.member_count}")
	except:
		print(f"Comfy joined '{guild.name}', Count: ERROR")
	try:
		await send_webhook(guild, bot, True, WEBHOOK_URL)
	except Exception as e:
		print(e)
		print("webhook error")
	await update_guild_count()

@bot.event
async def on_guild_remove(guild):
	try:
		print(f"Comfy left '{guild.name}', Count: {guild.member_count}")
	except:
		print(f"Comfy left '{guild.name}', Count: ERROR")
	try:
		await send_webhook(guild, bot, False,WEBHOOK_URL)
	except Exception as e:
		print(e)
		print("webhook error")
	await update_guild_count()

@bot.event
async def on_ready():
	print(len(bot.guilds))
	for i in bot.guilds:
		print(i.name, end=", ")
		try:
			print(i.member_count)
		except:
			print("ERROR")
	await bot.change_presence(status=discord.Status.idle, activity=discord.Activity(type=discord.ActivityType.listening,name='Comfy Vibes'))
	print(f"\nComfy Bot logged in as: {bot.user}", end="\n\n")

@bot.event
async def on_message(message):
	if message.author.bot:
		return
	temp_msg = message.content.lower()
	for i in ON_MESSAGE_TRIGGER_WORDS:
		if i in temp_msg:
			result = await update_cooldowns(message.author, "depression")
			if result:
				return
			print(f"Depression detected on '{message.guild}' by '{message.author}', message content was '{message.content}'")
			viesti = discord.Embed(title="Depression Help", description = f"Hey, I saw you were talking about sad things on {message.guild} and wanted to say that there are people that love and care about you! Hope you are okay.\n\nIf you want information about helplines for depressed and suicidal people use command `/ineedhelp`", color = c)
			try:
				channel = await message.author.create_dm()
				await channel.send(embed=viesti)
				await update_commands("depression", message.guild)
			except:
				try:
					await message.channel.send(embed=viesti, ephemeral=True)
					await update_commands("depression", message.guild)
				except:
					print("weird problem")
			return

#COMMANDS

@bot.slash_command(name="dice", description="Rolls the dice")
async def dice(ctx):
	num = random.randint(1, 6)
	viesti = discord.Embed(description = f"You rolled {num}!", color = c)
	await ctx.respond(embed=viesti)
	await update_commands("dice", ctx.guild)

@bot.slash_command(name="coinflip", description="Flips a coin")
async def coinflip(ctx):
	num = random.randint(1, 2)
	value = "tails" if num == 1 else "heads"
	viesti = discord.Embed(description = f"You got {value}!", color = c)
	await ctx.respond(embed=viesti)
	await update_commands("coinflip", ctx.guild)

@bot.slash_command(name="ineedhelp", description="Sends an info message about depression helplines in dms")
async def ineedhelp(ctx):
	viesti = discord.Embed(title="I Need Help Helplines", description = f"Here is information about helplines for depressed and suicidal people", color = c)
	viesti.add_field(name="Child Helplines (EU)", value="""
Telephone: 116 111

This number is free of charge.

The number 116 111 is specifically for children who seek assistance and need someone to talk to. The service helps children in need of care and protection and links them to the appropriate services and resources; it provides children with an opportunity to express their concerns and talk about issues directly affecting them.

Here's an alphabetical list of member states which have access to 116 111: Bulgaria, Cyprus, Czech Republic, Germany, Denmark, Estonia, Greece, Spain, Finland, Croatia, Hungary, Ireland, Lithuania, Luxembourg, Latvia, Poland, Portugal, Romania, Sweden, Slovenia, Slovakia, United Kingdom, Malta.
	""")
	viesti.add_field(name="Emotional Support Helpline (EU)", value="""
Telephone: 116 123

This number is free of charge.

116 123 is a phone number for people suffering from loneliness or who are in a state of psychological crisis or thinking about committing suicide.

Here's an alphabetical list of member states which have access to 116 123: Austria, Czech Republic, Germany, Greece, Hungary, Ireland, Lithuania, Malta, Netherlands, Poland, Slovenia, Sweden, United Kingdom.
	""")
	viesti.add_field(name="National Suicide Prevention Lifeline (US)", value="""
Telephone: 1-800-273-8255 (1-800-273-TALK)
Text: Text "START" (without quotes) to 741-741.
	""")
	try:
		channel = await ctx.author.create_dm()
		await channel.send(embed=viesti)
		viesti2 = discord.Embed(title="I Need Help Helplines", description = "I sent you a dm about helplines for depressed and suicidal people", color = c)
		await ctx.respond(embed=viesti2, ephemeral=True)
	except:
		await ctx.respond(embed=viesti, ephemeral=True)
	await update_commands("ineedhelp", ctx.guild)

@bot.slash_command(name="quote", description="Sends a comfy quote")
async def quote(ctx):
	ce = random.choice(QUOTES)
	quote, author = ce.split("-")
	
	viesti = discord.Embed(description = quote, color = c)
	if author == "me":
		author = "Comfy Bot"
	else:
		viesti.set_footer(text=f"~ {author}")
	await ctx.respond(embed=viesti)
	await update_commands("quote", ctx.guild)

@bot.slash_command(name="hug", description="Give someone a hug")
async def hug(ctx, member : Option(discord.Member, "Member to hug")):
	await open_profile(ctx.author)
	await open_profile(member)
	pref = f"{ctx.author.mention} hugged x y"
	if ctx.author.id != member.id:
		pref = pref.replace("x", f"{member.mention}")
		pref = pref.replace("y", "(つˆ⌣ˆ)つ⊂(・﹏・⊂)")
		await add_profile(ctx.author, member, "hug")
	else:
		pref = pref.replace("x", "themselves")
		pref = pref.replace("y", "(*・ω・)")
	viesti = discord.Embed(description = pref, color = c)
	viesti.set_image(url=random.choice(HUG_LINKS))
	await ctx.respond(embed=viesti)
	await update_commands("hug", ctx.guild)

@bot.user_command(name="Hug this person!")
async def callbackname(ctx, member : discord.Member):
	await open_profile(ctx.author)
	await open_profile(member)
	pref = f"{ctx.author.mention} hugged x y"
	if ctx.author.id != member.id:
		pref = pref.replace("x", f"{member.mention}")
		pref = pref.replace("y", "(つˆ⌣ˆ)つ⊂(・﹏・⊂)")
		await add_profile(ctx.author, member, "hug")
	else:
		pref = pref.replace("x", "themselves")
		pref = pref.replace("y", "(*・ω・)")
	viesti = discord.Embed(description = pref, color = c)
	viesti.set_image(url=random.choice(HUG_LINKS))
	await ctx.respond(embed=viesti)
	await update_commands("hug_user", ctx.guild)

@bot.slash_command(name="kiss", description="Kiss someone")
async def kiss(ctx, member : Option(discord.Member, "Member to kiss")):
	await open_profile(ctx.author)
	await open_profile(member)
	pref = f"{ctx.author.mention} kissed x y"
	if ctx.author.id != member.id:
		pref = pref.replace("x", f"{member.mention}")
		pref = pref.replace("y", "(˶^ з^(◡‿◡˶)")
		await add_profile(ctx.author, member, "kiss")
	else:
		pref = pref.replace("x", "themselves")
		pref = pref.replace("y", "(*・ω・)")
	viesti = discord.Embed(description = pref, color = c)
	viesti.set_image(url=random.choice(KISS_LINKS))
	await ctx.respond(embed=viesti)
	await update_commands("kiss", ctx.guild)

@bot.user_command(name="Kiss this person!")
async def callbackname(ctx, member : discord.Member):
	await open_profile(ctx.author)
	await open_profile(member)
	pref = f"{ctx.author.mention} kissed x y"
	if ctx.author.id != member.id:
		pref = pref.replace("x", f"{member.mention}")
		pref = pref.replace("y", "(˶^ з^(◡‿◡˶)")
		await add_profile(ctx.author, member, "kiss")
	else:
		pref = pref.replace("x", "themselves")
		pref = pref.replace("y", "(*・ω・)")
	viesti = discord.Embed(description = pref, color = c)
	viesti.set_image(url=random.choice(KISS_LINKS))
	await ctx.respond(embed=viesti)
	await update_commands("kiss_user", ctx.guild)

@bot.slash_command(name="wave", description="Wave at someone")
async def wave(ctx, member : Option(discord.Member, "Member to wave at")):
	await open_profile(ctx.author)
	await open_profile(member)
	pref = f"{ctx.author.mention} waved at x y"
	if ctx.author.id != member.id:
		pref = pref.replace("x", f"{member.mention}")
		pref = pref.replace("y", "(*・ω・)ﾉ")
		await add_profile(ctx.author, member, "wave")
	else:
		pref = pref.replace("x", "themselves")
		pref = pref.replace("y", "(*・ω・)ﾉ")
	viesti = discord.Embed(description = pref, color = c)
	viesti.set_image(url=random.choice(WAVE_LINKS))
	await ctx.respond(embed=viesti)
	await update_commands("wave", ctx.guild)

@bot.user_command(name="Wave at this person!")
async def callbackname(ctx, member : discord.Member):
	await open_profile(ctx.author)
	await open_profile(member)
	pref = f"{ctx.author.mention} waved at x y"
	if ctx.author.id != member.id:
		pref = pref.replace("x", f"{member.mention}")
		pref = pref.replace("y", "(*・ω・)ﾉ")
		await add_profile(ctx.author, member, "wave")
	else:
		pref = pref.replace("x", "themselves")
		pref = pref.replace("y", "(*・ω・)")
	viesti = discord.Embed(description = pref, color = c)
	viesti.set_image(url=random.choice(WAVE_LINKS))
	await ctx.respond(embed=viesti)
	await update_commands("wave_user", ctx.guild)


@bot.slash_command(name="gift", description="Give a gift to someone")
async def gift(ctx, member : Option(discord.Member, "Gift receiver"), gift : Option(str, "The gift you want give")):
	await open_profile(ctx.author)
	await open_profile(member)
	pref = f"{ctx.author.mention} gave x gift11000 y"
	if ctx.author.id != member.id:
		pref = pref.replace("x", f"{member.mention}")
		pref = pref.replace("y", "(´・ω・)っ由")
		pref = pref.replace("gift11000", gift)
		await add_profile(ctx.author, member, "gift")
	else:
		pref = pref.replace("x", "themselves")
		pref = pref.replace("y", "(*・ω・)")
		pref = pref.replace("gift11000", gift)
	viesti = discord.Embed(description = pref, color = c)
	viesti.set_image(url=random.choice(GIFT_LINKS))
	await ctx.respond(embed=viesti)
	await update_commands("gift", ctx.guild)

@bot.slash_command(name="cat", description="Send a cute cat picture")
async def cat(ctx):
	cat = random.choice(CAT_IMAGE)
	await ctx.respond(cat)
	await update_commands("cat", ctx.guild)

@bot.slash_command(name="dog", description="Send a cute dog picture")
async def dog(ctx):
	dog = random.choice(DOG_IMAGE)
	await ctx.respond(dog)
	await update_commands("dog", ctx.guild)

@bot.slash_command(name="bunny", description="Send a cute bunny picture")
async def bunny(ctx):
	bunny = random.choice(BUNNY_IMAGE)
	await ctx.respond(bunny)
	await update_commands("bunny", ctx.guild)

@bot.slash_command(name="duck", description="Send a cute duck picture")
async def duck(ctx):
	duck = random.choice(DUCK_IMAGE)
	await ctx.respond(duck)
	await update_commands("duck", ctx.guild)

@bot.slash_command(name="meme", description="Send a cute meme")
async def meme(ctx):
	mem = random.choice(MEMES)
	await ctx.respond(mem)
	await update_commands("meme", ctx.guild)

@bot.slash_command(name="cheerup", description="Send a cheerup meme")
async def cheerup(ctx):
	cheer = random.choice(CHEERUP)
	await ctx.respond(cheer)
	await update_commands("cheerup", ctx.guild)

@bot.slash_command(name="profilehelp", description="Sends a profile help message")
async def profilehelp(ctx):
	viesti = discord.Embed(title = "Profile help message", description = "Comfy Bot has 2 profile commands, `/profile` and `/myprofile`. These profiles are global across servers.\n\n`/profile` shows a members profile.\n\n`/myprofile` shows your own profile. You can also pass in a description and color to show on your profile. The description has a 150 character limit\n\nThe profile shows the users sent and received actions. Actions are `/hug`, `/kiss`, `/wave` and `/gift`\n\nHope this helps designing your profile!", color = c)
	await ctx.respond(embed=viesti, ephemeral=True)
	await update_commands("profilehelp", ctx.guild)

@bot.slash_command(name="help", description="Sends Comfy Bot help message")
async def help(ctx):
	viesti = discord.Embed(title = "Comfy Bot Help Message", description = "Comfy Bot is made to make others happy!\n It has tons of fun commands you can use!\nComfy uses `/` slash commmands like most popular bots.", color = c)
	viesti.add_field(name="Word detection", value="Comfy bot has word detection that sends\n hope you're okay messages to the users sending depressing messages.", inline=False)
	viesti.add_field(name=":frame_photo: Images", value="`/cat` `/dog` `/bunny`\n`/duck` `/meme`\n`/cheerup`")
	viesti.add_field(name=":busts_in_silhouette: Community", value="`/colorrole`\n`/ineedhelp` `/quote`\n`/dice` `/coinflip`")
	viesti.add_field(name=":exclamation:Actions", value="`/hug` `/kiss`\n`/wave` `/gift`")
	viesti.add_field(name="Other help commands", value="`/profilehelp` shows all Comfy Bots profile commands\n`/pethelp` shows all Comfy Bots pet commands", inline=False)
	viesti.add_field(name="Quick Links", value="[Support Server](https://top.gg/servers/901214060740235275) • [Invite Me](https://discord.com/api/oauth2/authorize?client_id=900706330183102525&permissions=268437504&scope=bot%20applications.commands) • [Vote for me](https://top.gg/bot/900706330183102525)")
	await ctx.respond(embed=viesti, ephemeral=True)
	await update_commands("help", ctx.guild)



@bot.slash_command(name="colorrole", description="Claim a color role")
async def colorrole(ctx, color : Option(str, "The color role you want", choices=VÄRIT_UP)):
	color_fix = color.lower()
	try:
		viesti_suc = discord.Embed(description = f"You succesfully got color role {color_fix}", color = värit[color_fix])
	except:
		pass
	try:
		w_role = None
		for i in ctx.author.roles:
			if i.name.lower() in värit.keys():
				await ctx.author.remove_roles(i)
		for i in ctx.guild.roles:
			if i.name.lower() == color_fix:	
				w_role = i
				await ctx.author.add_roles(w_role)
				await ctx.respond(embed=viesti_suc)
				await update_commands("colorrole", ctx.guild)
				return
	except:
		viesti = discord.Embed(description = "Uh oh, I am missing permissions. My role might not be high enough to control color roles.", color = c)
		await ctx.respond(embed=viesti)
		return
	try:
		w_role = await ctx.guild.create_role(name=color, color=värit[color_fix])
		await w_role.edit(position=ctx.me.top_role.position - 1)
		await ctx.author.add_roles(w_role)
		await ctx.respond(embed=viesti_suc)
		await update_commands("colorrole", ctx.guild)
	except Exception as e:
		print(e)
		viesti = discord.Embed(description = "Uh oh, I am missing permissions. My role might not have permissions to manage roles..", color = c)
		await ctx.respond(embed=viesti)
		return

@bot.slash_command(name="profile", description="Send someomes profile")
async def profile(ctx, member : Option(discord.Member, "Member to show profile")):
	await open_profile(member)
	p = await get_profile(member)
	auto = discord.Embed(title = f"{member.name}'s Comfy Profile", description = p.description, color = p.color)
	auto.add_field(name='Sent',value=f"""
Hugs : {p.sent["hug"]}
Kisses : {p.sent["kiss"]}
Waves : {p.sent["wave"]}
Gifts : {p.sent["gift"]}
""")
	if member.avatar:
		auto.set_thumbnail(url=member.avatar.url)
	else:
		auto.set_thumbnail(url="https://discord.com/assets/c09a43a372ba81e3018c3151d4ed4773.png")
	auto.add_field(name="Received", value=f"""
Hugs : {p.received["hug"]}
Kisses : {p.received["kiss"]}
Waves : {p.received["wave"]}
Gifts : {p.received["gift"]}
""")
	await ctx.respond(embed=auto)
	await update_commands("profile", ctx.guild)

@bot.user_command(name="Show profile")
async def callbackname(ctx, member : discord.Member):
	await open_profile(member)
	p = await get_profile(member)
	auto = discord.Embed(title = f"{member.name}'s Comfy Profile", description = p.description, color = p.color)
	auto.add_field(name='Sent',value=f"""
Hugs : {p.sent["hug"]}
Kisses : {p.sent["kiss"]}
Waves : {p.sent["wave"]}
Gifts : {p.sent["gift"]}
""")
	if member.avatar:
		auto.set_thumbnail(url=member.avatar.url)
	else:
		auto.set_thumbnail(url="https://discord.com/assets/c09a43a372ba81e3018c3151d4ed4773.png")
	auto.add_field(name="Received", value=f"""
Hugs : {p.received["hug"]}
Kisses : {p.received["kiss"]}
Waves : {p.received["wave"]}
Gifts : {p.received["gift"]}
""")
	await ctx.respond(embed=auto)
	await update_commands("profile_user", ctx.guild)

@bot.slash_command(name="myprofile", description="Sends your own profile")
async def myprofile(ctx, description : Option(str, "Profile description", required=False, default=None), color : Option(str, "Profile Color", required=False, default=None, choices=VÄRIT_UP)):
	await open_profile(ctx.author)
	if description:
		if len(description) > 150:
			viesti = discord.Embed( description = "Uh oh, description character limit is 150. Use `/profilehelp` to see more information about profiles", color = c)
			await ctx.respond(embed=viesti, ephemeral=True)
			return
		p = await get_profile(ctx.author)
		p.description = description
		await store_profile(ctx.author, p)
	if color:
		color_fix = color.lower()
		color_save = värit[color_fix]
		p = await get_profile(ctx.author)
		p.color = color_save
		await store_profile(ctx.author, p)
	p = await get_profile(ctx.author)
	auto = discord.Embed(title = f"{ctx.author.name}'s Comfy Profile", description = p.description, color = p.color)
	auto.add_field(name='Sent',value=f"""
Hugs : {p.sent["hug"]}
Kisses : {p.sent["kiss"]}
Waves : {p.sent["wave"]}
Gifts : {p.sent["gift"]}
""")
	if ctx.author.avatar:
		auto.set_thumbnail(url=ctx.author.avatar.url)
	else:
		auto.set_thumbnail(url="https://discord.com/assets/c09a43a372ba81e3018c3151d4ed4773.png")
	auto.add_field(name="Received", value=f"""
Hugs : {p.received["hug"]}
Kisses : {p.received["kiss"]}
Waves : {p.received["wave"]}
Gifts : {p.received["gift"]}
""")
	auto.set_footer(text="/profilehelp")
	await ctx.respond(embed=auto)
	await update_commands("myprofile", ctx.guild)


#PET COMMAND SECTION

@bot.slash_command(name="pethelp", description="Sends a pet help message")
async def pethelp(ctx):
	viesti = discord.Embed(title = "Pet help message", description = "Here you can see Comfy Bots pet commands. These pets are global across servers.\n\nAvailable pets are cat, dog, bunny, squirrel, frog, turtle, elephant, polar bear, bear, tiger, mouse, sheep, chicken, rooster, monkey and pig\n\n`/pet` shows your pet.\n`/search` tries to find a pet for you.\n`/give` gives your pet away.\n`/feed` feeds food to your pet. You can buy food from `/shop`\n`/water` gives water to your pet\n`/train` spends time with your pet.\n\n**Pet Points**:four_leaf_clover:\nYou can use pet points to buy food for your pet\nYou can use `/points` to see your points.\nYou can use `/find` to get more points.\nYou can use `/shop` to see shop items and `/shop (item)` to buy the item.\nYou can use `/inventory` to see all your food\n\nIf you don't interact with your pet, it will lose health and might even die.\nYou can level up and increase happiness of your pet by interacting with it", color = green)
	await ctx.respond(embed=viesti, ephemeral=True)
	await update_commands("pethelp", ctx.guild)


@bot.slash_command(name="search", description="Search for a pet")
async def search(ctx):
	await open_bank(ctx.author, ctx)
	await open_pet(ctx.author)
	if await has_pet(ctx.author):
		viesti = discord.Embed(description = "You already have a pet!", color = green)
		await ctx.respond(embed=viesti)
		return
	n, t = await search_pet(ctx.author)
	if not n:
		viesti = discord.Embed( description = "You didn't find any pets!", color = green)
		await ctx.respond(embed=viesti)
		return
	p = await get_pet(ctx.author)
	p.name = n
	p._type = t
	await store_pet(ctx.author, p)
	current_time = int(time.time() / 60)

	await set_interaction(p.pet, current_time, ctx.author, True)

	p = await get_pet(ctx.author)

	viesti = discord.Embed( description = f"""
	Congratulations! You found {await a_or_an(p._type)} {p._type} named {p.name}!
	Use `/pet` to see pet stats!
	""", color = green)
	await ctx.respond(embed=viesti)
	await update_commands("search", ctx.guild)



@bot.slash_command(name="give", description="Give your pet away")
async def give(ctx):
	await open_bank(ctx.author, ctx)
	await open_pet(ctx.author)

	if not await has_pet(ctx.author):
		viesti = discord.Embed(description = "You don't have a pet yet! Use `/search` to get a pet!", color = green)
		await ctx.respond(embed=viesti)
		return

	p = await get_pet(ctx.author)

	await set_interaction(p.pet, 0, ctx.author, True)

	await reset_pet(ctx.author)

	viesti = discord.Embed( description = f"You succesfully reset your pet {p.name}", color = green)
	await ctx.respond(embed=viesti)
	await update_commands("give", ctx.guild)


@bot.slash_command(name="pet", description="Show your pet stats")
async def pet(ctx, name : Option(str, "Pet name", required=False, default=None)):
	await open_bank(ctx.author, ctx)
	await open_pet(ctx.author)
	if not await has_pet(ctx.author):
		viesti = discord.Embed(description = "You don't have a pet yet! Use `/search` to get a pet!", color = green)
		await ctx.respond(embed=viesti)
		return

	current_time = int(time.time() / 60)
	await decay_stats(ctx.author, current_time)

	p = await get_pet(ctx.author)
		
	await set_interaction(p.pet, current_time, ctx.author)

	p = await get_pet(ctx.author)

	if not await is_alive(ctx.author):
		await set_interaction(p.pet, 0, ctx.author, True)
		viesti = discord.Embed(description = f"Your pet {p.name} has passed away", color = green)
		await ctx.respond(embed=viesti)
		await reset_pet(ctx.author)
		return

	if name:
		if len(name) >= 15:
			viesti = discord.Embed(description = "Uh oh, name character limit is 15. Use `/pethelp` to see more information about pets", color = green)
			await ctx.respond(embed=viesti)
			return
		elif len(name) <= 1:
			viesti = discord.Embed(description = "Uh oh, name length must be above 1. Use `/pethelp` to see more information about pets", color = green)
			await ctx.respond(embed=viesti)
			return
		else:
			p = await get_pet(ctx.author)
			p.name = name
			await store_pet(ctx.author, p)

	

	p = await get_pet(ctx.author)

	viesti = discord.Embed(title = p.name, description = f"_**{await first_up(p._type)}**_", color = green)
	viesti.set_thumbnail(url=THUMBNAILS[p._type])
	viesti.add_field(name=f"Level {p.level}", value=f"Exp : {p.experience}")
	viesti.add_field(name=f"Health", value=f"{p.health}/150")
	viesti.add_field(name=f"Happiness", value=f"{p.happiness}/100")
	await ctx.respond(embed=viesti)
	await update_commands("pet", ctx.guild)

@bot.slash_command(name="feed", description="Feed your pet")
async def feed(ctx, item : Option(str, "Item to feed", choices=FOODS_UP.keys())):
	await open_bank(ctx.author, ctx)
	await open_pet(ctx.author)


	if not await has_pet(ctx.author):
		viesti = discord.Embed(description = "You don't have a pet yet! Use `/search` to get a pet!", color = green)
		await ctx.respond(embed=viesti)
		return
	
	result = await update_cooldowns(ctx.author, "feed")
	if result:
		await ctx.respond(embed=result, ephemeral=True)
		return

	item_fix = item.lower()


	b = await get_bank(ctx.author)

	if not await is_in_inventory(ctx.author, item_fix):
		viesti = discord.Embed(description = "Uh oh, you don't have that item. Use `/shop` to buy more food", color = green)
		await ctx.respond(embed=viesti)
		return
	else:
		b.inventory[item_fix] -= 1
		await store_bank(ctx.author, b)
	if item_fix == "small mushroom":
		await feed_pet(ctx.author, 100, FOODS[item_fix], 10)
	elif item_fix == "big mushroom":
		await feed_pet(ctx.author, 200, FOODS[item_fix], 10)
	elif item_fix == "watermelon":
		await feed_pet(ctx.author, 20, FOODS[item_fix], 70)
	elif item_fix == "bread":
		await feed_pet(ctx.author, 20, FOODS[item_fix], 70)
	elif item_fix == "lemon":
		await feed_pet(ctx.author, 20, FOODS[item_fix], 70)
	else:
		await feed_pet(ctx.author, 10, FOODS[item_fix], 10)

	

	current_time = int(time.time() / 60)
	try:
		await decay_stats(ctx.author, current_time)
		p = await get_pet(ctx.author)

	except KeyError:
		p = await get_pet(ctx.author)

		pet = await set_interaction(p.pet, current_time, ctx.author, True)
		
	else:
		p = await get_pet(ctx.author)
		
		await set_interaction(p.pet, current_time, ctx.author)

	await store_pet(ctx.author, p)
	p = await get_pet(ctx.author)
	if not await is_alive(ctx.author):
		viesti = discord.Embed(description = f"Your pet {p.name} has passed away", color = green)
		await ctx.respond(embed=viesti)
		await set_interaction(p.pet, 0, ctx.author, True)
		await reset_pet(ctx.author)
		return

	viesti = discord.Embed( description = f"You succesfully fed **{item_fix}** to your pet {p.name}", color = green)
	await ctx.respond(embed=viesti)
	await update_commands("feed", ctx.guild)

@bot.slash_command(name="water", description="Give water to your pet")
async def water(ctx):
	await open_bank(ctx.author, ctx)
	await open_pet(ctx.author)

	if not await has_pet(ctx.author):
		viesti = discord.Embed(description = "You dont have a pet yet!", color = green)
		await ctx.respond(embed=viesti)
		return
	result = await update_cooldowns(ctx.author, "water")
	if result:
		await ctx.respond(embed=result, ephemeral=True)
		return

	p = await get_pet(ctx.author)
	current_time = int(time.time() / 60)
	try:
		await decay_stats(ctx.author, current_time)
	except KeyError:
		await set_interaction(p.pet, current_time, ctx.author, True)
	else:
		await set_interaction(p.pet, current_time, ctx.author)

	p = await get_pet(ctx.author)
	if not await is_alive(ctx.author):
		await set_interaction(p.pet, 0, ctx.author, True)
		viesti = discord.Embed(description = f"Your pet {p.name} has passed away", color = green)
		await ctx.respond(embed=viesti)
		await reset_pet(ctx.author)
		return

	await feed_pet(ctx.author, 10, 5, 5)

	viesti = discord.Embed( description = f"You succesfully gave water to your pet {p.name}", color = green)
	await ctx.respond(embed=viesti)
	await update_commands("water", ctx.guild)


@bot.slash_command(name="train", description="Spend time with your pet")
async def train(ctx):
	await open_bank(ctx.author, ctx)
	await open_pet(ctx.author)
	
	if not await has_pet(ctx.author):
		viesti = discord.Embed(description = "You dont have a pet yet!", color = green)
		await ctx.respond(embed=viesti)
		return
	result = await update_cooldowns(ctx.author, "train")
	if result:
		await ctx.respond(embed=result, ephemeral=True)
		return

	p = await get_pet(ctx.author)
	current_time = int(time.time() / 60)
	try:
		await decay_stats(ctx.author, current_time)
	except KeyError:
		await set_interaction(p.pet, current_time, ctx.author, True)
	else:
		await set_interaction(p.pet, current_time, ctx.author)

	p = await get_pet(ctx.author)
	if not await is_alive(ctx.author):
		await set_interaction(p.pet, 0, ctx.author, True)
		viesti = discord.Embed(description = f"Your pet {p.name} has passed away", color = green)
		await ctx.respond(embed=viesti)
		await reset_pet(ctx.author)

		return
	

	await feed_pet(ctx.author, 10, 1, 20)
	await update_commands("train", ctx.guild)

	viesti = discord.Embed( description = f"You succesfully spent time with your pet {p.name}", color = green)
	await ctx.respond(embed=viesti)

@bot.slash_command(name="inventory", description="See your food inventory")
async def inventory(ctx):
	await open_bank(ctx.author, ctx)


	b = await get_bank(ctx.author)

	viesti = discord.Embed(title="Food Inventory", description = f"You can see your food here", color = green)
	index = 0
	for k, v in b.inventory.items():
		viesti.set_thumbnail(url="https://cdn.discordapp.com/attachments/900712260937322529/908763716743491584/inventory_apple.png")
		if v != 0:
			upp = await first_up(k)
			viesti.add_field(name=f"{upp} {FOODS_UP[upp]}", value=f"Amount : {v}")
			index += 1
	if index == 0:
		viesti.description = "You don't have any food! Buy them from `/shop`"

	await ctx.respond(embed=viesti)
	await update_commands("inventory", ctx.guild)



#ECONOMY COMMAND SECTION

@bot.slash_command(name="find", description="Find pet points")
async def find(ctx):
	result = await update_cooldowns(ctx.author, "find")
	if result:
		await ctx.respond(embed=result, ephemeral=True)
		return



	await open_bank(ctx.author, ctx)
	b = await get_bank(ctx.author)
	first = random.randint(1, 10)
	if first <= 6:
		amt = random.randint(20, 40)
	if first >= 7 and first <= 9:
		amt = random.randint(40, 80)
	if first == 10:
		amt = random.randint(90, 180)

	b.points += amt
	await store_bank(ctx.author, b)
	sendable = random.choice(FIND_SENTENCES)
	viesti = discord.Embed( description = sendable.replace("x", f"**{amt}**:four_leaf_clover:"), color = green)
	await ctx.respond(embed=viesti)
	await update_commands("find", ctx.guild)


@bot.slash_command(name="points", description="Show your pet points")
async def points(ctx):
	await open_bank(ctx.author, ctx)
	b = await get_bank(ctx.author)

	viesti = discord.Embed( description = f"""
	You have **{b.points}**:four_leaf_clover:
	You can use these pet points to buy from `/shop`
	""", color = green)
	await ctx.respond(embed=viesti)
	await update_commands("points", ctx.guild)

@bot.slash_command(name="shop", description="Buy food for your pet")
async def shop(ctx, item : Option(str, "Item to buy", choices=FOODS_UP.keys(), required=False, default=None)):
	await open_bank(ctx.author, ctx)
	b = await get_bank(ctx.author)

	if item:
		item_fix = item.lower()
		cost = FOODS[item_fix]
		if cost == 15:
			cost = 30
		elif cost == 30:
			cost = 60
		elif cost == 40:
			cost = 80
		elif cost == 65:
			cost = 130
		elif cost == 10:
			cost = 200
		elif cost == 20:
			cost = 400
		if item_fix == "watermelon" or item_fix == "bread" or item_fix == "lemon":
			cost = 150
		

		
		if b.points >= cost:
			result = await update_cooldowns(ctx.author, "shop")
			if result:
				await ctx.respond(embed=result, ephemeral=True)
				return
			b.points -= cost
			b.inventory[item_fix] += 1
			await store_bank(ctx.author, b)
			viesti = discord.Embed(description = f"You succesfully bought **{item_fix}**. Use `/feed` to give it to your pet", color = green)
			await ctx.respond(embed=viesti)
			await update_commands("shop", ctx.guild)
			return
		else:
			viesti = discord.Embed(description = f"Uh oh, you don't have enough points. Use `/find` to get more points", color = green)
			await ctx.respond(embed=viesti)
			return
		
	viesti = discord.Embed(title = "Pet Point Shop", description = f"Here you can buy food for your pet", color = green)
	viesti.add_field(name="Circle fruit :green_circle: ", value="""
	15 health boost
	**30**:four_leaf_clover:
	""")
	viesti.add_field(name="Triangle fruit :small_red_triangle:", value="""
	30 health boost
	**60**:four_leaf_clover:
	""")
	viesti.add_field(name="Square fruit :purple_square:", value="""
	40 health boost
	**80**:four_leaf_clover:
	""")
	viesti.add_field(name="Star fruit :star:", value="""
	65 health boost
	**130**:four_leaf_clover:
	""")
	viesti.add_field(name="Small Mushroom :mushroom:", value="""
	100 xp boost
	**200**:four_leaf_clover:
	""")
	viesti.add_field(name="Big Mushroom :mushroom:", value="""
	200 xp boost
	**400**:four_leaf_clover:
	""")
	viesti.add_field(name="Watermelon :watermelon:", value="""
	70 happiness boost
	**150**:four_leaf_clover:
	""")
	viesti.add_field(name="Bread :bread:", value="""
	70 happiness boost
	**150**:four_leaf_clover:
	""")
	viesti.add_field(name="Lemon :lemon:", value="""
	70 happiness boost
	**150**:four_leaf_clover:
	""")
	viesti.set_thumbnail(url="https://cdn.discordapp.com/attachments/900712260937322529/908351036467597394/shop.png")
	await ctx.respond(embed=viesti)
	await update_commands("shop", ctx.guild)

#FUNCTIONS

async def update_guild_count():
	if bot.user.id in TEST_IDS:
		print("Logged in under a TEST_ID, not posting guild count to discord bot list.")
		return
	headers = {'Authorization': DBL_TOKEN}
	data = {'server_count': len(bot.guilds)}
	api_url = 'https://top.gg/api/bots/' + str(bot.user.id) + '/stats'
	async with aiohttp.ClientSession() as session:
		await session.post(api_url, data=data, headers=headers)
	print("Posted guild count to discord bot list")

async def set_interaction(p, time_, member, i=None):
	data = await get_pet_data()
	if not i:
		data[str(member.id)]["pet"]["last_interactions"]["health_interaction"] = time_
		data[str(member.id)]["pet"]["last_interactions"]["fun_interaction"] = time_
	else:
		data[str(member.id)]["pet"]["last_interactions"] = {
			"health_interaction" : time_,
			"fun_interaction" : time_
		}
	await dump_pet_data(data)


async def decay_stats(member, current_time):
	data = await get_pet_data()
    # Times are in floored minutes
	saturation_difference = current_time - data[str(member.id)]["pet"]["last_interactions"]["health_interaction"]
	cleanliness_difference = current_time - data[str(member.id)]["pet"]["last_interactions"]["fun_interaction"]



	if (cleanliness_difference / 60) >= 4:
		subtract = int(cleanliness_difference / 20) # 20

		data[str(member.id)]["pet"]["happiness"] -= subtract
	else:
		subtract = int(cleanliness_difference / 15) # 10

		data[str(member.id)]["pet"]["happiness"] -= subtract


	# Less stat decay if they haven't been online in a while, maybe they were asleep
	if (saturation_difference / 60) >= 4:
        # Reduce their stat by 1 for every 30 min since they have fed their pet
		if data[str(member.id)]["pet"]["happiness"] <= 0:
			subtract = int(saturation_difference / 20) #15

			data[str(member.id)]["pet"]["health"] -= subtract
		else:
			subtract = int(saturation_difference / 35) # 25

			data[str(member.id)]["pet"]["health"] -= subtract

	else:
		if data[str(member.id)]["pet"]["happiness"] <= 0:
			subtract = int(saturation_difference / 20) #15

			data[str(member.id)]["pet"]["health"] -= subtract


		else:
			subtract = int(saturation_difference / 25)
			data[str(member.id)]["pet"]["health"] -= subtract




    # Set all stats to 0 so they don't stay negative
	if data[str(member.id)]["pet"]["health"] < 0:
		data[str(member.id)]["pet"]["health"] = 0
	if data[str(member.id)]["pet"]["happiness"] < 0:
		data[str(member.id)]["pet"]["happiness"] = 0

	await dump_pet_data(data)





async def is_alive(member):
	p = await get_pet(member)
	if p.health <= 0:
		return False
	return True

async def first_up(text):
	fixed_name_t = text[0]
	rest = text[1:]
	fixed_name = f"{fixed_name_t.upper()}{rest}"
	return fixed_name

async def is_in_inventory(member, item):
	b = await get_bank(member)
	if b.inventory[item] == 0:
		return False
	return True

async def feed_pet(member, exp_amount, health_amount, ha_amount):
	p = await get_pet(member)

	p.experience += exp_amount
	p.health += health_amount
	p.happiness += ha_amount
	if p.health > 150:
		p.health = 150
	if p.happiness > 100:
		p.happiness = 100

	await store_pet(member, p)

	e, l = await level_up(member)
	await store_pet(member, pet_account(name=False, _type=False, health=False, happiness=False, experience=e, level=l, pet=False))


async def level_up(member):
	p = await get_pet(member)

	lvl_end = int(p.experience ** (1/4))

	if p.level < lvl_end:
		p.level = lvl_end
	return p.experience, p.level
	

async def random_type(p_value):
	if p_value <= 10:
		return None
	elif p_value >= 11 and p_value <= 50:
		return random.choice(PETS_1)
	elif p_value >= 51 and p_value <= 80:
		return random.choice(PETS_2)
	elif p_value >= 81:
		return random.choice(PETS_3)

async def search_pet(member):
	p_value = random.randint(1, 100)
	t = await random_type(p_value)
	n = random.choice(PET_NAMES)
	if not t:
		return False, False
	return n, t

async def reset_pet(member):
	data = await get_pet_data()
	u = str(member.id)
	data[u]["pet"]["name"] = ""
	data[u]["pet"]["health"] = 150
	data[u]["pet"]["type"] = ""
	data[u]["pet"]["experience"] = 0
	data[u]["pet"]["level"] = 1
	data[u]["pet"]["happiness"] = 100
		
	await dump_pet_data(data)


async def has_pet(member):
	p = await get_pet(member)
	if p.name == "":
		return False
	return True

async def a_or_an(text):
	vowels = ("a", "e", "i", "o", "u", "A", "E", "I", "O", "U")
	return "an" if text[0] in vowels else "a"

async def get_command_data():
	with open('../files/json/command_usage.json', 'r') as f:
		data = json.load(f)
		return data

async def dump_command_data(data):
	with open('../files/json/command_usage.json', 'w') as f:
		return json.dump(data, f, indent=4)

async def get_pet_data():
	with open('../files/json/pet_data.json', 'r') as f:
		data = json.load(f)
		return data

async def dump_pet_data(data):
	with open('../files/json/pet_data.json', 'w') as f:
		return json.dump(data, f, indent=4)

async def get_bank_data():
	with open('../files/json/bank_data.json', 'r') as f:
		data = json.load(f)
		return data

async def dump_bank_data(data):
	with open('../files/json/bank_data.json', 'w') as f:
		return json.dump(data, f, indent=4)

async def get_profile_data():
	with open('../files/json/profile_data.json', 'r') as f:
		data = json.load(f)
		return data

async def dump_profile_data(data):
	with open('../files/json/profile_data.json', 'w') as f:
		return json.dump(data, f, indent=4)

async def update_commands(command, guild):
	data = await get_command_data()

	g_string = f"'{guild.id}','{guild.name}'"
	if command not in data:
		data[command] =  {}
	if g_string not in data[command]:
		data[command][g_string] = 0
	data[command][g_string] += 1
	await dump_command_data(data)

async def open_pet(member):
	data = await get_pet_data()
	g = str(member.guild.id)
	u = str(member.id)
	if u in data:
		return False
	data[u] = {}
	data[u]["pet"] = {}
	data[u]["pet"]["name"] = ""
	data[u]["pet"]["health"] = 150
	data[u]["pet"]["type"] = ""
	data[u]["pet"]["experience"] = 0
	data[u]["pet"]["level"] = 1
	data[u]["pet"]["happiness"] = 100
	data[u]["pet"]["last_interactions"] = {}
		
	await dump_pet_data(data)
	return True

async def open_bank(member, ctx):
	data = await get_bank_data()
	g = str(ctx.guild.id)
	u = str(member.id)
	if u in data:
		return False
	data[u] = {}
	data[u]["points"] = 0
	data[u]["inventory"] = {}
	for i in FOODS.keys():
		data[u]["inventory"][i] = 0

		
	await dump_bank_data(data)
	return True

async def open_profile(member):
	data = await get_profile_data()
	g = str(member.guild.id)
	u = str(member.id)
	if u in data:
		return False
	data[u] = {}
	data[u]["profile"] = {}
	data[u]["profile"]["description"] = "This is my default Comfy Profile!"
	data[u]["profile"]["sent"] = {}
	data[u]["profile"]["sent"] = {"hug" : 0, "kiss" : 0, "wave" : 0, "gift" : 0}
	data[u]["profile"]["received"] = {}
	data[u]["profile"]["received"] = {"hug" : 0, "kiss" : 0, "wave" : 0, "gift" : 0}
	data[u]["profile"]["color"] = pink
		
	await dump_profile_data(data)

async def get_profile(member):
	data = await get_profile_data()
	g = str(member.guild.id)
	u = str(member.id)
	s = data[u]["profile"]["sent"]
	r = data[u]["profile"]["received"]
	d = data[u]["profile"]["description"]
	cu = data[u]["profile"]["color"]
	return profile_account(sent=s, received=r, description=d, color=cu)

async def get_bank(member):
	data = await get_bank_data()
	g = str(member.guild.id)
	u = str(member.id)
	p = data[u]["points"]
	i = data[u]["inventory"]
	return bank_account(points=p, inventory=i)


async def get_pet(member):
	data = await get_pet_data()
	g = str(member.guild.id)
	u = str(member.id)
	n = data[u]["pet"]["name"]
	h = data[u]["pet"]["health"]
	ha = data[u]["pet"]["happiness"]
	t = data[u]["pet"]["type"]
	e = data[u]["pet"]["experience"]
	l = data[u]["pet"]["level"]
	p = data[u]["pet"]
	return pet_account(name=n, health=h, happiness=ha, _type=t, experience=e, level=l, pet=p)


async def store_pet(member, objekti, i=False):
	data = await get_pet_data()
	g = str(member.guild.id)
	u = str(member.id)
	if objekti.name != False: 
		data[u]["pet"]["name"] = objekti.name
	if objekti.health != False:
		data[u]["pet"]["health"] = objekti.health
	if objekti.happiness != False:
		data[u]["pet"]["happiness"] = objekti.happiness
	if objekti._type != False:
		data[u]["pet"]["type"] = objekti._type
	if objekti.experience != False:
		data[u]["pet"]["experience"] = objekti.experience
	if objekti.level != False:
		data[u]["pet"]["level"] = objekti.level
	if i and objekti.pet != False:
		data[u]["pet"] = objekti.pet
	await dump_pet_data(data)

async def store_bank(member, objekti):
	data = await get_bank_data()
	g = str(member.guild.id)
	u = str(member.id)
	if objekti.points != False:
		data[u]["points"] = objekti.points
	if objekti.inventory != False:
		data[u]["inventory"] = objekti.inventory
	await dump_bank_data(data)
	
async def store_profile(member, objekti):
	data = await get_profile_data()
	g = str(member.guild.id)
	u = str(member.id)
	if objekti.sent != False:
		data[u]["profile"]["sent"] = objekti.sent
	if objekti.received != False:
		data[u]["profile"]["received"] = objekti.received
	if objekti.description != False:
		data[u]["profile"]["description"] = objekti.description
	if objekti.color != False:
		data[u]["profile"]["color"] = objekti.color
	await dump_profile_data(data)

async def add_profile(author, member, item):
	data = await get_profile_data()
	g = str(member.guild.id)
	u = str(member.id)
	ua = str(author.id)
	p = await get_profile(member)
	p.received[item] += 1
	pa = await get_profile(author)
	pa.sent[item] += 1

	await store_profile(member, profile_account(sent=False, received=p.received, description=False, color=False))

	await store_profile(author, profile_account(sent=pa.sent, received=False, description=False, color=False))

async def update_cooldowns(member, command):
	member_id = member.id
	curr_time = int(time.time())
	if member_id not in custom_cooldowns.keys():
		custom_cooldowns[member_id] = {}
	if command not in custom_cooldowns[member_id].keys():
		custom_cooldowns[member_id][command] = curr_time
	else:
		new_time = curr_time - custom_cooldowns[member_id][command]
		cooldown_seconds = cooldowns[command]
		if new_time < cooldown_seconds:
			show = cooldown_seconds - new_time
			viesti = discord.Embed( description = f"This command is on cooldown!\n**{show}s** left until you can use again", color = green)
			return viesti
		custom_cooldowns[member_id][command] = curr_time
	return False


#BOT RUN

bot.run(TOKEN)

