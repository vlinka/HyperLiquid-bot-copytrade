#! /usr/bin/env python3

import json
import signal
import sys
import time
import os
from hyperliquid.info import Info
from hyperliquid.exchange import Exchange
from hyperliquid.utils import constants
from eth_account import Account

# Configuration
WALLET_TO_TRACK = "0x..." # Wallet to track
CONFIG_FILE = "config.json"

def load_config():
    if not os.path.exists(CONFIG_FILE):
        raise Exception(f"Please create {CONFIG_FILE} with your private key")
    with open(CONFIG_FILE) as f:
        return json.load(f)

def setup():
    config = load_config()
    private_key = config["secret_key"]
    account = Account.from_key(private_key)
    
    info = Info(constants.MAINNET_API_URL, skip_ws=True)
    exchange = Exchange(account, constants.MAINNET_API_URL)
    
    return info, exchange

def get_spot_details(info, address):
    print("=== Wallet Status ===")
    spot_state = info.spot_user_state(address)
    
    if "balances" in spot_state:
        for balance in spot_state["balances"]:
            print(f"""
            Token: {balance['coin']}
            Total: {balance['total']}
            In orders: {balance['hold']}
            Available: {float(balance['total']) - float(balance['hold'])}
            """)
    return spot_state

def copy_trade(info, exchange, wallet_to_track):
    print("\n=== Starting copy trading ===")
    print("Press Ctrl+C to stop the program")
    
    signal.signal(signal.SIGINT, signal_handler)
    
    initial_state = info.spot_user_state(wallet_to_track)
    positions = {}
    
    try:
        while True:
            try:
                current_state = info.spot_user_state(wallet_to_track)
                
                for balance in current_state.get("balances", []):
                    coin = balance["coin"]
                    current_total = float(balance["total"])
                    
                    if coin in positions:
                        position = positions[coin]
                        change = (current_total - position["total"]) / position["total"] if position["total"] > 0 else 0
                        
                        if change < -0.01 and position["in_position"]:
                            try:
                                size_to_sell = position["total"] * abs(change)
                                print(f"SELL {coin}: {size_to_sell:.4f}")
                                exchange.market_open(f"{coin}/USDC", False, size_to_sell)
                                position["total"] = current_total
                                position["in_position"] = False
                            except Exception as e:
                                print(f"Sell error {coin}: {str(e)}")
                        
                        elif change > 0.01 and not position["in_position"]:
                            try:
                                size_to_buy = current_total - position["total"]
                                print(f"BUY {coin}: {size_to_buy:.4f}")
                                exchange.market_open(f"{coin}/USDC", True, size_to_buy)
                                position["total"] = current_total
                                position["in_position"] = True
                            except Exception as e:
                                print(f"Buy error {coin}: {str(e)}")
                    
                    elif current_total > 0:
                        positions[coin] = {
                            "total": current_total,
                            "in_position": False
                        }
                        print(f"New position detected: {coin}")
                
                time.sleep(2)
                
            except Exception as e:
                print(f"Error: {str(e)}")
                time.sleep(5)
                
    except KeyboardInterrupt:
        signal_handler(signal.SIGINT, None)

def signal_handler(signum, frame):
    print("\n=== Stopping program ===")
    print("Closing positions...")
    sys.exit(0)

def main():
    info, exchange = setup()
    
    get_spot_details(info, WALLET_TO_TRACK)

    copy_trade(info, exchange, WALLET_TO_TRACK)

if __name__ == "__main__":
    main()