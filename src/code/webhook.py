from dhooks import Webhook, Embed
import asyncio
async def send_webhook(g, b, t):
	
	hook = Webhook("https://discord.com/api/webhooks/911031528337850388/4BG6nqFvrXEI0Se08_V3OQm9KoBL6NzBOHJiAqk6-_fxhpsGXrAuALkEiQ_ZPTijf88i")
	
	embed = Embed(
		title=g.name,
		color=0xf774b0
	)
	try:
		embed.description=f"{g.id}, Count: {g.member_count}"
	except:
		embed.description=f"{g.id}, Count: ERROR"
	if g.icon:
		embed.set_thumbnail(g.icon.url)
	embed.add_field(name="Count", value=len(b.guilds))
	total_mem = 0
	for i in b.guilds:
		try:
			total_mem += i.member_count
		except Exception as e:
			print(e)
	embed.add_field(name="Total users", value=str(total_mem))
	if t:
		gg = []
		for i in b.guilds:
			gg.append(i.name)
		ggg = "\n".join(gg)
		embed.add_field(name="Guilds", value=ggg)
	else:
		embed.title = f"{g.name}"
		embed.color = 0xff000d

	hook.send(embed=embed)

