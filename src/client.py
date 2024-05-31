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
    def __init__(self, *args: object, **kwargs: object) -> object:
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

    await bot.loop.create_task(bot.tree.sync())


@bot.tree.command(name='add_topico', description='Criar um novo tópico')
async def create_topic(interaction: discord.Interaction, topic_name: str):
    success = Database.set_topic(topic_name)

    if success:
        logger.info(f'Topic successfully created with name {topic_name}')
        await interaction.response.send_message(f':white_check_mark: Tópico {topic_name} criado com sucesso!',
                                                ephemeral=True)
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
        await interaction.followup.send(f':white_check_mark: Tópico **"{topic_name}"**'
                                        f' atualizado para **"{new_topic_name}"** com sucesso!', ephemeral=True)
    else:
        await interaction.followup.send(f':prohibited: Erro: Falha ao atualizar o tópico com ID **{topic_id}**!',
                                        ephemeral=True)


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


@bot.tree.command(name='procurar_solucao', description='Procura solução na base de dados')
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
        await interaction.followup.send('## Selecione a solução que deseja visualizar:', view=view_solution,
                                        ephemeral=True)

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
            await interaction.followup.send(f':prohibited: Nenhuma solução encontrada com os termos pesquisado!',
                                            ephemeral=True)
    else:
        await interaction.followup.send(f':prohibited: Nenhuma solução encontrada no tópico selecionado!',
                                        ephemeral=True)


@bot.tree.command(name='ajuda', description='Mostra todos os comandos disponíveis')
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
    await interaction.response.send_message(":white_check_mark: Enviei a lista de comandos para sua DM!",
                                            ephemeral=True)


# @bot.tree.command(name='apagar_solucao', description='Apaga uma solução do tópico selecionado')
# async def delete_solution(interaction: discord.Interaction):


@bot.tree.command(name='chamados_pedentes',
                  description='Cria uma mensagem com os tickets pendentes, separar numeração com ","')
async def pending_tickets(
        interaction: discord.Interaction,
        aguardando_tratativa: str,
        escalonado_css: str,
        aguardando_cliente: str):
    aguardando_tratativa = ['#' + chamado for chamado in aguardando_tratativa.split(',')]
    escalonado_css = ['#' + chamado for chamado in escalonado_css.split(',')]
    aguardando_cliente = ['#' + chamado for chamado in aguardando_cliente.split(',')]

    message_str = '## :ticket:Chamados Pendentes:ticket:\n'
    message_str += '### **Aguardando Tratativa**\n'
    message_str += '\n'.join(aguardando_tratativa)
    message_str += '\n### **Escalonado CSS**\n'
    message_str += '\n'.join(escalonado_css)
    message_str += '\n### **Aguardando Cliente**\n'
    message_str += '\n'.join(aguardando_cliente)

    channel_id = 1075054483551301683
    channel = bot.get_channel(channel_id)
    await channel.send(message_str)

    await interaction.response.send_message(
        ":white_check_mark: Mensagem de tickets pedentes criado com sucesso! :ticket:",
        ephemeral=True)


@bot.tree.command(name='add_cliente', description='Adiciona cliente na base de dados.')
async def add_cliente(interaction: discord.Interaction, name: str):
    versions_gestor = Database.get_versions_gestor()
    versions_pdv = Database.get_versions_pdv()

    view_gestor = VersionGestorSelectView(versions_gestor)
    await interaction.response.send_message('## :page_with_curl: Selecione a versão do sistema gestor do cliente:'
                                            , view=view_gestor, ephemeral=True)

    # Wait for user interaction
    await bot.wait_for('interaction')

    version_gestor = view_gestor.value

    view_pdv = VersionPdvSelectView(versions_pdv)
    await interaction.followup.send('## :moneybag: Selecione a versão do sistema PDV do cliente:'
                                    , view=view_pdv, ephemeral=True)

    await bot.wait_for('interaction')

    version_pdv = view_pdv.value

    success = Database.add_cliente(name, version_gestor, version_pdv)

    if success:
        await interaction.followup.send(f':white_check_mark: Cliente {name} criado com sucesso!',
                                                ephemeral=True)
    else:
        await interaction.followup.send(f':prohibited: Erro: Erro ao criar cliente {name}.', ephemeral=True)


@bot.tree.command(name='add_versao_gestor', description='Adiciona uma versão do sistema gestor na base de dados.')
async def add_version_gestor(interaction: discord.Interaction, version: str):
    success = Database.add_version_gestor(version)

    if success:
        await interaction.response.send_message(f':white_check_mark: Versão {version} criado com sucesso!',
                                                ephemeral=True)
    else:
        await interaction.response.send_message(f':prohibited: Erro: Versão {version} já existe!', ephemeral=True)


@bot.tree.command(name='add_versao_pdv', description='Adiciona uma versão do sistema PDV na base de dados.')
async def add_version_pdv(interaction: discord.Interaction, version: str):
    success = Database.add_version_pdv(version)

    if success:
        await interaction.response.send_message(f':white_check_mark: Versão {version} criado com sucesso!',
                                                ephemeral=True)
    else:
        await interaction.response.send_message(f':prohibited: Erro: Versão {version} já existe!', ephemeral=True)


bot.run(TOKEN)
