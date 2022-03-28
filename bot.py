#Don't Change Any Information Unless Clearly Stated Something Goes There

import opensql
import nextcord
from nextcord.ext import commands

intents = nextcord.Intents.default()
intents.members = True

db = opensql.ODB("Insert opensql key here...")
print("Database connected!")

def exists(guild_id):
    res = db.query(f"SELECT * FROM channelSave WHERE guild_id = {guild_id}")
    return not not res

client = commands.Bot(command_prefix="auto!",intents=intents)

@client.command()
async def sponsor(ctx):
    await ctx.send(f"Server Hoster/Sponsors here")

@client.command()
@commands.has_permissions(manage_channels=True)
async def set(ctx,channel:nextcord.TextChannel=None):
    
    if not channel:
        return await ctx.reply("Remember to # a channel!")
    if exists(ctx.guild.id):
        res = db.query(f"UPDATE channelSave SET channel_id={channel.id} WHERE guild_id LIKE {ctx.guild.id}")
        if res == []:
            await channel.send("New Members will be Auto-Pinged here!")
        else:await ctx.send(f':x: Failed: {res["error"]}')
    else:
        res = db.query(f"INSERT INTO channelSave VALUES({ctx.guild.id},{channel.id})")

@client.command()
@commands.has_permissions(manage_channels=True)
async def remove(ctx):
    if exists(ctx.guild.id):
        res = db.query(f"DELETE FROM channelSave WHERE guild_id LIKE {ctx.guild.id}")
        if res == []:
            await ctx.send("AutoPing disabled!")
        else:
            await ctx.send(f':x: Failed: {res["error"]}')
    else:
       	res = {"error":"This Guild has no Channel Set!"}

@client.command()
async def find(ctx):
    if exists(ctx.guild.id):
        res = db.query(f"SELECT channelSave.channel_id FROM channelSave WHERE guild_id LIKE {ctx.guild.id}")
        if res == []:
            channel = client.get_channel(res[0])
            await ctx.send(f"AutoPing is set in {channel.mention}!")
        else:
            await ctx.send(f':x: Failed: {res["error"]}')
    else:
       	res = {"error":"This Guild has no Channel Set!"}

@client.event
async def on_member_join(member):
    print("Member Joined")
    if exists(member.guild.id):
        res = db.query(f"SELECT channelSave.channel_id FROM channelSave WHERE guild_id LIKE {member.guild.id}")
        
        if isinstance(res,list):
            channel = client.get_channel(res[0])
            m = await channel.send(member.mention)
            await m.delete()
        else:
        	print(res)
    else:
        print("Member joined guild, but no channel was set")

@client.command()
async def sql(ctx,*,code):
    await ctx.send(db.query(code))

@client.event
async def on_ready():
    print("Discord Connected")
    print(f"Logged in as {client.user} ({client.user.id})")
        
client.run("TOKEN GOES HERE")
