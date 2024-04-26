import socket
import hashlib
import os
import sys
import argparse
import logging
from datetime import datetime

FILE_SIZE = 1024  # 1KB
SERVER_DIR = 'serverdata'


logging.basicConfig(
    level=logging.INFO,  
    format='%(asctime)s - %(levelname)s - %(message)s', 
    datefmt='%Y-%m-%d %H:%M:%S' 
)
logger = logging.getLogger(__name__)


def generate_random_file(file_path):
    with open(file_path, 'wb') as file:
        file.write(os.urandom(FILE_SIZE))


def compute_checksum(file_path):
    with open(file_path, 'rb') as file:
        checksum = hashlib.md5(file.read()).hexdigest()
    return checksum


def create_directory(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)


def server(host, port):
    create_directory(SERVER_DIR)

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(1)
    logger.info(f"Server listening on {host}:{port}")

    try:
        while True:
            client_socket, client_address = server_socket.accept()
            client_host, client_port = client_address
            logger.info(f"Connection established with {client_host}:{client_port}")

            timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
            file_path = os.path.join(SERVER_DIR, f'server_file_{timestamp}.txt')
            logger.info(f"Generating random file: {file_path}")
            generate_random_file(file_path)

            logger.info("Computing checksum...")
            checksum = compute_checksum(file_path)

            logger.info("Sending file and checksum to client...")
            with open(file_path, 'rb') as file:
                file_data = file.read()
                client_socket.sendall(file_data)
                client_socket.sendall(checksum.encode())

            logger.info("File and checksum sent successfully.")

            client_socket.close()
            logger.info("Connection closed with client.")
            logger.info("")
    except KeyboardInterrupt:
        logger.info("Server interrupted by KeyboardInterrupt. Closing connections.")
    finally:
        server_socket.close()
        logger.info("Server socket closed.")
        sys.exit(0)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Server for file transfer")
    parser.add_argument('--host', default='localhost', help="Host IP address (default: localhost)")
    parser.add_argument('--port', type=int, default=13101, help="Port number (default: 13101)")
    args = parser.parse_args()

    server(args.host, args.port)
