import discord
from checker import replaychecker
from discord.ext import commands
from checkeradv import replaycheckeradv

client = commands.Bot(command_prefix = '$$')


@client.event
async def on_ready():
    print("bot is go")


@client.command()
async def deathtoll(ctx,*,url):
    f = replaychecker(url)
    str(f)
    print(f)
    print("aa")
    await ctx.send(f"{f}")

@client.command()
async def kills(ctx,*,url):
    battle = replaycheckeradv(url)
    team1 = ", ".join(battle.team1)
    team2 = ", ".join(battle.team2)
    kill_logs = "\n".join(battle.kill_logs)
    embed = discord.Embed(title=f"{battle.p1} vs {battle.p2}", url=url)
    embed.add_field(name=f"{battle.p1}'s team", value=team1)
    embed.add_field(name=f"{battle.p2}'s team", value=team2)
    embed.add_field(name="Kills", value=kill_logs)

    print("aa")
    await ctx.send(content=None, embed=embed)

@client.command()
async def ping(ctx):

    await ctx.send("pong")

client.run("NTkwNTU5NjA5MjUzNTI3NTgy.XQkAJQ.f3zEdsqOQonql6-TXq83K0_4HFc")
