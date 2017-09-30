from discord.ext import commands
import discord
import asyncio


class Quote:
    """Quote a message by adding the reaction!"""

    def __init__(self, bot):
        self.bot = bot

    async def quote_message(self, message, requestor=None, ctx=None):
        embed_args = {
            'description': message.content,
            'colour': message.author.colour,
            'timestamp': message.created_at,
        }
        embed = discord.Embed(**embed_args)
        embed.set_author(name=message.author.display_name, icon_url=message.author.avatar_url)
        if requestor:
            embed.set_footer(text="Requested by: {}".format(requestor.name))

        if message.content == "" or message.content is None:
            embed.set_image(url=message.attachments[0].url)

        if ctx:
            target = ctx
        else:
            target = message.channel

        await target.send(embed=embed)
        await message.add_reaction('\U0001f44d')

    async def on_reaction_add(self, reaction, user):
        try:
            if reaction.emoji == self.bot.quote_emote and not user.bot and reaction.count == 1:
                await self.quote_message(reaction.message, requestor=user)
        except Exception as e:
            self.bot.log(e)

    @commands.command(name='id')
    async def id_command(self, ctx, *, message_id):
        """Quote a message with a specific Message ID in the current channel"""
        try:
            message = await ctx.channel.get_message(int(message_id))
            await self.quote_message(message, requestor=ctx.author)
        except Exception as e:
            self.bot.log(e)
            await ctx.send("I couldn't find a message with that ID, sorry :(")

    @commands.command(name='user')
    async def user_command(self, ctx, *, user : discord.Member):
        """Quote the last message from a specific user in the current channel"""
        message = None
        async for m in ctx.channel.history(limit=None, before=ctx.message, reverse=False):
            if m.author == user:
                message = m
                break
        if message:
            await self.quote_message(message, ctx=ctx, requestor=ctx.author)
        else:
            await ctx.send("I couldn't find the last message {} sent, sorry :(".format(user.name))


def setup(bot):
    bot.add_cog(Quote(bot))
