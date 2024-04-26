import socket
import hashlib
import os
import sys
import argparse
import time
import logging
from datetime import datetime

FILE_SIZE = 1024  # 1KB
CLIENT_DIR = 'clientdata'


logging.basicConfig(
    level=logging.INFO,  
    format='%(asctime)s - %(levelname)s - %(message)s', 
    datefmt='%Y-%m-%d %H:%M:%S' 
)
logger = logging.getLogger(__name__)


def compute_checksum(data):
    checksum = hashlib.md5(data).hexdigest()
    return checksum


def create_directory(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)


def client(host, port):
    create_directory(CLIENT_DIR)

    server_address = (host, port)

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            try:
                client_socket.connect(server_address)
            except ConnectionRefusedError:
                logger.error("Connection refused: Unable to connect to the server.")
                sys.exit(1)

            logger.info(f"Connected to server at {host}:{port}")

            timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
            file_path = os.path.join(CLIENT_DIR, f'client_file_{timestamp}.txt')

            logger.info(f"Receiving file from server and saving to {file_path}...")
            with open(file_path, 'wb') as file:
                received_data = client_socket.recv(FILE_SIZE)
                file.write(received_data)

            logger.info("File received successfully.")

            received_checksum = client_socket.recv(32).decode()
            computed_checksum = compute_checksum(received_data)

            if received_checksum == computed_checksum:
                logger.info("Checksum verified. File stored successfully.")
            else:
                logger.warning("Checksum mismatch. File may be corrupted.")

            time.sleep(60)    
    except ConnectionResetError:
        logger.error("Connection with the server was forcibly closed.")
    finally:
        sys.exit(0)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Client for file transfer")
    parser.add_argument('--host', default='localhost', help="Host IP address (default: localhost)")
    parser.add_argument('--port', type=int, default=13101, help="Port number (default: 13101)")
    args = parser.parse_args()

    client(args.host, args.port)
