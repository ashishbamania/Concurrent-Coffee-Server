import selectors
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
            self.selector = selectors.DefaultSelector()
            self.selector.register(
                self.server_socket, selectors.EVENT_READ, self.accept)
        except OSError:
            print("\nCoffee server stopped.")

    def accept(self, source, _):
        try:
            conn, client_address = source.accept()
            print("Connected to a coffee lover at:", client_address)
            conn.setblocking(False)
            self.clients.append(conn)
            self.selector.register(conn, selectors.EVENT_READ, self.serve)
        except BlockingIOError:
            pass

    def serve(self, source, _):
        try:
            data = source.recv(BUFFER_SIZE)
            if not data:
                self.clients.remove(source)
                self.selector.unregister(source)
                source.close()
                return
            try:
                order = data.decode().strip()
                response = self.process_order(order)
            except ValueError:
                response = "Invalid order, please try again."
            source.send(response.encode())
        except BlockingIOError:
            pass
        except OSError:
            self.clients.remove(source)
            self.selector.unregister(source)
            source.close()

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
                events = self.selector.select()
                for key, _ in events:
                    callback = key.data
                    callback(key.fileobj, _)
        finally:
            for conn in self.clients:
                conn.close()
            self.server_socket.close()
            print("\nCoffee server stopped.")


if __name__ == "__main__":
    coffee_server = CoffeeServer()
    coffee_server.start()
