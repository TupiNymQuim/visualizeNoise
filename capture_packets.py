import pyshark
from influxdb_client import InfluxDBClient, Point, WritePrecision
import time

# Configurações do InfluxDB
influx_url = "http://localhost:8086"  # URL do seu InfluxDB
influx_token = "ehyisCSiwzbeWJqbd3w6UNI4TiJpRS6ohQir4ZcqPlXUG2tzTkbKkhnmaOthAod00AeY_tMpTI6kLHPyAKJfbQ=="  # O token de autenticação
org = "TupiNymQuim"  # Nome da sua organização
bucket = "PacketCount"  # O nome do seu bucket

# Criação do cliente InfluxDB
client = InfluxDBClient(url=influx_url, token=influx_token)
# Use WriteApi sem o WritePrecision (caso o erro persista)
write_api = client.write_api()

# Função para capturar pacotes
def capture_packets(interface="wlp0s20f3", interval=5):
    # Inicia captura de pacotes na interface de rede
    cap = pyshark.LiveCapture(interface=interface)

    start_time = time.time()
    packet_count = 0

    for packet in cap:
        # Cria um ponto de dados para cada pacote
        packet_count += 1

        if time.time() - start_time >= interval:
            point = Point("network_packet").tag("type", "total").field("count", packet_count)
            write_api.write(bucket=bucket, org=org, record=point)
            points = []
            start_time = time.time()
            print(f"Pacotes enviados: {packet_count}")
            packet_count = 0

        # Registra o contador total de pacotes
        # write_api.write(bucket=bucket, org=org, record=point)


if __name__ == "__main__":
    print("Iniciando captura de pacotes...")
    capture_packets()

