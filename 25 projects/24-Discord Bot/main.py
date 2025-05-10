import discord
import os
import requests
import json
import random
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

# Set up Discord intents
intents = discord.Intents.default()
intents.message_content = True  # Enable Message Content Intent
intents.presences = True        # Enable Presences Intent
intents.members = True          # Enable Server Members Intent

# Initialize Discord client with intents
client = discord.Client(intents=intents)

# List of sad words to trigger encouragements
sad_words = ["sad", "depressed", "unhappy", "angry", "miserable"]

# Default encouraging messages
starter_encouragements = [
    "Cheer up!",
    "Hang in there.",
    "You are a great person / bot!"
]

# File for storing encouragements and responding state
DATA_FILE = "encouragements.json"

def load_data():
    """Load encouragements and responding state from JSON file."""
    try:
        with open(DATA_FILE, "r") as f:
            data = json.load(f)
            return data.get("encouragements", []), data.get("responding", True)
    except (FileNotFoundError, json.JSONDecodeError):
        return [], True

def save_data(encouragements, responding):
    """Save encouragements and responding state to JSON file."""
    try:
        with open(DATA_FILE, "w") as f:
            json.dump({"encouragements": encouragements, "responding": responding}, f)
    except IOError as e:
        print(f"Error saving data: {e}")

# Initialize data
encouragements, responding = load_data()

def get_quote():
    """Fetch a random inspirational quote from ZenQuotes API."""
    try:
        response = requests.get("https://zenquotes.io/api/random")
        response.raise_for_status()
        json_data = json.loads(response.text)
        quote = json_data[0]["q"] + " -" + json_data[0]["a"]
        return quote
    except (requests.RequestException, ValueError) as e:
        return f"Error fetching quote: {e}"

def update_encouragements(encouraging_message):
    """Add a new encouraging message."""
    global encouragements
    encouragements.append(encouraging_message)
    save_data(encouragements, responding)

def delete_encouragement(index):
    """Delete an encouraging message by index."""
    global encouragements
    if len(encouragements) > index:
        del encouragements[index]
        save_data(encouragements, responding)
        return True
    return False

@client.event
async def on_ready():
    """Log when the bot is ready."""
    print(f"We have logged in as {client.user}")

@client.event
async def on_message(message):
    """Handle incoming messages and commands."""
    global encouragements, responding

    if message.author == client.user:
        return

    msg = message.content.lower()

    # $inspire: Send a random quote
    if msg.startswith("$inspire"):
        quote = get_quote()
        await message.channel.send(quote)

    # Auto-respond to sad words if responding is enabled
    if responding:
        options = starter_encouragements + encouragements
        if any(word in msg for word in sad_words):
            await message.channel.send(random.choice(options))

    # $new: Add a new encouraging message
    if msg.startswith("$new"):
        if len(msg) <= 5:
            await message.channel.send("Please provide a message after $new.")
            return
        encouraging_message = msg.split("$new ", 1)[1]
        update_encouragements(encouraging_message)
        await message.channel.send("New encouraging message added.")

    # $del: Delete an encouraging message by index
    if msg.startswith("$del"):
        if len(msg) <= 5:
            await message.channel.send("Please provide an index after $del.")
            return
        try:
            index = int(msg.split("$del ", 1)[1])
            success = delete_encouragement(index)
            if success:
                await message.channel.send(f"Deleted message. Current encouragements: {encouragements}")
            else:
                await message.channel.send(f"No message at index {index}.")
        except ValueError:
            await message.channel.send("Please provide a valid number after $del.")

    # $list: Show all encouraging messages
    if msg.startswith("$list"):
        if encouragements:
            await message.channel.send(f"Encouragements: {encouragements}")
        else:
            await message.channel.send("No custom encouragements yet.")

    # $responding: Toggle responding to sad words
    if msg.startswith("$responding"):
        if len(msg) <= 11:
            await message.channel.send("Please specify 'true' or 'false' after $responding.")
            return
        value = msg.split("$responding ", 1)[1].lower()
        if value == "true":
            responding = True
            save_data(encouragements, responding)
            await message.channel.send("Responding is on.")
        elif value == "false":
            responding = False
            save_data(encouragements, responding)
            await message.channel.send("Responding is off.")
        else:
            await message.channel.send("Please use 'true' or 'false' after $responding.")

# Run the bot
if not DISCORD_TOKEN:
    print("Error: DISCORD_TOKEN not found in .env file.")
else:
    client.run(DISCORD_TOKEN)