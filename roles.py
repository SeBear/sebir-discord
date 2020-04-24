import pandas as pd
from discord.ext import commands as do
import re
import os

os.chdir(os.path.curdir+"\\data")
bot = do.Bot(command_prefix=".")
TOKEN = 'NzAxODc5NDY3NjA5Njg2MTM3.Xp8-UQ.5xIrSeITFCbUoZbngE3-De7QMyc'

def get_auth_list():
    auth_list = pd.DataFrame()


def get_auth_list():
    auth_list = pd.read_csv("school_auth.csv", sep=";", encoding="windows-1251")
    return auth_list

@bot.command(pass_context=True)
async def say(context, arg):

@ -23,43 +27,61 @@ async def on_ready():
@do.bot_has_permissions(manage_roles = True, manage_nicknames = True)
async def on_message(message):

    async def assign(role, name):
        msg = role
        await member.edit(nick=name)
        for role in serverroles:
            if re.match(msg, role.name) is not None:
                print("Assigning...", member.id, role.id)
                if member.nick is not None:
                    tosay = "Я выдал " + member.nick + "права на доступ к " + role.name
                else:
                    tosay = "Я выдал " + member.name + "права на доступ к " + role.name
                await member.edit(roles=[role])
        return tosay

    global auth
    channel = message.channel
    userid = message.author.id
    member = message.author
    serverid = 697358625261223996
    serverroles = bot.get_guild(serverid).roles

    tosay = "Что-то пошло не так и я ничего не стал делать..."

    msg = message.content

    if len(msg) > 4:
        tosay = "Что-то это не очень похоже на класс. Попробуй по-другому!"
        classFound = False
    else:
        try:
            #Берём число
            num = re.search(r"\d+", msg)[0]
            #Берём букву
            letter = re.search(r"(?:\d+)[ -]?(\w)", msg)[1]
            classFound = True
        except IndexError:
            tosay = "Что-то это не очень похоже на класс. Попробуй по-другому!"
            classFound = False

    if classFound:
        msg = num + '-' + letter

    for role in serverroles:
        if classFound and re.match(msg, role.name) is not None:
            print("Assigning...", member.id, role.id)
            if member.nick is not None:
                tosay = "Я выдал " + member.nick + "права на доступ к " + role.name
            else:
                tosay = "Я выдал " + member.name + "права на доступ к " + role.name
            await member.add_roles(role)

    if not message.author.bot:
    # Make sure bot is not assigning itself
    if not member.bot:
        # Make sure message exist
        tosay = "Что-то пошло не так и я ничего не стал делать..."
        msg = message.content
        #Ensure password is valid
        userauth = auth.where(auth['pass'] == msg).dropna()
        if not userauth.empty:
            role = userauth['role'].values[0]
            name = userauth['nick'].values[0]
            tosay = await assign(role, name)
        else:
            tosay = "Неверный пароль! Попробуй ещё раз..."
        await channel.send(tosay)


    # if len(msg) > 4:
    #     tosay = "Что-то это не очень похоже на класс. Попробуй по-другому!"
    #     classFound = False
    # else:
    #     try:
    #         #Берём число
    #         num = re.search(r"\d+", msg)[0]
    #         #Берём букву
    #         letter = re.search(r"(?:\d+)[ -]?(\w)", msg)[1]
    #         classFound = True
    #     except IndexError:
    #         tosay = "Что-то это не очень похоже на класс. Попробуй по-другому!"
    #         classFound = False
    # if classFound:
    #     msg = num + '-' + letter





auth = get_auth_list()
bot.run(TOKEN)
