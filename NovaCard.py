import os
import time
import requests
import random
import string
import datetime
import shutil
import tempfile
import PyInstaller.__main__
import subprocess
import sys
import webbrowser


discord_webhook_url = "No webhook selected"
last_codes = []
valid_count = 0
invalid_count = 0
generated_count = 0

# Flag to track if the message has already been displayed
intro_displayed = False

def display_intro_message():
    """Displays the message once when the software is first opened."""
    global intro_displayed
    if not intro_displayed:
        print("\033[31mSoftware developed by Ole4923.\033[35m")
        time.sleep(2)  # Wait for 3 seconds to display the message.
        
        intro_displayed = True  # Set the flag to True so the message is not displayed again.

def set_title():
    os.system("title NavaCord by Ole4923")
    os.system("mode con: cols=150 lines=30")

def display_logo():
    logo = '''
\033[35m

  _   _                   ____              _ 
 | \ | | __ ___   ____ _ / ___|___  _ __ __| |
 |  \| |/ _` \ \ / / _` | |   / _ \| '__/ _` |
 | |\  | (_| |\ V / (_| | |__| (_) | | | (_| |
 |_| \_|\__,_| \_/ \__,_|\____\___/|_|  \__,_|
\033[0m    '''
    print(logo)

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def display_menu():
    options = [" Nitro Code Generator", " Bot Token Info", " User Token Info", " Webhook Info", " Webhook Spammer", " Webhook Deleter"," Server Info", " Discord", " Buy me a coffee"]
    exit_option = "Exit"

    max_per_column = 7000
    
    for i in range(0, len(options), max_per_column):
        column = options[i:i + max_per_column]
        for idx, option in enumerate(column, start=i + 1):
            print(f"[\033[35m{idx}\033[0m] {option}")

    print(f"[\033[35m{len(options)+1}\033[0m] {exit_option}")

def generate_random_string(length=18):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

def send_to_discord(webhook_url, message):
    payload = {"content": message}
    try:
        response = requests.post(webhook_url, json=payload)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Error sending to Discord: {e}")

def update_display():
    clear_screen()
    display_logo()
    print(f"\n\033[35mCurrently selected Webhook:\033[0m {discord_webhook_url}")
    print("===============================")
    for entry in last_codes:
        print(entry)

def add_code_to_list(code, status="?"):
    global last_codes, valid_count, invalid_count

    if status == "?":
        return  

    symbol = "✅" if status == "valid" else "❌"
    last_codes.insert(0, f"{code} {symbol}")

    if status == "valid":
        valid_count += 1
    elif status == "invalid":
        invalid_count += 1

    update_display()

def code_generator(amount):
    global valid_count, invalid_count, generated_count
    valid_count = 0
    invalid_count = 0
    generated_count = amount  

    url_template = "https://discordapp.com/api/v9/entitlements/gift-codes/{code}?with_application=false&with_subscription_plan=true"

    generated_codes = []  # For final summary

    for _ in range(amount):
        random_code = generate_random_string(18)
        generated_codes.append(random_code)  # Save for summary
        url = url_template.format(code=random_code)

        try:
            response = requests.get(url)

            if response.status_code == 200:
                add_code_to_list(random_code, "valid")
                send_to_discord(discord_webhook_url, f"Valid Nitro code found: {random_code}")
            else:
                add_code_to_list(random_code, "invalid")
        except requests.RequestException as e:
            print(f"Error checking code {random_code}: {e}")

    clear_screen()
    display_logo()
    print("\n\033[35mSummary:\033[0m")
    print("===============================")
    print(f"🔄 Generated codes: {generated_count}")
    print(f"❌ Invalid codes: {invalid_count}")
    print(f"✅ Valid codes: {valid_count}")
    print("\n")
    input()
    main()

def option_1_Nitro_gen():
    global discord_webhook_url, last_codes, valid_count, invalid_count, generated_count

    discord_webhook_url = "No webhook selected"
    last_codes = []
    valid_count = 0
    invalid_count = 0
    generated_count = 0

    while True:
        update_display()
        print("\n[\033[35m1\033[0m] Select Webhook")
        print("[\033[35m2\033[0m] Generate Codes")
        print("[\033[35m3\033[0m] Back to Main Menu")
        choice = input("\nSelect an option: ")
        
        if choice == '1':
            clear_screen()
            display_logo()
            print("Enter your Webhook:")
            discord_webhook_url = input("> ")
            if not discord_webhook_url.startswith('http'):
                discord_webhook_url = "No webhook selected"
                print("Invalid Webhook! Please enter a valid link.")
                time.sleep(1)
        elif choice == '2':
            if discord_webhook_url == "No webhook selected":
                print("Please select a valid webhook first!")
                time.sleep(1)
                continue
            
            try:
                clear_screen()
                display_logo()
                amount = int(input("How many codes should be generated and tested? > "))
                if amount > 0:
                    print(f"Starting generation of {amount} codes...")
                    code_generator(amount)
                else:
                    print("Please enter a number greater than 0.")
            except ValueError:
                print("Invalid input! Please enter a number.")
            time.sleep(1)
        elif choice == '3':
            discord_webhook_url = "No webhook selected"
            last_codes = []
            valid_count = 0
            invalid_count = 0
            generated_count = 0
            break  # Return to main menu
        else:
            print("Invalid selection. Please try again.")
            time.sleep(1)

def check_bot_token(bot_token):
    url = "https://discord.com/api/v10/users/@me"
    headers = {"Authorization": f"Bot {bot_token}"}
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        bot_data = response.json()
        bot_name = bot_data.get("username", "❓")
        bot_id = bot_data.get("id", "")
        bot_status = "Online" if bot_data.get("bot", False) else "Offline"
        bot_creation_date = "❓"  # Discord does not provide this directly
        bot_owner = "❓"  # No direct API method
        bot_guilds = "❓"  # Could initiate an additional API request here
        return bot_name, bot_id, bot_status, bot_creation_date, bot_owner, bot_guilds
    else:
        return "❓", "❓", "❓", "❓", "❓", "❓"

def option_2_Bot_Token_Info():
    clear_screen()
    display_logo()
    print("\033[35mBot Token Info:\033[0m")
    print("===============================")
    bot_token = input("Enter your bot token (or press Enter to cancel): ")

    if bot_token == "":
        print("No token entered. Returning to the main menu.")
        time.sleep(1)
        return main()
    
    bot_name, bot_id, bot_status, bot_creation_date, bot_owner, bot_guilds = check_bot_token(bot_token)
    
    clear_screen()
    display_logo()
    print("\033[35mBot Info\033[0m")
    print("===============================")
    
    if bot_name == "XXXXX":
        print("\033[31mBot token invalid!\033[0m")
    else:
        print("\033[32mToken: Valid\033[0m")
    
    print(f"User ID: {bot_id}")
    print(f"Status: {bot_status}")
    print(f"Owner: {bot_owner}")
    print(f"Created on: {bot_creation_date}")
    print(f"On {bot_guilds} servers")
    
    input("\nPress Enter to return to the menu...")

def get_creation_date(snowflake_id):
    """Calculate the creation date from the Discord Snowflake ID."""
    timestamp = ((int(snowflake_id) >> 22) + 1420070400000) / 1000
    return datetime.datetime.utcfromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')

def check_user_token(user_token):
    url = "https://discord.com/api/v10/users/@me"
    headers = {"Authorization": user_token}  # No "Bearer", just the raw token

    # HEAD request for a quick check
    response = requests.head(url, headers=headers)

    if response.status_code == 401:
        return "❌ Token invalid or expired.", "", "", "", "", ""
    elif response.status_code == 403:
        return "⛔ Token forbidden! Possibly banned.", "", "", "", "", ""
    elif response.status_code != 200:
        return f"⚠ Error {response.status_code}: {response.text}", "", "", "", "", ""

    # If the token is valid, retrieve the full user data
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        user_data = response.json()
        user_name = user_data.get("username", "❓") + "#" + user_data.get("discriminator", "0000")
        user_id = user_data.get("id", "❓")
        user_email = user_data.get("email", "❓")
        user_status = "✅ Active" if user_data.get("verified", False) else "⚠ Unverified"
        user_creation_date = get_creation_date(user_id) if user_id != "❓" else "❓"

        # Check if 2FA is enabled (indirectly by trying to perform an action)
        url_2fa = "https://discord.com/api/v10/users/@me/2fa"
        response_2fa = requests.get(url_2fa, headers=headers)

        if response_2fa.status_code == 200:
            two_fa_status = "✅ 2FA enabled"
        else:
            two_fa_status = "❌ 2FA not enabled"

        # Check subscriptions (e.g., Discord Nitro)
        url_subscriptions = "https://discord.com/api/v10/users/@me/billing/subscriptions"
        response_subs = requests.get(url_subscriptions, headers=headers)

        if response_subs.status_code == 200:
            subscriptions = response_subs.json()
            user_subscriptions = [sub['sku_id'] for sub in subscriptions] if subscriptions else ["❌ No subscriptions found"]
        else:
            user_subscriptions = ["❌ No subscriptions available"]

        return user_name, user_id, user_email, user_status, user_creation_date, two_fa_status, user_subscriptions

    return "❓", "❓", "❓", "❓", "❓", "❓", "❓"

def option_3_User_Token_Info():
    clear_screen()
    display_logo()
    print("\033[35mUser Token Info:\033[0m")
    print("===============================")
    user_token = input("\nEnter your user token (or press Enter to cancel): ")

    if not user_token:
        print("No token entered. Returning to the main menu.")
        time.sleep(1)
        return main()
    
    user_name, user_id, user_email, user_status, user_creation_date, two_fa_status, user_subscriptions = check_user_token(user_token)
    
    clear_screen()
    display_logo()
    print("\033[35mUser Info\033[0m")
    print("===============================")
    
    if user_name.startswith("❌") or user_name.startswith("⛔") or user_name.startswith("⚠"):
        print(f"\033[31m{user_name}\033[0m")
    else:
        print("\033[32mToken: Valid\033[0m")
    
    print(f"User ID: {user_id}")
    print(f"Email: {user_email}")
    print(f"Status: {user_status}")
    print(f"Created on: {user_creation_date}")
    print(f"2FA Status: {two_fa_status}")
    print(f"Subscriptions: {', '.join(user_subscriptions)}")
    
    input("\nPress Enter to return to the menu...")

def option_5_Webhook_Spammer():
    clear_screen()
    display_logo()
    print("\033[35mWebhook Spammer:\033[0m")
    print("===============================")
    webhook_url = input("\nEnter the webhook URL: ")
    clear_screen()
    display_logo()
    print("\033[35mWebhook Spammer:\033[0m")
    print("===============================")
    message = input("\nEnter the message: ")
    
    try:
        clear_screen()
        display_logo()
        print("\033[35mWebhook Spammer:\033[0m")
        print("===============================")
        num_messages = int(input("\nHow many messages should be sent? "))
        clear_screen()
        display_logo()
        print("\033[35mWebhook Spammer:\033[0m")
        print("===============================")
        messages_per_second = float(input("\nHow many messages per second? "))

        if num_messages <= 0 or messages_per_second <= 0:
            print("Error: Both values must be greater than 0.")
            return

    except ValueError:
        print("Error: Please enter valid numbers.")
        return

    delay = 1 / messages_per_second

    for _ in range(num_messages):
        payload = {"content": message}
        try:
            response = requests.post(webhook_url, json=payload)
            response.raise_for_status()
            clear_screen()
            display_logo()
            print("\033[35mWebhook Spammer:\033[0m")
            print("===============================")
            print(f"\nSent: {message}")
        except requests.RequestException as e:
            print(f"Error sending: {e}")
        time.sleep(delay)

        clear_screen()
        display_logo()
        print("\033[35mWebhook Spammer:\033[0m")
        print("===============================")
        print("\nAll messages have been sent!")
        input("Press Enter to return to the menu...")

def check_webhook_info(webhook_url):
    try:
        response = requests.get(webhook_url)
        
        if response.status_code == 200:
            webhook_data = response.json()
            webhook_id = webhook_data.get("id", "❓")
            webhook_name = webhook_data.get("name", "❓")
            webhook_guild_id = webhook_data.get("guild_id", "❓")
            webhook_channel_id = webhook_data.get("channel_id", "❓")
            webhook_creator = webhook_data.get("user", {}).get("id", "❓")
            webhook_avatar = webhook_data.get("user", {}).get("avatar", "❓")

            return webhook_id, webhook_name, webhook_guild_id, webhook_channel_id, webhook_creator, webhook_avatar
        elif response.status_code == 404:
            return "❌ Webhook not found.", "", "", "", "", ""
        else:
            return f"⚠ Error {response.status_code}: {response.text}", "", "", "", "", ""

    except requests.RequestException as e:
        return f"❌ Request error: {e}", "", "", "", "", ""

def option_4_Webhook_Info():
    clear_screen()
    display_logo()
    print("\033[35mWebhook Info Checker:\033[0m")
    print("===============================")
    webhook_url = input("Enter the webhook URL (or press Enter to cancel): ")

    if not webhook_url:
        print("Cancelled. Returning to the main menu...")
        time.sleep(1)
        return main()

    webhook_id, webhook_name, webhook_guild_id, webhook_channel_id, webhook_creator, webhook_avatar = check_webhook_info(webhook_url)

    clear_screen()
    display_logo()
    print("\033[35mWebhook Info\033[0m")
    print("===============================")

    if webhook_id.startswith("❌") or webhook_id.startswith("⚠"):
        print(f"\033[31m{webhook_id}\033[0m")
    else:
        print("\033[32mWebhook is valid!\033[0m")
    
    print(f"Webhook ID: {webhook_id}")
    print(f"Name: {webhook_name}")
    print(f"Server ID: {webhook_guild_id}")
    print(f"Channel ID: {webhook_channel_id}")
    print(f"Creator ID: {webhook_creator}")
    print(f"Avatar: {webhook_avatar if webhook_avatar != '❓' else 'No avatar'}")

    input("\nPress Enter to return to the menu...")

def delete_webhook(webhook_url):
    try:
        response = requests.delete(webhook_url)
        
        if response.status_code == 204:
            print("\n\033[32mWebhook successfully deleted!\033[0m")

            time.sleep(1)

            clear_screen()
            display_logo()
            print("\033[35mWebhook Deleter:\033[0m")
            print("===============================")

        elif response.status_code == 404:
            print("\n\033[31mWebhook not found!\033[0m")

            time.sleep(1)

            clear_screen()
            display_logo()
            print("\033[35mWebhook Deleter:\033[0m")
            print("===============================")

        else:
            print(f"\n\033[31mError deleting: {response.status_code} - {response.text}\033[0m")

            time.sleep(1)

            clear_screen()
            display_logo()
            print("\033[35mWebhook Deleter:\033[0m")
            print("===============================")

    except requests.RequestException as e:
        print(f"\n\033[31mRequest error: {e}\033[0m")

def option_6_Webhook_Deleter():
    clear_screen()
    display_logo()
    print("\033[35mWebhook Deleter:\033[0m")
    print("===============================")
    
    webhook_url = input("Enter the webhook URL to delete (or press Enter to cancel): ")

    if not webhook_url:
        print("\nCancelled. Returning to the main menu...")
        time.sleep(1)
        return

    clear_screen()
    display_logo()
    print("\033[35mWebhook Deleter:\033[0m")
    print("===============================")

    confirm = input("\nAre you sure you want to delete this webhook? (yes/no): ").strip().lower()
    
    if confirm == "yes":
        delete_webhook(webhook_url)
    else:
        print("\nDeletion cancelled.")
        time.sleep(1)

    clear_screen()
    display_logo()
    print("\033[35mWebhook Deleter:\033[0m")
    print("===============================")

    input("\nPress Enter to return to the menu...")


def option_7_guild_info_by_invite():
    clear_screen()
    display_logo()
    print("\033[35mServer Info:\033[0m")
    print("===============================")

    invite = input("Enter the invite code or full invite link (e.g. discord.gg/abc123): ").strip()

    # Extrahiere Invite-Code, wenn ein voller Link eingegeben wurde
    if "discord.gg/" in invite:
        invite = invite.split("discord.gg/")[-1]
    elif "/" in invite:
        invite = invite.split("/")[-1]

    url = f"https://discord.com/api/v10/invites/{invite}?with_counts=true"

    try:
        response = requests.get(url)
        if response.status_code != 200:
            print(f"\n\033[31mFailed to fetch info: {response.status_code} - {response.text}\033[0m")
            input("Press Enter to return to the menu...")
            return

        data = response.json()
        guild = data.get("guild", {})

        clear_screen()
        display_logo()
        print(f"\033[35mGuild Info\033[0m")
        print("===============================")
        print(f"📛 Name: {guild.get('name', '❓')}")
        print(f"🆔 ID: {guild.get('id', '❓')}")
        print(f"👥 Approx. Members: {data.get('approximate_member_count', '❓')}")
        print(f"🟢 Online: {data.get('approximate_presence_count', '❓')}")
        print(f"🔗 Invite Code: {invite}")

        input("\nPress Enter to return to the main menu...")

    except requests.RequestException as e:
        print(f"\n\033[31mRequest error: {e}\033[0m")
        input("Press Enter to return to the menu...")

def option_8_join_Discord():
    url = "https://discord.com/invite/wvEbYQqXPQ"
    webbrowser.open(url)


def option_9_donate():
    url = "https://www.paypal.com/ncp/payment/95YV66V6C6P7A"
    webbrowser.open(url)

def main():
    while True:
        set_title()
        display_intro_message()
        set_title()
        clear_screen()
        display_logo()
        clear_screen()
        display_logo()
        print("\n\033[35mMain Menu:\033[0m")
        print("===============================")
        display_menu()
        choice = input("\nChoose an option: ")

        if choice == '1':
            option_1_Nitro_gen()
        elif choice == '2':
            option_2_Bot_Token_Info()
        elif choice == '3':
            option_3_User_Token_Info()
        elif choice == '4':
            option_4_Webhook_Info()
        elif choice == '5':
            option_5_Webhook_Spammer()
        elif choice == '6':
            option_6_Webhook_Deleter()
        elif choice == '7':
            option_7_guild_info_by_invite()
        elif choice == '8':
            option_8_join_Discord()
        elif choice == '9':
            option_9_donate()
        elif choice == '9':
            print("Exiting the program...")
            break
        else:
            print("Invalid choice.")
            time.sleep(1)

if __name__ == "__main__":
    main()
