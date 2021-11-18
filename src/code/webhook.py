from dhooks import Webhook, Embed
import asyncio
async def send_webhook(g, b, t):
	
	hook = Webhook("https://discord.com/api/webhooks/906158150456082433/3-yK_3w4K17S6gTzqcY-kFPuWPQUIw6hhh2k13rpK8sWCrA6hatG7B7W_4FK3d1zp-8q")
	
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
	if t:
		try:
			gg = [f"{q.name}, '{g.member_count}'" for q in b.guilds]
		except:
			gg = [f"{q.name}, 'ERROR'" for q in b.guilds]
		ggg = "\n".join(gg)
		embed.add_field(name="Guilds", value=ggg)
	else:
		embed.title = f"{g.name}"
		embed.color = 0xff000d

	hook.send(embed=embed)

