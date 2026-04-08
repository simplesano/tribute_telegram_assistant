# Hosting Tribute Assistant on Railway for Telegram Payments Automation

Tribute is a Telegram-based payment service that accepts bank cards from almost any country, which makes it unique, and that’s why it’s gaining popularity among businesses working, for example, with Russian clients from abroad.

It works inside Telegram: you receive orders as chat messages from the Tribute bot. But there's a catch – Tribute doesn’t have an API for digital product payments. It only sends notifications about new orders.

This Python Telegram assistant handles the routine work. It works with Telethon – the official Telegram library for creating bots that can read and reply to messages.

When a user makes a payment:
 1️⃣ Tribute sends a message about the new order
 2️⃣ The assistant checks if the order description contains the user ID
 3️⃣ If valid, it sends a request to the server
 4️⃣ The server activates the product
 5️⃣ The assistant replies to Tribute with order details and confirms the delivery

This code is designed to work on Railway cloud:
https://www.railway.com

Railway does not provide runtime SSH access. Instead, credentials are configured directly in the control panel as environment variables. After cloning this project to Railway, set the environment variables in your dashboard. The variables are listed in env.py.

Generating the Telegram Session
To authorize the assistant, generate a Telethon session locally. Run local_auth.py on your machine. After successful authorization, the script prints your session string. That exact string should be added as the TG_HASH variable on Railway.

There is a room for improvement, such as:
- Better localization with additional languages (currently English and Russian)
- Auto-generated feedback responses when payment details are missing

Feel free to contribute to this project on GitHub. I am also happy to help if you run into any setup issues.
