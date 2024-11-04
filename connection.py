import requests
import time
import vlc

class ConnectionManager:
    def __init__(self, player, url):
        self.player = player
        self.stream_url = url

    def check_internet_connection(self):
        try:
            requests.get("http://www.google.com", timeout=2)  # Reducir el tiempo de espera
            return True
        except requests.ConnectionError:
            return False
        except requests.Timeout:
            print("Timeout al intentar conectar a Internet.")
            return False
        except Exception as e:
            print(f"Ocurrió un error inesperado: {e}")
            return False

    def check_stream_accessible(self):
        try:
            response = requests.head(self.stream_url, timeout=2)  # Reducir el tiempo de espera
            return response.status_code == 200
        except requests.RequestException:
            return False

    def monitor_connection(self, update_status_callback):
        while True:
            internet_connected = self.check_internet_connection()
            stream_connected = self.player.player.get_state() == vlc.State.Playing

            # Si no hay conexión a Internet, el stream no puede estar conectado
            if not internet_connected:
                stream_connected = False

            if internet_connected and not stream_connected:
                if self.check_stream_accessible():
                    self.player.play_stream(self.stream_url)
                else:
                    print("Stream no accesible.")
            update_status_callback(internet_connected, stream_connected)
            time.sleep(0.5)  # Reducir el tiempo de espera entre comprobaciones