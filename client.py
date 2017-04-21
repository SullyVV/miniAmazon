import socket
from google.protobuf.internal.decoder import _DecodeVarint32
from google.protobuf.internal.encoder import _VarintBytes
import amazon_pb2
import io
import threading
import time


HOST = 'colab-sbx-pvt-19.oit.duke.edu'
PORT = 23456


class Client():
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
        """
        check for first 4 bytes to determine response length. Since size is variable int, the length could be from 1 to 4
        need to take care of it in case swallowing the real message
        return response in string, need to parseFromString in the calling method
        """

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


        return rsp_buffer.getvalue()


    def close(self):
        self.sock.close()

    def AConnect(self):
        msg = amazon_pb2.AConnect()
        msg.worldid = 1000
        self.send(msg)
        self.recv()

    def process_AResponse(self) :
        """
         process response of Acommnads, store the information in database for future reference
        """

        while (1):
            str = self.recv()
            if (len(str) > 0):
                response = amazon_pb2.AResponses()
                try :
                    response.ParseFromString(str)
                    print(response)
                    print(len(str))
                except :
                    print("error")

    def ALoad(self, ship_id, truck_id):
        command = amazon_pb2.ACommands()
        command.simspeed = 100000
        pack = command.load.add()
        pack.whnum = 0
        pack.shipid = ship_id;
        pack.truckid = truck_id

        self.send(command)


    def AToPack(self, product_id, description, quantity, ship_id):
        command = amazon_pb2.ACommands()
        command.simspeed = 100000
        pack = command.topack.add()
        pack.whnum = 0
        pack.shipid = ship_id;
        pid = pack.things.add()
        pid.id = product_id
        pid.description = description
        pid.count = quantity
        self.send(command)


    def APurchase(self, product_id, description, quantity):
        command = amazon_pb2.ACommands()
        command.simspeed = 100000
        purchase = command.buy.add()
        purchase.whnum = 0
        pid = purchase.things.add()
        pid.id = product_id
        pid.description = description
        pid.count = quantity
        self.send(command)

if __name__ == '__main__':
    client = Client()
    client.connect()
    client.AConnect()

    # client.APurchase(1, "cake", 3)
    # client.APurchase(2, "apple", 4)
    threading.Thread(target=client.process_AResponse).start()
    # client.APurchase(3, "banana", 5)
    # client.APurchase(4, "orange", 6)
    # client.AToPack(3, "banana", 10, 6)
    client.ALoad(6, 0)

    while(1) :
        pass

    client.close()

