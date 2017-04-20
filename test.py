import socket
import struct
import errno
from os import write
import io
from google.protobuf.internal.decoder import _DecodeVarint32
from google.protobuf.internal.encoder import _VarintBytes
import amazon_pb2
HOST = 'colab-sbx-pvt-25.oit.duke.edu'
# HOST = 'www.google.com'
PORT = 23456

class InitClient():
    """
    BankSocket - prefix message with length when send/recv
    """
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # self.sock.setblocking(0)

    def connect(self, host=None, port=None):
        # connect to hostname on the port
        if host is None:
            host = HOST
        if port is None:
            port = PORT
        self.sock.connect((host, port))
        print("here")


    def send(self, msg):
        data_string = msg.SerializeToString()

        # might need further process
        # num_of_bytes = struct.pack('>f', len(data_string))
        # print(struct.pack('>f', 0))
        size = msg.ByteSize()
        self.sock.sendall(_VarintBytes(size))
        self.sock.sendall(data_string)

        # self.sock.sendall(data_string)
        # num_of_bytes = struct.pack('>Q', len(data_string))
        # self.sock.sendall(num_of_bytes + data_string)
        # num_of_bytes = self.sock.recv(4) #assume 4 bytes for size
        # message_size = struct.unpack(num_of_bytes)[0]
        # chunks = []
        # totle_bytes = 0
        # while totle_bytes < message_size:
        #     chunk = self.sock.recv(4096)
        #     chunks.append(chunk)
        #     totle_bytes += len(chunk)
        # print("received: " + chunks.size())
    def recv(self):
        # num_of_bytes = self.sock.recv(4)
        # message_size = struct.unpack('>i', num_of_bytes)[0]
        # print(message_size)
        # buf = self.sock.recv(4096)
        # n = 0
        # AConnected = amazon_pb2.AConnected()
        # msg_len, new_pos = _DecodeVarint32(buf, n)
        # msg_buf = buf[n:n + msg_len]
        # n += msg_len
        # try:
        #     AConnected.ParseFromString(msg_buf)
        # except:
        #     print(AConnected.error)

        buf = self.sock.recv(1)
        msg_len, new_pos = _DecodeVarint32(buf, 0)
        print("haha")
        databuf = self.sock.recv(msg_len)
        AConnected = amazon_pb2.AConnected()
        # msg_len, new_pos = _DecodeVarint32(buf, 0)
        # msg_buf = buf[new_pos:new_pos + msg_len]
        try:
            AConnected.ParseFromString(databuf)
            print("haha")
        except:
            print(AConnected.error)

        print(AConnected.error)








        # buf = self.sock.recv(4096)
        # AConnected = amazon_pb2.AConnected()
        # msg_len, new_pos = _DecodeVarint32(buf, 0)
        # msg_buf = buf[new_pos:new_pos+msg_len]
        # try:
        #     AConnected.ParseFromString(msg_buf)
        # except:
        #     print(AConnected.error)


    # def receive(self, conn):
    #     # read # bytes - prefix
    #     num_of_bytes = conn.recv(8)
    #     message_size = struct.unpack('>Q', num_of_bytes)[0]
    #     chunks = []
    #     totle_bytes = 0
    #     while totle_bytes < message_size:
    #         chunk = conn.recv(4096)
    #         chunks.append(chunk)
    #         totle_bytes += len(chunk)
    #
    #     message = pickle.loads(b''.join(chunks))
    #     return message

    def close(self):
        self.sock.close()

if __name__ == '__main__':
    client = InitClient()
    client.connect()
    # whs = amazon_pb2.AInitWarehouse()
    msg = amazon_pb2.AConnect()
    print(msg)
    msg.worldid = 1008
    print(msg)
    client.send(msg)
    client.recv()
    client.close()