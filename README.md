# mini-keynote
A tool to present slides based on a text file. Designed to be simple with few features.

Based off the suckless tool, [sent](https://tools.suckless.org/sent/).


## Usage

### Using the script

To present a file all you have to do is put the text file in the same directory as the `main.py` script.

Then run the script with the file name as an argument.

```bash
python3 present.py pres.txt
```

### Installing the script

To install the script, you need to move it to a directory in your PATH.

```bash
sudo cp present.py /usr/local/bin/present
```

Then you can run the script from anywhere.

```bash
present file.txt
```

## Presentation File

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