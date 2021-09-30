import discord
from discord.ext import commands
import youtube_dl
import config


class music(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def join(self, ctx):
        await ctx.channel.purge(limit=1)
        if ctx.author.voice is None:
            await ctx.send('А кому я петь буду?! Зайди в войс сначала')
        voice_channel = ctx.author.voice.channel
        if ctx.voice_client is None:
            await voice_channel.connect()
        else:
            await ctx.voice_client.move_to(voice_channel)

    @commands.command()
    async def leave(self, ctx):
        await ctx.channel.purge(limit=1)
        await ctx.voice_client.disconnect()


    @commands.command()
    async def play(self, ctx, url):
        if ctx.author.voice is None:
            await ctx.send('А кому я петь буду?! Зайди в войс сначала')
        voice_channel = ctx.author.voice.channel
        if ctx.voice_client is None:
            await voice_channel.connect()
        else:
            await ctx.voice_client.move_to(voice_channel)
        FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
                          'options': '-vn'}
        YDL_OPTIONS = {'format': 'bestaudio'}
        vc = ctx.voice_client

        with youtube_dl.YoutubeDL(YDL_OPTIONS) as ydl:
            info = ydl.extract_info(url, download = False)
            url2 = info['formats'][0]['url']
            source = await discord.FFmpegOpusAudio.from_probe(url2, **FFMPEG_OPTIONS)
            vc.play(source)

    @commands.command()
    async def pause(self, ctx):
        await ctx.channel.purge(limit = 1)
        await ctx.send('Музыка приостановлена ⏸️')
        await ctx.voice_client.pause()


    @commands.command()
    async def resume(self, ctx):
        await ctx.channel.purge(limit=1)
        await ctx.send('Музыка продолжена ▶️')
        await ctx.voice_client.resume()



def setup(client):
    client.add_cog(music(client))
