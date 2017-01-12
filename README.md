# PyGhostLid

Submit and retrieve pastes from GhostBin within your application! This library supports both
ghostbin.com and any self-hosted instances of ghostbin.

'GhostLid' as a name is based on the silly idea that this library sits between your application and
GhostBin, in the same way as a lid sits between you and a garbage/composting bin.

This is a super simple library, but I thought it'd be worth sharing it anyway.

## What's GhostBin? Why this library?

GhostBin is an open-source "pastebin"-like web application, that allows users to upload arbitrary
text files for sharing on the internet: for example, sharing code or configuration files when asking
for help on forums, reddit or an IRC channel; sharing log files when contacting a technical support
forum or IRC channel; or sharing a long text to a friend over instant messaging, which often isn't
really friendly to long messages.

This convenience library is intended for any applications that needs a quick way of uploading to
GhostBin. For example, built-in GhostBin button in an instant messaging application, or a framework
that has a one-click "Upload to GhostBin" button for error messages/stack traces to allow them to
easily ask for help or include in a bug report.

## Requirements

This library requires Python 3.x, recommended >= 3.2. It is tested against Python 3.5.

## Basic usage

This library consists of a single class, `GhostLid`, and is dead simple. Check out the basic
examples below, and the method docstrings in the source for more info on the available options,
including using a host other than `ghostbin.com` and setting defaults.

```python
# The text we want to paste
paste_text = """
[04:10:07] <John> hi
[04:10:13] <Jane> hi
[04:19:21] <John> good talk
"""

# Setup
from ghostlid import GhostLid
ghostlid = GhostLid()
ghostlid.load_languages()

# Here's a simple list of supported languages
lang_list = ghostlid.get_lang_list()

# And here's the full info on languages - this has enough info to build a nice user interface
# See the "languages.json" section of this page: https://ghostbin.com/paste/p3qcy
lang_info = ghostlid.get_language_info()

# Paste some text (NOTE: AVOID FOR TEST PASTES - please use an expiration time limit!)
paste_url = ghostlid.paste(paste_text)
print("Your paste was uploaded to this URL: " + paste_url)

# Specify a language (usually programming language) for syntax highlighting
paste_url = ghostlid.paste(paste_text, lang="irc")

# Encrypt the paste with a password
paste_url = ghostlid.paste(paste_text, password="correct horse battery staple", lang="irc")

# Paste with an expiration of 10 minutes
paste_url = ghostlid.paste(paste_text, expire="10m", lang="irc")

# Get the ghostbin protocol info paste at https://ghostbin.com/paste/p3qcy
retrieved_paste_text = ghostlid.get_paste('p3qcy')

# Get the paste we submitted above
paste_id = ghostlid.get_paste_id(paste_url)
retrieved_paste_text = ghostlid.get_paste(paste_id)
```

## Known Issues

* Retrieval `get_paste()` does not work with Ghostbin.com at the time of writing, because
  [the /raw feature was disabled](https://github.com/DHowett/ghostbin/issues/41) on the main site
  due to abuse. It's still available in the codebase and may or may not be enabled on any
  self-hosted Ghostbin instances.

## Links

* [Protocol information for GhostBin](https://ghostbin.com/paste/p3qcy)
* [Note on the /raw feature on Ghostbin.com](https://github.com/DHowett/ghostbin/issues/41)
* [Ghostbin](https://ghostbin.com)
