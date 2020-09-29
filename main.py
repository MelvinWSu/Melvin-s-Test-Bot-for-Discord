# bot.py
import os
import random

import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='!')

#Discord functions
class DiscordCmd(commands.Cog):
    @commands.command(name='create_channel', help='Create a new channel')
    @commands.has_role('Admin')
    @commands.guild_only()
    async def create_channel(ctx, channel_name=None):
        if not channel_name:
            await ctx.send('Name paramter for creating a channel needed')
        else:
            guild = ctx.guild
            print(f'Creating channel: ' + channel_name)
            existing_channel = discord.utils.get(guild.channels, name=channel_name)
            if existing_channel:
                print (f'Channel already exist')
                await ctx.send('Channel already exist')
            if not existing_channel:
                print(f'Creating a new channel: {channel_name}')
                await guild.create_text_channel(channel_name)
                await ctx.send('Channel ' + channel_name + " created")

    @commands.command(name='send_guild_message',help='Have the bot send a message to the given channel')
    @commands.has_role('Admin')
    @commands.guild_only()
    async def send_guild_message(ctx, channel_name = None, message = "a"):
        if not channel_name:
            await ctx.send('Name paramter for channel to send message to')
        else:
            guild = ctx.guild
            existing_channel = discord.utils.get(guild.channels, name=channel_name)
            if not existing_channel:
                await ctx.send('Channel does not exist')
            else:
                await existing_channel.send(message)

    @commands.command(name='send_dm',help='Have the bot send a direct message to the given user')
    @commands.has_role('Admin')
    @commands.guild_only()
    async def send_dm(ctx, username = None, message = "a"):
        if not username:
            await ctx.send('Name paramter for user to send message to')
        else:
            guild = ctx.guild
            member_username = discord.utils.get(guild.members, name=username)
            if not member_username:
                await ctx.send('User is not in the guild')
            else:
                await member_username.send(message)

    @commands.command(name='kick_user', help='Kick the user!')
    @commands.has_role('Admin')
    @commands.guild_only()
    async def kick_user(ctx, username=None, reason="a"):
        print("user: " + username)
        print("reason: " + reason)
        if not username:
            await ctx.send('Name paramter for user to kick')
        else:
            guild = ctx.guild
            member_username = discord.utils.get(guild.members, name=username)
            if not member_username:
                await ctx.send('User is not in the guild')
            else:
                await kick(member_username, reason)

##########################################################

#api functions
class simpleFunctions(commands.Cog):
    @commands.command(name='99', help='Responds with a random quote from Brooklyn 99')
    async def nine_nine(ctx):
        brooklyn_99_quotes = [
            'I\'m the human form of the 💯 emoji.',
            'Bingpot!',
            (
                'Cool. Cool cool cool cool cool cool cool,\n'
                'no doubt no doubt no doubt no doubt.'
            ),
        ]

        response = random.choice(brooklyn_99_quotes)
        await ctx.send(response)

    @commands.command(name='roll_dice', help='Simulates rolling dice.')
    @commands.guild_only()
    async def roll(ctx, number_of_dice: int, number_of_sides: int):
        dice = [
            str(random.choice(range(1, number_of_sides + 1)))
            for _ in range(number_of_dice)
        ]
        await ctx.send(', '.join(dice))

##########################################################

#bot debugging
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.errors.CheckFailure):
        await ctx.send('error')

bot.add_cog(DiscordCmd(bot))
bot.add_cog(simpleFunctions(bot))
bot.run(TOKEN)