import discord
import os
from discord import app_commands, Intents
from log.log import logger
from dotenv import load_dotenv
from modal import *
from database import *

# Define the guild ID for the Discord server
GUILD = discord.Object(1209544390859816990)


# Define client
class SupportClient(discord.Client):
    def __init__(self, *, intents: discord.Intents):
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)
        logger.warning('Bot is initializing.')

    async def setup_hook(self) -> None:
        self.tree.copy_global_to(guild=GUILD)
        await self.tree.sync(guild=GUILD)
        logger.warning('Bot setup completed.')


# Initialize the app
load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.message_content = True

Database.initialise()
client = SupportClient(intents=intents)


@client.event
async def on_ready():
    print(f'Logged in as {client.user} (ID: {client.user.id})')
    print('---------------')


@client.tree.command(guild=GUILD, name='att_aviso', description="Cria um aviso de att.")
async def version_view(interaction: discord.Interaction, cliente_nome: str):
    versions = ['3.5.5.8', '3.5.5.7', '3.5.5.6']
    view = VersionSelectView(versions, cliente_nome)
    await interaction.response.send_message('## Selecione a versão atualizada:', view=view)

    await client.wait_for('interaction')

    version = view.value
    channel_id = 1239668293334208673
    channel = client.get_channel(channel_id)
    message = (f':warning:ATENÇÃO:warning:\n\n:beginner:{cliente_nome}\n\n:white_check_mark:ATUALIZAÇÃO\n\n'
               f'SISTEMA 365 - Versão {version}\n\n-----------------------------')

    logger.info(f'Warning of update created. Cliente: {cliente_nome}, Version: {version}')
    await channel.send(content=message)


@client.tree.command(guild=GUILD, name='add_topico', description='Criar um novo tópico')
async def create_topic(interaction: discord.Interaction, topic_name: str):
    success = Database.set_topic(topic_name)
    if success:
        logger.info(f'Topic successfully created with name {topic_name}')
        await interaction.response.send_message(f':white_check_mark: Tópico {topic_name} criado com sucesso!', ephemeral=True)
    else:
        logger.error(f'Failed to create a topic with name {topic_name}')
        await interaction.response.send_message(f':prohibited: Erro: O tópico {topic_name} já existe!', ephemeral=True)


@client.tree.command(guild=GUILD, name='editar_topico', description='Edita um tópico já existente')
async def edit_topic(interaction: discord.Interaction, topic_search: str):
    topics = Database.search_topic(topic_search)

    # Create a view with buttons for each topic
    view = TopicButtonView(topics)
    await interaction.response.send_message('## Selecione o tópico que deseja editar:', view=view)

    # Wait for the user to select a topic
    await client.wait_for('interaction')

    # Get the ID of the selected topic
    topic_id = view.topic_id

    # Get the name of the selected topic
    topic_name = view.topic_name

    # Ask the user for the new topic_name
    await interaction.followup.send('## Digite o novo nome do tópico:', ephemeral=True)
    message = await client.wait_for('message')

    # Get the new topic name from the user's message
    new_topic_name = message.content

    # Get the new topic in the database
    success = Database.edit_topic(topic_id, new_topic_name)
    if success:
        await interaction.followup.send(f':white_check_mark: Tópico **"{topic_name}"** atualizado para **"{new_topic_name}"** com sucesso!', ephemeral=True)
    else:
        await interaction.followup.send(f':prohibited: Erro: Falha ao atualizar o tópico com ID **{topic_id}**!', ephemeral=True)


@client.tree.command(guild=GUILD, name='add_solucao', description='Adiciona um nova solução a base de dados')
async def add_solution(interaction: discord.Interaction, title: str, description: str, image_url: str):

    # Get the topics names from database
    topic_names = Database.get_all_topics()

    # Set the view for topic select
    view = TopicSelectView(topics=topic_names)
    await interaction.response.send_message('## Selecione um tópico para a solução:', view=view)

    # Wait the user interaction
    await client.wait_for('interaction')

    # Get the topic_id from topic selected by user
    topic_id = view.value

    # Add the solution to the database
    success = Database.add_solution(topic_id, title, description, image_url)
    if success:
        await interaction.followup.send(f':white_check_mark: Solução {title} foi salva com sucesso!')
        logger.info(f'Solution {title} saved successfully into database ')
    else:
        await interaction.followup.send(f':prohibited: Erro: Falha ao salvar solução **{title}**!', ephemeral=True)


@client.tree.command(guild=GUILD, name='ver_solucao', description='Procura solução na base de dados')
async def search_solution(interaction: discord.Interaction, title_search_term: str):

    # Get the topics names from database
    topics = Database.get_all_topics()

    # Set the view for topic select
    view = TopicSelectView(topics=topics)
    await interaction.response.send_message('## Selecione um tópico para procura:', view=view)

    # Wait the user interaction
    await client.wait_for('interaction')

    # Get the topic_id from topic selected by user
    topic_id = view.value

    # Search the solutions
    solutions = Database.search_solution(topic_id, title_search_term)

    if solutions:
        # Show the solutions
        for solution in solutions:
            # Get the url links
            url_links = solution[-1].split(';')

            await interaction.followup.send(f'## **Titulo:** {solution[2]}\n### Descrição: {solution[3]}\n'
                                        f'### Imagen(s):{"\n".join(url_links)}\n------------------------')
    else:
        await interaction.followup.send(f'Nenhuma solução encontrada com os termos pesquisado!')




client.run(TOKEN)
