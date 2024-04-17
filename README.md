# mini-keynote
A tool to present slides based on a text file. Designed to be simple with few features.

Based off the suckless tool, [sent](https://tools.suckless.org/sent/).

## Installation

<details>
<summary

### macOS
</summary>


This command will install the script in your `/usr/local/bin` directory.

We assume that your system has `python3` installed at `/opt/homebrew/bin/python3`. You may have to modify the shebang line in the script to point to your python installation.

```bash
$ sudo curl -L -o /usr/local/bin/present https://github.com/wzid/mini-keynote/releases/download/1.0/present-mac.py && sudo chmod +x /usr/local/bin/present
$ present [presentation-file]
```
</details>

<details>
<summary

### Linux
</summary>

This command will install the script in your `/usr/local/bin` directory.

We assume that your system has `python3` installed at `/usr/bin/env/python`. You may have to modify the shebang line in the script to point to your python installation.

```bash
$ sudo curl -L -o /usr/local/bin/present https://github.com/wzid/mini-keynote/releases/download/1.0/present-linux.py && sudo chmod +x /usr/local/bin/present
$ present [presentation-file]
```
</details>


<details>
<summary

### Windows
</summary>

To use on windows you will either need to manually make the python file an executable or run it with python from the project directory.

```bash
$ git clone https://github.com/wzid/mini-keynote.git
$ cd mini-keynote
$ python3 present.py baseline/pres.txt
```
</details>

## Usage

This is a tool meant to present text files. Each slide is separated by a blank line.

If you want to display an image, prepend the url with an '@' symbol.

A sample presentation file looks like this:

```txt
mini-keynote

made by cameron

It includes these features:
- bullet points
- images
- press `i` to invert colors
- simple presentations

@https://i.imgur.com/r0we4CM.png
```

To invert the colors of the slides, press `i`.
