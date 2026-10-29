"""OPTIONAL always-on interactive bot. Run locally or on a bot hosting service."""
import os
import random
import discord
from discord import app_commands
from discord.ext import commands
from dotenv import load_dotenv
from events import fictional_event, history_events, embed_for

load_dotenv()
token = os.getenv('DISCORD_TOKEN')
if not token:
    raise SystemExit('DISCORD_TOKEN missing; see .env.example')

class Municipal(commands.Bot):
    async def setup_hook(self):
        guild_id = os.getenv('DISCORD_GUILD_ID', '').strip()
        if guild_id:
            guild = discord.Object(id=int(guild_id))
            self.tree.copy_global_to(guild=guild)
            await self.tree.sync(guild=guild)
        else:
            await self.tree.sync()

bot = Municipal(command_prefix='!', intents=discord.Intents.default())

@bot.tree.command(name='event', description='Generate a fictional 1984 town event')
@app_commands.describe(category='Type of fictional town event')
@app_commands.choices(category=[app_commands.Choice(name=n.title(), value=n) for n in
                               ['family','school','crime','business','supernatural','community']])
async def event(interaction: discord.Interaction, category: str | None = None):
    post = fictional_event(category)
    await interaction.response.send_message(embed=discord.Embed.from_dict(embed_for(post)))

@bot.tree.command(name='history', description='Read a sourced real-world historical story from 1984')
@app_commands.describe(month='Optional month 1-12', day='Optional day 1-31')
async def history(interaction: discord.Interaction,
                  month: app_commands.Range[int,1,12] | None = None,
                  day: app_commands.Range[int,1,31] | None = None):
    entries = history_events(month, day)
    if not entries:
        await interaction.response.send_message('No verified historical story in the starter collection for that date yet.', ephemeral=True)
        return
    await interaction.response.send_message(embed=discord.Embed.from_dict(embed_for(dict(random.choice(entries),kind='history'))))

@bot.tree.command(name='townhelp', description='See the town bot commands')
async def townhelp(interaction: discord.Interaction):
    await interaction.response.send_message('Use `/event` for fictional RP hooks and `/history` for sourced 1984 world news. No player characters are changed automatically.', ephemeral=True)

bot.run(token)
