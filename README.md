# Mail Daemon

## Installation (Currently supports only macOS)
`$ gem install terminal-notifier`
`$ pip install -r requirements.txt`

## Test
` $ ./main_test.py`

## Create configuration file
`$ cp sample.yaml configuration.yaml`
Fill with your email account data.
For `condition` field use IMAP SEARCH syntax https://tools.ietf.org/html/rfc3501#page-49

## Run
`$ ./main.py`
