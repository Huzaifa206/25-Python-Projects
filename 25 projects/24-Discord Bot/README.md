EncourageBot - A Discord Encouragement Bot
EncourageBot is a Discord bot that provides inspirational quotes, responds to "sad" words with encouraging messages, and allows users to manage custom encouragements. Built with Python and discord.py, it’s based on the freeCodeCamp Discord Bot Tutorial by Beau Carnes.
Features

Inspirational Quotes: Use $inspire to fetch a random quote from the ZenQuotes API.
Sad Word Detection: Responds to words like “sad” or “depressed” with encouraging messages (toggle with $responding true/false).
Custom Encouragements:
$new <message>: Add a custom encouraging message.
$del <index>: Delete a custom message by index.
$list: List all custom messages.



Run the Bot

Run the Script:
Open main.py.
Run:
In terminal: python main.py
Or Run > Run Without Debugging (select “Run Discord Bot”).


Expected output:We have logged in as EncourageBot#1234




Test in Discord:
Click this link to add this bot in your Server: 
https://discord.com/oauth2/authorize?client_id=1370869463901016226

Now Try commands:
$inspire: Get a random quote (e.g., “Stay hungry, stay foolish. -Steve Jobs”).
Type “I’m sad”: Get an encouragement (e.g., “Cheer up!”).
$new You’re awesome!: Add a custom encouragement.
$list: List custom encouragements.
$del 0: Delete a custom encouragement.
$responding false: Disable sad word responses.


Example:User: $inspire
Bot: “The only way to do great work is to love what you do. -Steve Jobs”
User: I’m sad
Bot: Hang in there.
User: $new Keep going!
Bot: New encouraging message added.


Stop the Bot:
Press Ctrl+C in the terminal.



