import vlc
import requests
import json
import os
from pathlib import Path

class MusicPlayer:
    def __init__(self):
        self.instance = vlc.Instance()
        self.player = self.instance.media_player_new()
        self.current_station = None
        self.custom_stations = self.load_custom_stations()

    def play_bok_radio(self):
        # Bok Radio 98.9 FM live stream URL
        url = "https://streaming.fabrik.fm/bokradio/echocast/audio/index.m3u8"
        self._play_url(url)
        self.current_station = "Bok Radio"

    def play_custom_station(self, name):
        if name in self.custom_stations:
            self._play_url(self.custom_stations[name])
            self.current_station = name
        else:
            raise ValueError(f"Station '{name}' not found in custom list")

    def add_custom_station(self, name, url):
        self.custom_stations[name] = url
        self.save_custom_stations()

    def _play_url(self, url):
        media = self.instance.media_new(url)
        self.player.set_media(media)
        self.player.play()

    def stop(self):
        self.player.stop()

    def load_custom_stations(self):
        config_path = Path.home() / ".stormy" / "stations.json"
        if config_path.exists():
            with open(config_path) as f:
                return json.load(f)
        return {}

    def save_custom_stations(self):
        config_path = Path.home() / ".stormy" / "stations.json"
        config_path.parent.mkdir(parents=True, exist_ok=True)
        with open(config_path, "w") as f:
            json.dump(self.custom_stations, f)
