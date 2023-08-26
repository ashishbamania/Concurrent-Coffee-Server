from socket import socket, create_server

BUFFER_SIZE = 1024
ADDRESS = ("127.0.0.1", 12345)


class CoffeeServer:
    def __init__(self):
        try:
            self.server_socket = create_server(ADDRESS)
            self.server_socket.setblocking(False)
            print("Coffee server started at:", ADDRESS)
            self.clients = []
        except OSError:
            print("\nCoffee server stopped.")

    def accept(self):
        try:
            conn, client_address = self.server_socket.accept()
            print("Connected to a coffee lover at:", client_address)
            conn.setblocking(False)
            self.clients.append(conn)
        except BlockingIOError:
            pass

    def serve(self, conn):
        try:
            data = conn.recv(BUFFER_SIZE)
            if not data:
                self.clients.remove(conn)
                conn.close()
                return
            try:
                order = data.decode().strip()
                response = self.process_order(order)
            except ValueError:
                response = "Invalid order, please try again."
            conn.send(response.encode())
        except BlockingIOError:
            pass
        except OSError:
            self.clients.remove(conn)
            conn.close()

    def process_order(self, order):
        menu = {
            "1": "Your espresso is on its way!",
            "2": "Enjoy your latte!",
            "3": "Your cappuccino is coming right up!",
        }
        return menu.get(order, "Sorry, we don't have that option.")

    def start(self):
        print("Coffee server is ready to take orders")
        try:
            while True:
                self.accept()
                for conn in self.clients.copy():
                    self.serve(conn)
        finally:
            for conn in self.clients:
                conn.close()
            self.server_socket.close()
            print("\nCoffee server stopped.")


if __name__ == "__main__":
    coffee_server = CoffeeServer()
    coffee_server.start()
