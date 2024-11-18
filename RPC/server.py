from xmlrpc.server import SimpleXMLRPCRequestHandler,SimpleXMLRPCServer

class MathOperations:
    def add(self, x:int, y:int):
        return x + y

    def subtract(self, x:int, y:int):
        return x - y

    def square(self, x:int):
        return x * x

    def cube(self, x:int):
        return x * x * x

class Requesthandler(SimpleXMLRPCRequestHandler):
    rpc_paths = ('/RPC2',)
def main():
    
    server = SimpleXMLRPCServer(('localhost',8000),requestHandler=Requesthandler)
    server.register_instance(MathOperations())
    
    print("Server is listening to port 8000")
    server.serve_forever()
    
if __name__ == "__main__":
    main()