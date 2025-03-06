import pyshark
from influxdb_client import InfluxDBClient, Point, WritePrecision
import time

# Configurações do InfluxDB
influx_url = "http://localhost:8086"  # URL do seu InfluxDB
influx_token = "EFuJl_vxykaQflccR6V8c4I0mMXce1z_QiYkHmBvKd7yJsQJqgGfRbD1qWav6fTbZWxWb30ZVpj0RFpNb-W24Q=="  # O token de autenticação
org = "tupinymquim"  # Nome da sua organização
bucket = "my-bucket"  # O nome do seu bucket

# Criação do cliente InfluxDB
client = InfluxDBClient(url=influx_url, token=influx_token)
# Use WriteApi sem o WritePrecision (caso o erro persista)
write_api = client.write_api()

# Função para capturar pacotes
def capture_packets(interface="wlp0s20f3"):
    # Inicia captura de pacotes na interface de rede
    cap = pyshark.LiveCapture(interface=interface)

    for packet in cap:
        # Cria um ponto de dados para cada pacote
        point = Point("network_packet")  # Nome da medida

        # Registra o contador total de pacotes
        point.tag("type", "total")
        point.field("count", 1)  # Cada pacote é contado com valor 1
        write_api.write(bucket=bucket, org=org, record=point)

        # Verifica o tipo de pacote e envia para o InfluxDB
        if 'TCP' in packet:
            point = Point("network_packet").tag("type", "tcp").field("count", 1)
            write_api.write(bucket=bucket, org=org, record=point)
        elif 'UDP' in packet:
            point = Point("network_packet").tag("type", "udp").field("count", 1)
            write_api.write(bucket=bucket, org=org, record=point)
        elif 'ICMP' in packet:
            point = Point("network_packet").tag("type", "icmp").field("count", 1)
            write_api.write(bucket=bucket, org=org, record=point)

        # Registra o tamanho do pacote
        point = Point("network_packet_size").tag("type", "size").field("size_bytes", len(packet))
        write_api.write(bucket=bucket, org=org, record=point)

if __name__ == "__main__":
    print("Iniciando captura de pacotes...")
    capture_packets()

