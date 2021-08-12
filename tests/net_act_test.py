import pytest

def test_import():
    from ceaos.networkactuation import NetworkActuation

def test_workflow():
    from ceaos.networkactuation import NetworkActuation
    import zmq
    import threading
    import json

    def do(obj):
        print(obj)
    
    def create_listener():
        NA = NetworkActuation()
        NA.register_do(do,dtype=bool)
        NA.listen(port=26521)
    
    listener = threading.Thread(target=create_listener, daemon=True)
    listener.start()

    context = zmq.Context()
    socket = context.socket(zmq.REQ)
    socket.connect("tcp://localhost:26521")
    socket.send_string(json.dumps({'action': 'do', 'payload':True}))
    reply = socket.recv()
    reply = json.loads(reply)
    listener.join(0.1)

    assert reply['status'] == 200

def test_conditions():
    from ceaos.networkactuation import NetworkActuation
    import zmq
    import threading
    import json

    def do(obj):
        print(obj)
    
    def create_listener():
        NA = NetworkActuation()
        NA.register_do(do,dtype=bool)
        NA.listen(port=26521)
    
    listener = threading.Thread(target=create_listener, daemon=True)
    listener.start()

    context = zmq.Context()
    socket = context.socket(zmq.REQ)
    socket.connect("tcp://localhost:26521")
    socket.send_string(json.dumps({'action': 'do', 'payload':'testing'}))
    reply = socket.recv()
    reply = json.loads(reply)
    print(reply)
    listener.join(0.1)

    assert reply['status'] == 200

