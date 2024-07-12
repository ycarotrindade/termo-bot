# Termo-Bot

A TUI made with Textual and a sieve object made with pure Python POO for calculate the best words for TERMO, a portuguese version of WORDLE.

# Details

This software calculate the best words to put in TERMO, it's basically a set of filters.


# Controls

* Ctrl+z: Enable the input widget again to type a new word.
* Ctrl+a: Try to calculate the best words based on the information given
* Up-arrow: Change the char color, white means "it doens't have that letter", yellow menas "maybe it has that letter" and green means "has that letter"
* Right and Left arrows: Move between chars.
* Backspace: Reset the software

# Installation

1. Download or clone this repository:

```
git clone https://github.com/ycarotrindade/termo-bot.git
```

2. Install the requirements
```
pip install -r requirements.txt
```

3. Run ``main.py``
```
py main.py
```

Note: This is a TUI, this means that this software runs directly in the terminal.