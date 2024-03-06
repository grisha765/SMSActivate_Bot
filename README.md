# SMSActivate_Bot
This Python script serves as a bot for registering accounts using virtual phone numbers provided by the SMSActivateAPI. It automates the process of obtaining phone numbers, receiving SMS, and handling registration procedures.
### Initial Setup

1. **Clone the repository**: Clone this repository using `git clone`.
2. **Create Virtual Env**: Create a Python Virtual Env `venv` to download the required dependencies and libraries.
3. **Download Dependencies**: Download the required dependencies into the Virtual Env `venv` using `pip`.

```shell
git clone https://github.com/grisha765/SMSActivate_Bot.git
cd SMSActivate_Bot
python3 -m venv venv
venv/bin/pip3 install pyautogui smsactivate
```

### Run Bot

1. **Start an Instance**: Start an instance from the `venv` virtual environment by entering your `API_TOKEN` using the `-t` argument received from https://sms-activate.org/ru/api2.

```shell
venv/bin/python3 main.py -t API_TOKEN
```

### Arguments

1. **-t, --token**: Required. Specify the SMSActivateAPI `API_TOKEN` received from https://sms-activate.org/ru/api2.

### Features

1. Automates the process of obtaining virtual phone numbers from SMSActivateAPI.
2. Handles SMS verification for registration procedures.
3. Alerts user with sound notifications upon successful registration or failure.
4. Automatically retries in case of number blocking or failure to receive SMS.

### Note

1. Ensure you have sufficient balance in your SMSActivateAPI account for purchasing virtual phone numbers and receiving SMS.
