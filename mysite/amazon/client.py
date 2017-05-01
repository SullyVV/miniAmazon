import io
import socket
import threading

#from django.shortcuts import get_object_or_404
from google.protobuf.internal.decoder import _DecodeVarint32
from google.protobuf.internal.encoder import _VarintBytes

from . models import Whstock, Transaction
from . import amazon_pb2
from . import AU_pb2

HOST = 'colab-sbx-pvt-25.oit.duke.edu'
PORT = 23456

UPS_HOST = "colab-sbx-63.oit.duke.edu"
UPS_PORT = 34567

class Client():
    """
 
    """
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        self.Usock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.Usock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)


    def connect(self):
        # connect to hostname on the port

        self.sock.connect((HOST, PORT))
        self.Usock.connect((UPS_HOST, UPS_PORT))


    def send(self, msg, sock):
        data_string = msg.SerializeToString()
        size = msg.ByteSize()
        sock.sendall(_VarintBytes(size))
        sock.sendall(data_string)

    def recv(self, sock):
        """
        check for first 4 bytes to determine response length. Since size is variable int, the length could be from 1 to 4
        need to take care of it in case swallowing the real message
        return response in string, need to parseFromString in the calling method
        """

        #int length is at most 4 bytes long
        hdr_bytes = sock.recv(1)
        (msg_length, hdr_length) = _DecodeVarint32(hdr_bytes, 0)
        rsp_buffer = io.BytesIO()
        if hdr_length < 4:
            rsp_buffer.write(hdr_bytes[hdr_length:])

        # read the remaining message bytes
        # msg_length = msg_length - (4 - hdr_length)
        while msg_length > 0:
            rsp_bytes = sock.recv(min(8096, msg_length))
            rsp_buffer.write(rsp_bytes)
            msg_length = msg_length - len(rsp_bytes)
        return rsp_buffer.getvalue()


    def close(self):
        self.sock.close()
        self.Usock.close()

    def AConnect(self):
        msg = amazon_pb2.AConnect()
        msg.worldid = 1000
        self.send(msg, self.sock)
        print(self.recv(self.sock))


    def process_Uresponse(self, trans):
        """
        save package_id and send Aload command
        :param trans: 
        :return: 
        """
        while (1):
            str = self.recv(self.Usock)
            if (len(str) > 0):
                response = AU_pb2.UA()
                # try:
                print(str)
                response.ParseFromString(str)
                print(response)
                if (response != None):
                    self.ALoad(trans.ship_id, response.truckid)
                    trans.package_id = response.packageid
                    trans.save()
                    return
                # except:
                #     print('error')

    def AUCommand(self, trans, flag):
        command = AU_pb2.AU()
        command.flag = flag
        command.shipid = trans.ship_id
        command.whid = trans.stock.hid
        # not yet tested (detail of package)
        command.detailofpackage = trans.product_name + ":" + trans.product_num
        if trans.package_id is not -1:
            command.packageid = trans.package_id
        command.x = trans.address_x
        command.y = trans.address_y
        if trans.ups_act is not -1:
            command.ups_id = trans.ups_act
        self.send(command, self.Usock)

    def process_AResponse(self) :
        """
         process response of Acommnads, store the information in database for future reference
        """
        while (1):
            str = self.recv(self.sock)
            if (len(str) > 0):
                response = amazon_pb2.AResponses()
                response.ParseFromString(str)
                print(response)
                # handle import new stock
                for arrive in response.arrived:
                    things = arrive.things
                    for thing in things:
                        products = Whstock.objects.filter(pid = thing.id)
                        if len(products) != 0:
                            products[0].count = products[0].count + thing.count
                            products[0].save()
                        else :
                            #need to specify world id
                            whstock = Whstock()
                            whstock.hid = arrive.whnum
                            whstock.pid = thing.id
                            whstock.dsc = thing.description
                            whstock.count = thing.count
                            whstock.save()
                # handle pack ready response
                #when ready send AU command to let UPS truck pickup,
                #use another thread for wait for UPS response
                #when receive response send ALoad command
                #when reveived loaded for Sim send AU command and let flag = 1;
                # tell UPS packages is ready and ask for trucks (provide destinaiton address)
                # tell warehouse to load when UPS trucks ready
                for currReady in response.ready:
                    #save current state
                    trans = Transaction.objects.get(ship_id = currReady)
                    trans.ready = True
                    trans.save()
                    #connect to UPS
                    ups_handler = threading.Thread(target=self.process_Uresponse, args=(trans,))
                    ups_handler.start()
                    self.AUCommand(trans, 0)
                    print("first msg for UPS sent(to pickup)")
                    ups_handler.join()

                #load info from sim
                for load in response.loaded:
                    #save current state
                    trans = Transaction.objects.get(ship_id = load)
                    trans.loaded = True
                    trans.save()
                    #connect to UPS
                    self.AUCommand(trans, 1)
                    print("second msg for UPS sent(get load success from sim world)")

    def ALoad(self, ship_id, truck_id):
        command = amazon_pb2.ACommands()
        command.simspeed = 100000
        pack = command.load.add()
        pack.whnum = 0
        pack.shipid = ship_id;
        pack.truckid = truck_id

        self.send(command , self.sock)


    def AToPack(self, product_id, description, quantity, ship_id):
        """
        ship_id should be unique per ship
        """     
        command = amazon_pb2.ACommands()
        command.simspeed = 100000
        pack = command.topack.add()
        pack.whnum = 0
        pack.shipid = ship_id;
        pid = pack.things.add()
        pid.id = product_id
        pid.description = description
        pid.count = quantity
        self.send(command, self.sock)


    def APurchase(self, product_id, description, quantity):
        command = amazon_pb2.ACommands()
        command.simspeed = 100000
        purchase = command.buy.add()
        purchase.whnum = 0
        pid = purchase.things.add()
        pid.id = product_id
        pid.description = description
        pid.count = quantity
        self.send(command, self.sock)

if __name__ == '__main__':
    print("start")
    client = Client()
    client.connect()
    client.AConnect()
    #client.connect(UPS_HOST, UPS_PORT, self.Usock)
    # client.APurchase(1, "cake", 3)
    # client.APurchase(2, "apple", 4)
    response_handler = threading.Thread(target=client.process_AResponse)
    response_handler.start()
    client.APurchase(3, "banana", 5)
    #client.APurchase(4, "orange", 6)
    # time.sleep(3)
    # client.AToPack(3, "banana", 10, 6)
    # time.sleep(3)
    # client.ALoad(6, 0)
    response_handler.join()
    client.close()

