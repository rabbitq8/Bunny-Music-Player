import os
import ctypes
import random
from typing_extensions import Literal


class MusicPlayer:
    DEVICE_ALIAS = "MP3"

    def __init__(self):
        self.playlist = []
        self.current_track_index = 0
        self.shuffle = False
        self.paused = False
        self.currentTrack = ""
        self.currentVol = 1000
        self.mciSendString(f"set {self.DEVICE_ALIAS} time format ms")
        self.is_stopped = False

    def mciSendString(self, command, buffer=None, bufferSize=256, hwndCallback=0):
        buffer = ctypes.create_unicode_buffer(bufferSize)
        ctypes.windll.winmm.mciSendStringW(command, buffer, bufferSize, hwndCallback)
        return buffer.value

    def load_track(self, file_path):
        self.play_music(file_path)

    def get_volume(self):
        p_command = f"status {self.DEVICE_ALIAS} volume"
        volume_str = self.mciSendString(p_command)

        try:
            return int(volume_str)
        except (ValueError, TypeError):
            return 0

    def load_playlist(self, directory):
        for filename in os.listdir(directory):
            if filename.endswith((".mp3", ".wav")):
                file_path = os.path.join(directory, filename)
                self.playlist.append(file_path)

    def play_music(self, trk: str = ""):
        if self.shuffle:
            random.shuffle(self.playlist)

        if len(trk) > 3:
            self.currentTrack = trk
            self.mciSendString(f'open "{trk}" alias {self.DEVICE_ALIAS}')
            self.mciSendString(f"play {self.DEVICE_ALIAS}")

        if len(self.playlist) > 1:
            track_to_play = self.playlist[self.current_track_index]
            self.currentTrack = trk
            self.mciSendString(f'open "{track_to_play}" alias {self.DEVICE_ALIAS}')
            self.mciSendString(f"play {self.DEVICE_ALIAS}")

    def stop_music(self):
        self.mciSendString(f"stop {self.DEVICE_ALIAS}")
        self.close_media()
        self.is_stopped = True

    def pause_music(self):
        if not self.paused:
            self.mciSendString(f"pause {self.DEVICE_ALIAS}")
            self.paused = True
        else:
            self.mciSendString(f"resume {self.DEVICE_ALIAS}")
            self.paused = False

    def length(self):
        p_command = f"status {self.DEVICE_ALIAS} length"
        error = self.mciSendString(p_command)

        try:
            return int(error)
        except ValueError:
            return 0

    def next_track(self):
        if len(self.playlist) > 1:
            self.current_track_index = (self.current_track_index + 1) % len(
                self.playlist
            )
            self.stop_music()
            self.play_music(self.playlist[self.current_track_index])
        else:
            return

    def prev_track(self):
        if len(self.playlist) > 1:
            self.current_track_index = (self.current_track_index - 1) % len(
                self.playlist
            )
            self.stop_music()
            self.play_music(self.playlist[self.current_track_index])
        else:
            return

    def forward_10_seconds(self):
        current_position = self.get_position_millisecond()
        new_position = max(0, current_position + 1000)
        self.set_position(new_position)

    def rewind_10_seconds(self):
        current_position = self.get_position_millisecond()
        new_position = max(0, current_position - 1000)
        self.set_position(new_position)

    def rewind_start(self):
        self.set_position(0)

    def is_playing(self):
        p_command = f"status {self.DEVICE_ALIAS} mode"
        buffer_size = 128
        status_buffer = ctypes.create_unicode_buffer(buffer_size)
        error = self.mciSendString(p_command, status_buffer, buffer_size, 0)
        if "playing" in error:
            return "playing" in error
        elif "stopped" in error:
            return "Next Track"
        elif "paused" in error:
            return "paused"

    def get_position_millisecond(self):
        p_command = f"status {self.DEVICE_ALIAS} position"
        position_str = self.mciSendString(p_command)

        try:
            position_ms = int(position_str)
        except (ValueError, TypeError):
            position_ms = 0

        return position_ms

    def set_position(self, position):
        p_command = f"seek {self.DEVICE_ALIAS} to {position}"
        self.mciSendString(p_command)
        self.mciSendString(f"play {self.DEVICE_ALIAS}")

    def set_volume(self, slider: Literal["up", "down"] = "down"):
        if slider == "down":
            self.currentVol = max(0, self.currentVol - 100)
        elif slider == "up":
            self.currentVol = min(1000, self.currentVol + 100)

        p_command = f"setaudio {self.DEVICE_ALIAS} volume to {self.currentVol}"
        self.mciSendString(p_command)

    def close_media(self):
        self.mciSendString(f"close {self.DEVICE_ALIAS}")

    def close(self):
        try:
            self.close_media()
        except Exception as e:
            print(f"An error occurred while closing the media: {e}")
