import discord
from discord.ext import commands
import music
from googleapiclient.discovery import build
import config
import levelsys
import random
import giphy_client
from giphy_client.rest import ApiException

cogs = [music]
cgs = [levelsys]
client = commands.Bot(command_prefix=config.PREFIX, intents =
discord.Intents.all())
client.remove_command('help')
api_key = "AIzaSyBqNFovxFdMiHNYeYk1HA0hNqvgspRepSY"

@client.command(pass_context = True)
async def roll(ctx):
    random_number = random.randint(0, 100)
    await ctx.send(f'Ролл: {random_number}')

@client.command(pass_context=True)
async def showpic(ctx, *, search):
    ran = random.randint(0, 9)
    resource = build("customsearch", "v1", developerKey=api_key).cse()
    result = resource.list(
        q=f"{search}", cx="74b5169e7839f827e", searchType="image"
    ).execute()
    url = result["items"][ran]["link"]
    embed1 = discord.Embed(title=f"Я тут слегка порылся в ящике, вот то что ты просил ({search})")
    embed1.set_image(url=url)
    await ctx.send(embed=embed1)


@client.command(pass_context=True)
async def help(ctx):
    await ctx.channel.purge(limit=1)
    emb = discord.Embed(title='Помощь на месте')
    emb.add_field(name='{}clear'.format(config.PREFIX), value='Очистка n-го количества компромата')
    emb.add_field(name='{}kick'.format(config.PREFIX), value='Убираем свидетелей')
    emb.add_field(name='{}ban'.format(config.PREFIX), value='Серёга!А серёги больше нет...(Бан)')
    emb.add_field(name='{}hello'.format(config.PREFIX), value='Приветствие')
    emb.add_field(name='{}info'.format(config.PREFIX), value='Информация о боте')
    emb.add_field(name='{}showpic'.format(config.PREFIX), value='Поиск картинки по названию')
    emb.add_field(name='{}deadinside'.format(config.PREFIX), value='1000-7')
    emb.add_field(name='{}roll'.format(config.PREFIX), value='Рандом числа от 1 до 100')
    emb.add_field(name='{}join'.format(config.PREFIX), value='Бот заходит в войс')
    emb.add_field(name='{}play'.format(config.PREFIX), value='Проигрывание музыки по ссылке с ютуба')
    emb.add_field(name='{}pause'.format(config.PREFIX), value='Ставит проигрование на паузу')
    emb.add_field(name='{}resume'.format(config.PREFIX), value='Продолжает проигрование')
    emb.add_field(name='{}showgif'.format(config.PREFIX), value = 'Поиск гифки по названию')
    await ctx.send(embed=emb)


@client.command(pass_context=True)
@commands.has_permissions(kick_members=True)
async def clear(ctx, amount=0):
    if amount == 0:
        amount = 1
        await ctx.channel.purge(limit=amount)
        await ctx.send(f'{ctx.message.author.mention}, ну и сколько я по твоему должен удалить, а? Впиши количество!')
    else:
        await ctx.channel.purge(limit=amount+1)
        await ctx.send(f'Я нахуй удалил {amount} сообщений')


@client.command(pass_context=True)
async def hello(ctx, amount=1):
    await ctx.channel.purge(limit=amount)
    author = ctx.message.author
    await ctx.send(f'Опачки, ать, {author.mention}! Дарова ёпта, я Круть, дискорд бот')


@client.command(pass_context=True)
async def deadinside(ctx):
    print(ctx)
    await ctx.channel.purge(limit=1)
    i = 1000
    while i > 0:
        k = i
        i -= 7
        await ctx.send(f'{k}-7 ={i}')

@client.command(pass_context = True)
async def showgif(ctx, *, q = 'Smile'):

    api_key = '0rN4DtOylokGA8WKqqy1u9GnORBAeRfc'
    api_istance = giphy_client.DefaultApi()
    try:
        api_responce = api_istance.gifs_search_get(api_key, q, limit = 5, rating = 'r')
        lst = list(api_responce.data)
        giff = random.choice(lst)
        embs = discord.Embed(title = f'Я тут слегка порылся в ящике, вот то что ты просил {q}')
        embs.set_image(url = f'https://media.giphy.com/media/{giff.id}/giphy.gif')

        await ctx.channel.send(embed = embs)
    except ApiException as e:
        print("Exeption when calling Api")

@client.command(pass_context=True)
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason=None):
    await ctx.channel.purge(limit=1)
    await member.kick(reason=reason)
    await ctx.send(f'{member.mention} в сделку не входил...')


@client.command(pass_context=True)
async def info(ctx):
    await ctx.channel.purge(limit=1)
    emb = discord.Embed(title='Я бот Круть.',
                        description='Дарова ёпта, я бот созданный для того, что бы в мир полон боли и отчаяния привносить немного добра и сделать его забавнее.\nТех поддержка: [гений](https://www.instagram.com/antioxia228/)\nСупер ровный чел: [Паша](https://www.instagram.com/supavkik/)\nПросто ровный чел: [чел](https://www.instagram.com/mbreddd/)\n\nНакормить создателя: 5375414111451976',
                        colour=discord.Color.blurple(), url='https://www.instagram.com/kveys_/')
    emb.set_thumbnail(url=client.user.avatar_url)
    emb.add_field(name='Моя версия:', value='1.4.8.8')
    emb.add_field(name='Моё имя:', value=client.user.name)
    emb.add_field(name='Мой создатель', value='[Slava Aysa](https://www.instagram.com/slava_aysa/)')
    emb.set_image(url="https://wallpapercave.com/wp/wp9068045.jpg")
    await ctx.send(embed=emb)


@client.command(pass_context=True)
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason=None):
    await ctx.channel.purge(limit=1)
    emb = discord.Embed(title='Ого, менше 60%', colour=discord.Color.red())
    await member.ban(reason=reason)
    emb.set_author(name=member.name, icon_url=member.avatar_url)
    emb.add_field(name='Ідемо дальші', value=f'{member.mention} полёг в неравной битве с Володей')
    await ctx.send(embed=emb)


bad_words = ['@everyone', '@here']
hello_words = ['дарова', 'hello', 'hi', 'привет', 'здарова', 'добрый вечер', 'добрый день', 'доброе утро',
               'вечер добрый', 'утро доброе', 'день добрый', 'gm']
answer_words = ['информация о сервере', 'какие команды', 'команды сервера', 'что ты умеешь', 'что ты можешь',
                'хули доебался']
goodbye_words = ['goodbye', 'bye-bye', 'bye bye', 'bye', 'bb', 'пока', 'отъебись', 'отьебись', 'пока', 'досвидание',
                 'хорошего дня', 'хорошего вечера', 'иди нахуй', 'пошёл нахуй', 'пошел нахуй']


@client.event
async def on_ready():
    print('Катя Круть на месте!')


@client.event
async def on_message(message):
    await client.process_commands(message)
    msg = message.content.lower()
    if msg in hello_words:
        await message.channel.send('Ну привет и хули тебе надобно?')
    if msg in answer_words:
        await message.channel.send('Ну солнышко, пропиши -help и всё узнаешь блин 👉👈')
    if msg in goodbye_words:
        await message.channel.send('Уходиш ну і пиздуй. Удачи солнышко!')
    if ('@everyone') in msg:
        await message.delete()
        await message.author.send(
            f'{message.author.name}, ну я же просил так не делать, ай, ай, ай, мне же обидно блин 👉👈, ты же не блатной и даже не сидел...')
    if ("@here") in msg:
        await message.delete()
        await message.author.send(
            f'{message.author.name}, ну это тоже не красиво, лучше чем everyone, но всё ещё петушинный поступок... Солнышко, не делай так👉👈')


@client.event
async def on_member_join(member):
    guild = client.get_guild(869536215995662337)
    channel = client.get_channel(872113527408689152)
    welcomeEmbed = discord.Embed(
        title='Ого новоприбывший!',
        colour=discord.Color.blurple(),
        description=f'Хай ``{member.name}``, приветствую на этом чудесном сервере или как прийнято тут говорить, дарова ёпта!',
        color=0x0f0faa)
    welcomeEmbed.set_author(name=member.name, icon_url=member.avatar_url)
    await channel.send(embed=welcomeEmbed)


for i in range(len(cogs)):
    cogs[i].setup(client)
for i in range(len(cgs)):
    print("YAY")
client.run(config.TOKEN)
