# 🤖 Hyperliquid Copy Trading Bot

A Python-based copy trading bot for the Hyperliquid DEX that automatically mirrors trades from a specified wallet address.

## 📝 Overview

This bot allows you to automatically copy trades from any wallet on Hyperliquid DEX. It monitors the target wallet's positions and replicates their trading activity on your account.

## 💡 Features

- Real-time position monitoring
- Automatic trade replication
- Configurable trade thresholds (1% by default)
- Clean program termination with Ctrl+C
- Detailed logging of all trading activities
- Error handling and recovery
- Support for all assets available on Hyperliquid

## 📦 Prerequisites

- Python 3.8 or higher
- hyperliquid-python-sdk
- A Hyperliquid account with funds
- The wallet address you want to copy

## 🛠️ Installation

1. Install the required package:
```bash
pip install hyperliquid-python-sdk
```
## 🔧 Configuration

Create config.json:
```json
{
    "secret_key": "YOUR_PRIVATE_KEY", // No '0x' prefix
    "account_address": "YOUR_PUBLIC_ADDRESS" // Must include '0x' prefix
}
```

Set target wallet address in code:
```python
WALLET_TO_TRACK = "wallet_address_to_copy"
```

## Usage
```bash
python copy_trading_bot.py
```

## 🛡️ Safety Features

- Error handling for API calls
- Position monitoring
- Trade validation
- Graceful shutdown

## 🔐 Security

- Never share private keys
- Start with small amounts
- Monitor bot activity
-   Keep config.json secure

## 🚨 Disclaimer

Trading cryptocurrencies involves significant risk. This bot is provided as-is with no guarantees. Test with small amounts first.
