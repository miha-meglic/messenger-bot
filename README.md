# Simple Messenger bot

Just a simple Messenger bot using Selenium automated browser.

## Setup

Create a .env file and write in your Facebook credentials.

Example:

```shell
EMAIL="example@email.com"
PASSWORD="yourpassword"
```

## Running

To run in background uncomment lines from 35 to 37 and comment line 38.  
On startup it asks for a Chat ID, which you can find in a messenger link (i.e. www.facebook.com/messages/t/<span style="color:pink">321564321863</span>).

### Basic commands

The most important commands are:

- !help : Returns available commands
- !quit : Shuts down the bot

There are some hidden key words (this bot was made for a school groupchat) that are irrelevant for most users and will later be removed.

## NOTICE

If you're running the browser in the background, make sure you exit the bot with !quit, otherwise the process keeps running in the background.

This project is just a proof of concept and will be made into a usable API at some point. This is also the reason why about 1/2 of the code is a complete mess and unreadable even to me.

## Licence

MIT License

Copyright (c) [year] [fullname]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
