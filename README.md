# Mail Daemon

## Installation (Currently supports only macOS)
First install notifier:
`$ gem install terminal-notifier`
Then use pip to install required packages:
`$ pip install -r requirements.txt`

## Test
` $ ./main_test.py`

## Create configuration file
`$ cp sample.yaml configuration.yaml`
Fill with your email account data.
The field `condition` is used to search for messages, it uses sIMAP SEARCH syntax https://tools.ietf.org/html/rfc3501#page-49
The field `interval` indicates interval of fetching in seconds.
For the field `actions` you can use a list of actions (as many as you want) to take when new messages are found.
example: `- sound: 'any_sound.wav'` will play `any_sound.wav` file
example: `- notify: 'your_message'` will use macOS notification bar with `your_message`

## Run
`$ ./main.py`
