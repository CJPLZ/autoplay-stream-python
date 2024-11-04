import vlc

class StreamPlayer:
    def __init__(self):
        # Configurar VLC con un buffer mínimo
        self.instance = vlc.Instance("--network-caching=100")  # 100 ms de buffering
        self.player = self.instance.media_player_new()

    def play_stream(self, url):
        media = self.instance.media_new(url)
        self.player.set_media(media)
        self.player.play()

    def stop(self):
        self.player.stop()

    def toggle_play_pause(self):
        if self.player.is_playing():
            self.player.pause()
            return "Play"
        else:
            self.player.play()
            return "Pause"

    def set_volume(self, volume):
        self.player.audio_set_volume(int(volume))