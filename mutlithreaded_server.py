from socket import socket, create_server
import threading

BUFFER_SIZE = 1024
ADDRESS = ("127.0.0.1", 12345)


class CoffeeServer:
    def __init__(self):
        try:
            self.server_socket = create_server(ADDRESS)
            print("Coffee server started at:", ADDRESS)
        except OSError:
            print("\nCoffee server stopped.")

    def accept(self):
        conn, client_address = self.server_socket.accept()
        print("Connected to a coffee lover at:", client_address)
        return conn

    def serve(self, conn):
        try:
            while True:
                order = conn.recv(BUFFER_SIZE).decode().strip()
                if not order:
                    break
                response = self.process_order(order)
                conn.send(response.encode())
        finally:
            print("Connection with", conn.getpeername(), "closed")
            conn.close()

    def process_order(self, order):
        menu = {
            "1": "Your espresso is on its way!",
            "2": "Enjoy your latte!",
            "3": "Your cappuccino is coming right up!",
        }
        return menu.get(order, "Sorry, we don't have that option.")

    def handle_client(self, conn):
        try:
            self.serve(conn)
        except Exception as e:
            print("An error occurred:", e)
        finally:
            conn.close()

    def start(self):
        print("Coffee server is ready to take orders")
        try:
            while True:
                conn = self.accept()
                client_thread = threading.Thread(
                    target=self.handle_client, args=(conn,))
                client_thread.start()
        finally:
            self.server_socket.close()
            print("\nCoffee server stopped.")


if __name__ == "__main__":
    coffee_server = CoffeeServer()
    coffee_server.start()
