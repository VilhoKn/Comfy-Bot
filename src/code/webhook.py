from dhooks import Webhook, Embed
import asyncio
async def send_webhook(g, b, t, w):
	
	hook = Webhook(w)
	
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
	if not t:
		embed.title = f"{g.name}"
		embed.color = 0xff000d
		

	hook.send(embed=embed)

