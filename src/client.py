import discord
import os
from discord.ext import commands
from discord import app_commands, Intents
from log.log import logger
from dotenv import load_dotenv
from modal import *
from database import *

# Define the guild ID for the Discord server
GUILD = discord.Object(897839630852952114)
GUILD_test = discord.Object(897839630852952114)


# Define bot
class SupportClient(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        logger.warning('Bot is initializing.')

    async def setup_hook(self) -> None:
        await self.tree.sync()
        logger.warning('Bot setup completed.')


# Initialize the app
load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.guilds = True
intents.integrations = True
intents.messages = True
intents.message_content = True

Database.initialise()
bot = SupportClient(command_prefix='!', intents=intents)

bot.tree.sync()


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    print("Connected to the following guilds:")
    for guild in bot.guilds:
        print(f'- {guild.name} (ID: {guild.id})')
    print('---------------')

    bot.loop.create_task(bot.tree.sync())


@bot.tree.command(name='att_aviso', description="Cria um aviso de att.")
async def version_view(interaction: discord.Interaction, cliente_nome: str):
    versions = ['3.5.6.9', '3.5.6.8', '3.5.5.7', '3.5.5.6']
    view = VersionSelectView(versions, cliente_nome)
    await interaction.response.send_message('## Selecione a versão atualizada:', view=view, ephemeral=True)

    followup_message = await interaction.original_response()
    await followup_message.delete(delay=10)

    # Wait for user interaction
    await bot.wait_for('interaction')

    version = view.value
    channel_id = 897839632820109397
    channel = bot.get_channel(channel_id)
    message = (f':warning:ATENÇÃO:warning:\n\n:beginner:{cliente_nome}\n\n:white_check_mark:ATUALIZAÇÃO\n\n'
               f':blue_circle:SISTEMA 365 - Versão {version}\n\n-----------------------------')

    logger.info(f'Warning of update created. Cliente: {cliente_nome}, Version: {version}')
    await channel.send(content=message)


@bot.tree.command(name='add_topico', description='Criar um novo tópico')
async def create_topic(interaction: discord.Interaction, topic_name: str):
    success = Database.set_topic(topic_name)
    if success:
        logger.info(f'Topic successfully created with name {topic_name}')
        await interaction.response.send_message(f':white_check_mark: Tópico {topic_name} criado com sucesso!', ephemeral=True)
    else:
        logger.error(f'Failed to create a topic with name {topic_name}')
        await interaction.response.send_message(f':prohibited: Erro: O tópico {topic_name} já existe!', ephemeral=True)


@bot.tree.command(name='editar_topico', description='Edita um tópico já existente')
async def edit_topic(interaction: discord.Interaction, topic_search: str):
    topics = Database.search_topic(topic_search)

    # Create a view with buttons for each topic
    view = TopicButtonView(topics)
    await interaction.response.send_message('## Selecione o tópico que deseja editar:', view=view, ephemeral=True)

    # Wait for the user to select a topic
    await bot.wait_for('interaction')

    # Get the ID of the selected topic
    topic_id = view.topic_id

    # Get the name of the selected topic
    topic_name = view.topic_name

    # Ask the user for the new topic_name
    await interaction.followup.send('## Digite o novo nome do tópico:', ephemeral=True)
    message = await bot.wait_for('message')

    # Get the new topic name from the user's message
    new_topic_name = message.content

    followup_message = await interaction.original_response()
    await followup_message.delete(delay=10)

    # Get the new topic in the database
    success = Database.edit_topic(topic_id, new_topic_name)
    if success:
        await interaction.followup.send(f':white_check_mark: Tópico **"{topic_name}"** atualizado para **"{new_topic_name}"** com sucesso!', ephemeral=True)
    else:
        await interaction.followup.send(f':prohibited: Erro: Falha ao atualizar o tópico com ID **{topic_id}**!', ephemeral=True)


@bot.tree.command(name='show_topicos', description='Exibe todos os tópicos da base de dados')
async def show_topics(interaction: discord.Interaction):

    # Get the topics names from database
    topic_names = Database.get_all_topics()

    # Initial message
    topics_string = '## :pushpin:Tópicos disponíveis:\n'
    if topic_names:
        for topic_name in topic_names:
            topics_string += f'- **{topic_name[1]}**\n'
    else:
        topics_string += ':prohibited: Nenhum tópico foi encontrado!'

    # Send the string with all the
    await interaction.response.send_message(topics_string)


@bot.tree.command(name='add_solucao', description='Adiciona um nova solução a base de dados')
async def add_solution(interaction: discord.Interaction, title: str, description: str, image_url: str):

    # Get the topics names from database
    topic_names = Database.get_all_topics()

    # Set the view for topic select
    view = TopicSelectView(topics=topic_names)
    await interaction.response.send_message('## Selecione um tópico para a solução:', view=view)

    # Wait the user interaction
    await bot.wait_for('interaction')

    # Get the topic_id from topic selected by user
    topic_id = view.value

    followup_message = await interaction.original_response()
    await followup_message.delete(delay=10)

    # Add the solution to the database
    success = Database.add_solution(topic_id, title, description, image_url)
    if success:
        await interaction.followup.send(f':white_check_mark: Solução {title} foi salva com sucesso!')
        logger.info(f'Solution {title} saved successfully into database ')
    else:
        await interaction.followup.send(f':prohibited: Erro: Falha ao salvar solução **{title}**!', ephemeral=True)


@bot.tree.command(name='procurar_solucao',description='Procura solução na base de dados')
async def search_solution(interaction: discord.Interaction):

    # Get the topics names from database
    topics = Database.get_all_topics()

    # Set the view for topic select
    view = TopicSelectView(topics=topics)
    await interaction.response.send_message('## Selecione um tópico para procura:', view=view, ephemeral=True)

    # Wait the user interaction
    await bot.wait_for('interaction')

    # Get the topic_id from topic selected by user
    topic_id = view.value

    followup_message = await interaction.original_response()
    await followup_message.delete(delay=10)

    # Search the solutions
    solutions = Database.get_all_solutions_by_topic_id(topic_id)

    if solutions:
        view_solution = SolutionViewSelect(solutions=solutions)
        await interaction.followup.send('## Selecione a solução que deseja visualizar:', view=view_solution, ephemeral=True)

        # Wait the user interaction
        await bot.wait_for('interaction')

        id_selected = view_solution.value
        solution_selected = Database.get_solution_by_id(id_selected)

        followup_message = await interaction.original_response()
        await followup_message.delete(delay=10)

        if solution_selected:
            # Show the solutions
            for solution in solution_selected:
                # Get the url links
                url_links = solution[-1].split(';')

                await interaction.followup.send(f'## **Titulo:** {solution[2]}\n'
                                                f'### Descrição\n '
                                                f'{solution[3]}\n'
                                                f'### Imagem(ns)\n'
                                                f"{' '.join([f'![Image]({url})' for url in url_links])}\n"
                                                f"----")
        else:
            await interaction.followup.send(f':prohibited: Nenhuma solução encontrada com os termos pesquisado!', ephemeral=True)
    else:
        await interaction.followup.send(f':prohibited: Nenhuma solução encontrada no tópico selecionado!', ephemeral=True)


@bot.tree.command( name='help', description='Mostra todos os comandos disponíveis')
async def show_commands(interaction: discord.Interaction):

    # Get the available commands
    commands = bot.tree.get_commands(guild=interaction.guild)

    commands_string = ('## :sparkles: Comandos SupportMate365\n'
                       'Todos os comandos disponíveis são:\n')
    for command in commands:
        commands_string += f'- **{command.name}**: {command.description}\n'

    # Get the DM channel from the user
    if interaction.user.dm_channel is None:
        await interaction.user.create_dm()

    # Send the message to DM
    logger.info(f'Command list sent to {interaction.user.display_name} DM')
    await interaction.user.dm_channel.send(commands_string)

    # Send the confirmation
    await interaction.response.send_message(":white_check_mark: Enviei a lista de comandos para sua DM!", ephemeral=True)

# @bot.tree.command(name='apagar_solucao', description='Apaga uma solução do tópico selecionado')
# async def delete_solution(interaction: discord.Interaction):


bot.run(TOKEN)
