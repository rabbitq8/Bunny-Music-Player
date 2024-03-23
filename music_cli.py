from argparse import ArgumentParser
import ctypes
import os
import locale
import shutil
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from player import MusicPlayer
from datetime import timedelta
from time import sleep
import keyboard

locale.setlocale(locale.LC_ALL, "")
player = MusicPlayer()

ctypes.windll.kernel32.SetConsoleTitleW("Bunny Music Player")


def convert_to_time(time_ms):
    total_seconds = time_ms // 1000
    hours, remainder = divmod(total_seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return timedelta(hours=hours, minutes=minutes, seconds=seconds)


def main():
    parser = ArgumentParser(
        prog="Bunny music player",
        usage="%(prog)s [options]",
        description="Command-line music player.",
        epilog="Enjoy your music, Bunny!",
        add_help=True,
        allow_abbrev=False,
    )

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "--playlist",
        "-l",
        help="Specify the directory containing music files.",
    )

    args = parser.parse_args()

    if args.playlist:
        player.load_playlist(args.playlist)
        player.play_music(os.path.basename(player.playlist[player.current_track_index]))
    console = Console()

    def update_status():
        instructions = Text(
            "[ Instructions ]\n\n"
            "[*] 'p' to pause\n"
            "[*] 'n' to resume\n"
            "[*] 's' to skip\n"
            "[*] 'c' to prev\n"
            "[*] 'd' to vol(-)\n"
            "[*] 'u' to vol(+)\n"
            "[*] 'r' to rewind(start)\n"
            "[*] 'm' to move_back (10secs)\n"
            "[*] 'b' to back_forward (10secs)\n"
            "[*] 'e' to exit\n"
        )
        now_playing = Text(
            "\n\nNow playing: " + os.path.basename(player.currentTrack) + "\n"
            "Track: "
            + str(player.current_track_index + 1)
            + "/"
            + str(len(player.playlist))
            + "\n"
            + "Volume: "
            + str(player.get_volume() // 10)
            + "%"
            + "\n"
            + f"Time: [ {str(convert_to_time(player.get_position_millisecond()))} | {str(convert_to_time(player.length()))} ]"
            + "\n"
        )
        layout = instructions + now_playing

        global last_layout
        if "last_layout" not in globals() or last_layout != layout:
            last_layout = layout

            console_width = shutil.get_terminal_size().columns
            panel = Panel(layout, title="Bunny Music Player", width=console_width)
            console.clear()
            console.print(panel)

    while True:
        update_status()
        if keyboard.is_pressed("p"):
            keyboard.press_and_release("\b")
            player.pause_music()
            update_status()
        elif keyboard.is_pressed("n"):
            keyboard.press_and_release("\b")
            player.pause_music()
            update_status()
        elif keyboard.is_pressed("m"):
            keyboard.press_and_release("\b")
            player.rewind_10_seconds()
            update_status()
        elif keyboard.is_pressed("s"):
            keyboard.press_and_release("\b")
            player.next_track()
            player.rewind_start()
            update_status()
        elif keyboard.is_pressed("c"):
            keyboard.press_and_release("\b")
            player.prev_track()
            player.rewind_start()
            update_status()
        elif keyboard.is_pressed("r"):
            keyboard.press_and_release("\b")
            player.rewind_start()
            update_status()
        elif keyboard.is_pressed("b"):
            keyboard.press_and_release("\b")
            player.forward_10_seconds()
            update_status()
        elif keyboard.is_pressed("e"):
            keyboard.press_and_release("\b")
            update_status()
            player.stop_music()
            ctypes.windll.kernel32.SetConsoleTitleW("")
            break
        elif keyboard.is_pressed("u"):
            keyboard.press_and_release("\b")
            player.set_volume("up")
            update_status()
        elif keyboard.is_pressed("d"):
            keyboard.press_and_release("\b")
            player.set_volume("down")
            update_status()

        sleep(0.1)


if __name__ == "__main__":
    main()
