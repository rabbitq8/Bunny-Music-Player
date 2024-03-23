
<br>

# Bunny Music Player

[![Build Status](https://travis-ci.org/joemccann/dillinger.svg?branch=master)](https://github.com/officicalalkhaldi/Bunny-Music-Player)

<br>

<p style="font-size: 5px;">
  The "Bunny Music Player" is a Python command-line tool for playing music. It offers keyboard shortcuts for playback control, volume adjustment, and track navigation. Users specify a directory for their music files, and the player provides track information and playback instructions.
</p>

<br>

## Features

<br>

> 1. Easily control music playback with keyboard shortcuts.
> 
> 2. Adjust volume levels conveniently from the command line.
> 
> 3. Navigate through tracks in the playlist with ease.
> 
> 4. Get real-time information about the currently playing track, including its title, volume, and playback progress.
> 

<br>

## Screenshots
<br>

![Music player in action, playing music.](screenshots/screenshot2.png)

## Usage

```
git clone https://github.com/officicalalkhaldi/Bunny-Music-Player.git

cd Bunny-Music-Player

python music_cli.py --playlist <directory_path>

```

> Replace **<directory_path>** with the path to the directory containing your music files.

<br>

## Keyboard Shortcuts
```
p: Pause/Resume playback
n: Next track
s: Skip track
c: Previous track
d: Decrease volume
u: Increase volume
r: Rewind to start
m: Move back 10 seconds
b: Move forward 10 seconds
e: Exit the player
```
<br>

## Requirements

```
> Python 3.x
> pip install rich
```

<br>

## Contributing

- Pull requests are welcome. For major changes,
- please open an issue first to discuss what you would like to change.
- Please make sure to update tests as appropriate.


<br>

## License
[MIT](https://choosealicense.com/licenses/mit/)
