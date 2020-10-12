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
    async def create_channel(self, ctx, channel_name=None):
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
    async def send_guild_message(self, ctx, channel_name = None, message = "a"):
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
    async def send_dm(self, ctx, username = None, message = "a"):
        if not username:
            await ctx.send('Name paramter for user to send message to')
        else:
            guild = ctx.guild
            member_username = discord.utils.get(guild.members, name=username)
            if not member_username:
                await ctx.send('User is not in the guild')
            else:
                await member_username.send(message)

    @commands.command(name='k', help='Kick the user!')
    @commands.has_role('Admin')
    @commands.guild_only()
    async def kick(self, ctx, username = None, reason = None):
        if not username:
            await ctx.send('Name paramter needed to kick someone')
        else:
            guild = ctx.guild
            member_username = discord.utils.get(guild.members, name = username)
            await member_username.kick(reason=reason)
            await ctx.send(f'User {member_username} has been kicked')

    @commands.command(name='b', help='Ban the user!')
    @commands.has_role('Admin')
    @commands.guild_only()
    #to-do: reason, delete_message_days
    async def ban(self, ctx, username=None, reason = None, days_remove = 1):
        if not username:
            await ctx.send('Name paramter needed to ban someone')
        else:
            guild = ctx.guild
            member_username = discord.utils.get(guild.members, name=username)
            await member_username.ban(reason=reason, delete_message_days = days_remove)
            await ctx.send(f'User {member_username} has been banned')

    @commands.command(name='ub', help='Unban the user!')
    @commands.has_role('Admin')
    @commands.guild_only()
    #to-do: reason
    async def unban(self, ctx, username=None):
        if not username:
            await ctx.send('Name paramter needed to unban someone')
        else:
            guild = ctx.guild
            ban_list = await ctx.guild.bans()
            for username in ban_list:
                print(username)
                user = username.user
                print(user)
                await guild.unban(user)
                await ctx.send(f'User {user} has been unbanned')

    @commands.command(name='nn', help='Change nickname of user')
    @commands.has_role('Admin')
    @commands.guild_only()
    async def change_nickname(self, ctx, username=None, name=None, reason=None):
        if not username:
            await ctx.send('Name paramter needed')
        else:
            guild = ctx.guild
            member_username = discord.utils.get(guild.members, name=username)
            if name:
                await member_username.edit(nick=name, reason=reason)
                await ctx.send(f'{member_username} renamed to {name}')
            else:
                await member_username.edit(nick=None, reason=reason)
                await ctx.send(f'Removed {member_username}\'s nickname')

    @commands.command(name='ra', help='Add role to user')
    @commands.has_role('Admin')
    @commands.guild_only()
    #role must already exist in server before assigning
    async def add_role(self, ctx, username=None, role=None, reason=None):
        if not username:
            await ctx.send('Name paramter needed')
        else:
            guild = ctx.guild
            desired_role = discord.utils.get(guild.roles, name=role)
            if not desired_role:
                await ctx.send(f'Role not found')
            else:
                member_username = discord.utils.get(guild.members, name=username)
                await member_username.add_roles(desired_role, reason=reason)
                await ctx.send(f'added role {role} to {member_username}')

    @commands.command(name='rr', help='Remove role from user')
    @commands.has_role('Admin')
    @commands.guild_only()
    async def remove_role(self, ctx, username=None, role=None, reason=None):
        if not username:
            await ctx.send('Name paramter needed')
        else:
            guild = ctx.guild
            desired_role = discord.utils.get(guild.roles, name=role)
            if not desired_role:
                await ctx.send(f'Role not found')
            else:
                member_username = discord.utils.get(guild.members, name=username)
                await member_username.remove_roles(desired_role,reason=reason)
                await ctx.send(f'removed role {role} from {member_username}')

##########################################################

#api functions
class simpleFunctions(commands.Cog):
    @commands.command(name='99', help='Responds with a random quote from Brooklyn 99')
    async def nine_nine(self, ctx):
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
    async def roll(self, ctx, number_of_dice: int, number_of_sides: int):
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