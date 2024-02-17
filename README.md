<a href="https://github.com/dudynets/Telegram-Summarize-Bot">
  <img src="https://user-images.githubusercontent.com/39008921/191470114-c074b17f-1c88-4af3-b089-1b14418cabf5.png" alt="drawing" width="128"/>
</a>

# Telegram Summarize Bot

<p><strong>A Telegram bot that summarizes messages from a chat.</strong></p>

> Developed by [Oleksandr Dudynets](https://dudynets.dev)

## Overview

When you add the bot to a chat, it start listening to all text messages and save them to a history file.
Then, when any user replies to some message with the command `/summarize`, the bot will summarize all messages that were sent since the replied message.

## Getting Started

### Prerequisites

- [Python](https://www.python.org/)
- [Ollama](https://ollama.com/)
- [Compatible model from Ollama's library](https://ollama.com/library) (e.g. `llama2:13b`)

### Installation and Usage

1. Clone the repository
   ```sh
   git clone https://github.com/dudynets/Telegram-Summarize-Bot
   ```
2. Install the required packages
   ```sh
   pip install -r requirements.txt
   ```
3. Create a `.env` file in the root directory and add the following environment variables:
   ```env
   TELEGRAM_BOT_TOKEN=<your-telegram-bot-token>
   ```
4. Run the bot
   ```sh
   python app.py
   ```
5. Add the bot to a group chat, send some messages and try to summarize them using the `/summarize` command.

## License

Distributed under the [MIT](https://choosealicense.com/licenses/mit/) License.
See [LICENSE](LICENSE) for more information.
