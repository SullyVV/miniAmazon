import socket
from google.protobuf.internal.decoder import _DecodeVarint32
from google.protobuf.internal.encoder import _VarintBytes
import amazon_pb2
import io

HOST = 'colab-sbx-pvt-19.oit.duke.edu'
PORT = 23456

class InitClient():
    """
 
    """
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)


    def connect(self, host=None, port=None):
        # connect to hostname on the port
        if host is None:
            host = HOST
        if port is None:
            port = PORT
        self.sock.connect((host, port))


    def send(self, msg):
        data_string = msg.SerializeToString()
        size = msg.ByteSize()
        self.sock.sendall(_VarintBytes(size))
        self.sock.sendall(data_string)

    def recv(self):
        #int length is at most 4 bytes long
        hdr_bytes = self.sock.recv(4)
        (msg_length, hdr_length) = _DecodeVarint32(hdr_bytes, 0)
        rsp_buffer = io.BytesIO()
        if hdr_length < 4:
            rsp_buffer.write(hdr_bytes[hdr_length:])

        # read the remaining message bytes
        msg_length = msg_length - (4 - hdr_length)
        while msg_length > 0:
            rsp_bytes = self.sock.recv(min(8096, msg_length))
            rsp_buffer.write(rsp_bytes)
            msg_length = msg_length - len(rsp_bytes)

        AConnected = amazon_pb2.AConnected()
        AConnected.ParseFromString(rsp_buffer.getvalue())
        #print(AConnected.error)

    def close(self):
        self.sock.close()

    def AConnect(self):
        msg = amazon_pb2.AConnect()
        msg.worldid = 1008
        self.send(msg)
        return self.recv()

    def APurchase(self):
        command = amazon_pb2.ACommands()
        command.simspeed = 100000000
        purchase = command.buy.add()
        purchase.whnum = 0
        goods = purchase.things.add()
        goods.id = 1
        goods.description = 'andrew'
        goods.count = 3
        client.send(command)
        client.recv()

if __name__ == '__main__':
    client = InitClient()
    client.connect()
    client.AConnect()
    client.APurchase()
    while (1):
        pass


