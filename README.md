# Telegram Calendar Bot

## Overview

The Telegram Calendar Bot allows users to create and manage events with other people, ensuring that all participants have the selected time available. The bot notifies all participants when a new event is created.

## Features

- **Group Management**: Create groups of users to plan events together.
- **Event Scheduling**: Schedule events for groups, ensuring no conflicts with existing events.
- **Notifications**: Automatically notify users of upcoming events 30 minutes in advance.
- **Database Support**: Persistent storage of users, groups, events, and schedules using SQLite.

---

## Prerequisites

- Python 3.9+
- Telegram Bot Token (replace in `bot_instance.py`)

---

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-repo/telegram-calendar-bot.git
   cd telegram-calendar-bot
   ```

2. Create a virtual environment and activate it:
   ```bash
   python3 -m venv venv
   source venv/bin/activate # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up the SQLite database:
   ```bash
   python
   >>> import dataBase.dataBase as db
   >>> db.create_dataBase()
   >>> exit()
   ```

5. Start the bot:
   ```bash
   python main.py
   ```

---

## Directory Structure

```
├── main.py                  # Entry point for the bot
├── bot_instance.py          # Bot initialization
├── handlers
│   ├── handlers.py          # Bot handlers
│   └── keyboard.py          # Inline keyboards for user interaction
├── dataBase
│   └── dataBase.py          # Database operations
├── requirements.txt         # Required Python packages
```

---

## How It Works

### Event Creation Workflow
1. **Create Group**: Users can create groups for event planning.
2. **Schedule Event**: Users select a group, specify an event name, and choose a date and time.
3. **Conflict Check**: The bot ensures no conflicts with existing events for participants.
4. **Notification**: Participants are notified about the event.

### Notifications
- The bot uses APScheduler to send reminders 30 minutes before an event.

---

## Example Usage

1. **Start the Bot**: Send `/start` to the bot.
2. **Group Management**:
   - To create a group, navigate to "Группы" -> "Создать новую группу" -> Enter a name for the group.
   - In the selected group, you can add participants using the provided buttons.
3. **Event Scheduling**:
   - To create an event, navigate to "События" -> "Добавить событие" -> Select a group -> Enter a name for the event.
   - In the selected event within the chosen group, you can add or remove times by pressing the corresponding buttons.
4. **Receive Notifications**: Get reminders before events.

---

## Configuration

### Update Bot Token
Replace the placeholder in `bot_instance.py` with your Telegram bot token:
```python
bot = Bot(token="YOUR_TELEGRAM_BOT_TOKEN")
```

---

## Dependencies

- `aiogram`: Telegram Bot API framework.
- `apscheduler`: Task scheduling.
- `sqlite3`: Database management.

Install dependencies with:
```bash
pip install -r requirements.txt
```

---

## License
This project is licensed under the MIT License.

---

## Contributions
Contributions are welcome! Feel free to fork this repository and submit a pull request.
