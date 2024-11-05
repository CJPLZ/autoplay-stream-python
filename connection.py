import requests
import time
import vlc

class ConnectionManager:
    def __init__(self, player, url):
        self.player = player
        self.stream_url = url

    def check_internet_connection(self):
        """Verificar la conexión a Internet."""
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
        """Verificar si el stream está accesible."""
        try:
            response = requests.head(self.stream_url, timeout=2)  # Reducir el tiempo de espera
            return response.status_code == 200
        except requests.RequestException:
            return False

    def reconnect(self):
        """Intentar reconectar al stream si se pierde la señal."""
        print("Intentando reconectar al stream...")
        while not self.check_stream_accessible():
            print("Stream no accesible. Intentando nuevamente...")
            time.sleep(1)  # Esperar antes de intentar nuevamente (1 segundo)
        print("Stream accesible. Reproduciendo...")
        self.player.play_stream(self.stream_url)

    def monitor_connection(self, update_status_callback):
        """Monitorear la conexión y realizar reconexiones si es necesario."""
        while True:
            internet_connected = self.check_internet_connection()
            stream_connected = self.player.player.get_state() == vlc.State.Playing

            # Si no hay conexión a Internet, el stream no puede estar conectado
            if not internet_connected:
                stream_connected = False

            if internet_connected and not stream_connected:
                # Intentar reconectar solo si el stream no está en reproducción
                if self.check_stream_accessible():
                    self.player.play_stream(self.stream_url)
                else:
                    print("Stream no accesible. Intentando reconectar...")
                    self.reconnect()

            elif not internet_connected and stream_connected:
                # Si se pierde la conexión a internet, detener el stream
                print("Conexión a Internet perdida. Deteniendo el stream.")
                self.player.stop_stream()

            # Si el stream está desconectado, intentar reconectar
            if not stream_connected:
                print("Stream desconectado. Intentando reconectar...")
                self.reconnect()

            update_status_callback(internet_connected, stream_connected)

            time.sleep(1)  # Esperar un segundo antes de la siguiente comprobación
