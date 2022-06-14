import pandas as pd
from discord.ext import commands as do
import re
import os

os.chdir(os.path.curdir+"\\data")
bot = do.Bot(command_prefix=".")
TOKEN = ''

def get_auth_list():
    auth_list = pd.read_csv("school_auth.csv", sep=";", encoding="windows-1251")
    return auth_list

@bot.command(pass_context=True)
async def say(context, arg):
    await context.send(arg)


@bot.event
async def on_ready():
    print("Запущен!")


@bot.event
@do.bot_has_permissions(manage_roles = True, manage_nicknames = True)
async def on_message(message):
    # todo: delete message after assigning
    # todo: check if has role except @everyone - GTFO!
    async def assign(role, name):
        msg = role
        tosay = ", что-то я не могу найти такие права.:no_entry:\n Обратитесь к <@!697160016129687733> :sos:"
        if len(member.roles) > 1:
            tosay = ", права доступа уже назначены. **Система не предполагает привязку более чем к одному классу.** :no_entry:\n" \
                    "Если вы считаете, что данное сообщение возникло по ошибке - обратитесь к администратору <@!697160016129687733> :sos:"
        else:
            await member.edit(nick=name)
            for role in serverroles:
                if re.match(msg, role.name) is not None:
                    print("Assigning...", member.id, role.id)
                    if member.nick is not None:
                        tosay = "Я выдал " + member.nick + " права на доступ к " + role.name + ":white_check_mark:"
                    else:
                        tosay = ":white_check_mark: Я выдал " + member.name + " права на доступ к " + role.name + ":white_check_mark:"
                    await member.edit(roles=[role])
        return tosay

    global auth
    true_content = message.content
    channel = message.channel
    userid = message.author.id
    member = message.author
    mention = member.mention
    serverid = 697358625261223996
    serverroles = bot.get_guild(serverid).roles
    if not member.bot:
        await message.delete()
        # Make sure message exist
        tosay = ", что-то пошло не так и я ничего не стал делать...:x:"
        msg = true_content
        #Ensure password is valid
        userauth = auth.where(auth['pass'] == msg).dropna()
        if not userauth.empty:
            role = userauth['role'].values[0]
            name = userauth['nick'].values[0]
            tosay = await assign(role, name)
        else:
            tosay = ", неверный пароль! Попробуй ещё раз... :x:"
        # Ensure nobody reads password
        if re.match(r"[A-Z0123456789]{6,8}", true_content):
            true_content = "||██████ [ДАННЫЕ_УДАЛЕНЫ]||"
        await channel.send(
            "**:arrow_right::arrow_right::arrow_right:**" + mention + " пишет сообщение: " + true_content)
        await channel.send(mention + ' ' + tosay)

auth = get_auth_list()
bot.run(TOKEN)
