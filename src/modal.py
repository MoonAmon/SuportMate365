import traceback
from discord import Interaction
from typing import Any

from discord._types import ClientT

from log.log import logger
import discord


class VersionSelect(discord.ui.Select):
    def __init__(self, versions):
        options = [discord.SelectOption(label=version, value=version) for version in versions]
        super().__init__(options=options)

    async def callback(self, interaction: Interaction):
        self.view.value = self.values[0]
        await interaction.response.send_message(f'Aviso criado para versão: {self.values[0]}', ephemeral=True)


class VersionSelectView(discord.ui.View):
    def __init__(self, versions, cliente_nome):
        super().__init__()
        self.value = None
        self.cliente_nome = cliente_nome
        self.add_item(VersionSelect(versions))


class TopicSelect(discord.ui.Select):
    def __init__(self, topics):
        options = [discord.SelectOption(label=topic[1], value=topic[0]) for topic in topics]
        super().__init__(options=options)

    async def callback(self, interaction: Interaction):
        self.view.value = self.values[0]


class TopicSelectView(discord.ui.View):
    def __init__(self, topics):
        super().__init__()
        self.value = None
        self.add_item(TopicSelect(topics))


class TopicButton(discord.ui.Button):
    def __init__(self, label, topic):
        super().__init__(label=label)
        self.value = topic

    async def callback(self, interaction: discord.Interaction):
        # Get the topic_id select by user
        self.view.topic_id = self.value[0]
        self.view.topic_name = self.value[1]


class TopicButtonView(discord.ui.View):
    def __init__(self, topics):
        super().__init__()
        self.topic_id = None
        self.topic_name = None
        for topic in topics:
            label = topic[1]
            if len(label) > 80:
                self.add_item(TopicButton(label=label[:80], topic=topic))
            else:
                self.add_item(TopicButton(label=label, topic=topic))
