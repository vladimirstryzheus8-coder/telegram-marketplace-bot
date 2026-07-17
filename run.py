#!/usr/bin/env python3
"""Run script - starts both bot and admin panel"""
import subprocess
import sys
import os
from time import sleep

def run():
    print("🚀 Starting Digital Marketplace Bot...\n")
    
    # Check if database exists
    if not os.path.exists('marketplace.db'):
        print("💾 Initializing database...")
        subprocess.run([sys.executable, 'db_init.py'])
        print()
    
    print("🤖 Starting Telegram Bot...")
    print("🎯 Starting Admin Panel at http://localhost:5000...\n")
    
    # Start bot and admin panel
    bot_process = subprocess.Popen([sys.executable, 'bot.py'])
    sleep(2)
    admin_process = subprocess.Popen([sys.executable, 'admin_panel.py'])
    
    try:
        print("\u2705 Both services are running!")
        print("\n🎯 Admin Panel: http://localhost:5000")
        print("🤖 Telegram Bot: Running...")
        print("\n🔛 Press CTRL+C to stop\n")
        
        bot_process.wait()
        admin_process.wait()
    except KeyboardInterrupt:
        print("\n\n🚫 Stopping services...")
        bot_process.terminate()
        admin_process.terminate()
        bot_process.wait()
        admin_process.wait()
        print("✅ Services stopped.")

if __name__ == '__main__':
    run()
