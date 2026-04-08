<p align="left">
  <img src="https://img.shields.io/badge/Python-3.10+-blue" />
  <img src="https://img.shields.io/badge/Platform-Railway-black" />
  <img src="https://img.shields.io/badge/License-MIT-green" />
</p>

# Hosting Tribute Assistant on Railway for Telegram Payments Automation

## 📌 Overview

**Tribute** is a Telegram-based payment service that accepts bank cards from almost any country.  
This makes it especially useful for businesses working with international audiences, including Russian clients abroad.

The service operates entirely inside Telegram: orders are delivered as chat messages from the Tribute bot.

⚠️ **Limitation:** Tribute does not provide an API for digital product payments — only notifications about new orders.

## 🤖 Solution

This project provides a **Python-based Telegram assistant** that automates order processing.

It uses **Telethon** — the official Telegram library for building clients that can read and respond to messages.

## ⚙️ How It Works

When a user makes a payment:

1. Tribute sends a message about the new order  
2. The assistant detects the order and sends it to the backend
3. The backend activates the product
   - In case of succcess, the assistant replies to Tribute and confirms delivery
   - In case of an error, the assistant sends message to admin

## ☁️ Deployment (Railway)

This project is designed to run on **Railway**:  
https://www.railway.com  

### Key Notes

- Railway does **not provide SSH access**  
- Configuration is done via **environment variables**  
- All required variables are listed in `env.py`  

After deploying the project, set the variables in your Railway dashboard.

## 🔐 Telegram Session Setup

To authorize the assistant, you need to generate a **Telethon session string** locally.

### Steps:

1. Run:
   ```bash
   python local_auth.py
   ```
2. Complete Telegram authorization
3. Copy the generated session string to Railway variable `TG_HASH`

## 💡 Possible Improvements

There is a room for improvement, such as:
- Better localization with additional languages (currently English and Russian)
- Auto-generated feedback responses when payment details are missing

## 🤝 Contribution and support

Feel free to contribute to this project on GitHub. I am also happy to help if you run into any setup issues.
