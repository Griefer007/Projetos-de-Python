import discord

# A variável intents armazena as permissões do bot
intents = discord.Intents.default()
# Ativar a permissão para ler o conteúdo das mensagens
intents.message_content = True
# Criar um bot e passar as permissões
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'Fizemos login como {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.content.startswith('$olá'):
        await message.channel.send("Olá")
    elif message.content.startswith('$tchau'):
        await message.channel.send("\U0001f642")
    else:
        await message.channel.send(message.content)

client.run("SEU TOKEN AQUI")
