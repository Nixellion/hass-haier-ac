# https://github.com/bstuff/haier-ac-remote/blob/master/packages/haier-ac-remote/src/lib/raw-commands.ts
# https://github.com/bstuff/haier-ac-remote/blob/master/packages/haier-ac-remote/src/lib/commands.ts
# https://extendsclass.com/typescript-to-javascript.html
# https://pypi.org/project/Js2Py/

import socket
import js2py
from threading import Thread
import re

IP = "192.168.1.160"
MAC = "0007A8CE01E7"

IP2 = "192.168.1.165"
MAC2 = "0007A8CDFFB0"

PORT = 56800

reference = """
00000000: 0000 2714 0000 0000 0000 0000 0000 0000  ..'.............
00000010: 0000 0000 0000 0000 0000 0000 0000 0000  ................
00000020: 0000 0000 0000 0000 3030 3037 4138 4539  ........0007A8E9
00000030: 3137 4143 0000 0000 0000 0000 0000 0000  17AC............
00000040: 0000 0000 0000 0000 0000 0001 0000 000d  ................
00000050: ffff 0a00 0000 0000 0001 4d02 5a         ..........M.Z
"""


class cmds():
    request = "00 00 27 14 00 00 00 00"
    response = "00 00 27 15 00 00 00 00"
    zero16 = "00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00"
    hello = "ff ff 0a 00 00 00 00 00 00 01 4d 01 59"
    on = "ff ff 0a 00 00 00 00 00 00 01 4d 02 5a"
    off = "ff ff 0a 00 00 00 00 00 00 01 4d 03 5b"
    init = "ff ff 08 00 00 00 00 00 00 73 7b"

    @staticmethod
    def mac_address(mac):
        # https://github.com/bstuff/haier-ac-remote/blob/e16964b93a89aa4e57cc4a2bfedacee4ab8dd220/packages/haier-ac-remote/src/lib/commands.ts#L54
        mac = re.sub(r"[^a-f\d]", "", mac, flags=re.IGNORECASE).upper()
        mac = mac.replace(":", "")
        res = []

        for i in mac:
            res.append('%x' % ord(i))

        res.extend(["00"] * 4)

        return " ".join(res)

    @staticmethod
    def order_byte(n):
        """
        # TODO Convert to python
        """
        code = '''function (n) {
            return n % 256 < 16 ? "00 00 00 0" + (n % 256).toString(16) : "00 00 00 " + (n % 256).toString(16);
        }
        '''
        # f = js2py.eval_js(code)
        # return f(n)
        nstring = ('%x' % (n % 256))
        if n % 256 < 16:
            return "00 00 00 0" + nstring
        else:
            return "00 00 00 " + nstring

    @staticmethod
    def len4(cmd):
        """
        TODO Convert to python
        """
        code = '''
        function (cmd) {
            var length = cmd.replace(/[^0-f]/g, '').split('').length / 2;
            return orderByte(length);
        }
        '''
        # f = js2py.eval_js(code)
        # return f(cmd)

        length = int(len(cmd.replace(" ", "")) / 2)
        return cmds.order_byte(length)


def to_hex(*args):
    s = "".join(args)
    s = re.sub(r'[^0-f]', '', s)
    return bytes(bytearray.fromhex(s))
    # return s.encode()


class HaierAC():
    def __init__(self, ip, mac, port=56800):
        self.ip = ip
        self.mac = mac
        self.port = port
        self.socket = socket.socket()
        self.socket.settimeout(1)
        self._seq = 0

    def connect(self):
        self.socket.connect((self.ip, self.port))

    def disconnect(self):
        print("Closing...")
        self.socket.close()

    def send(self, command, seq):
        self._seq = (self._seq + 1) % 256
        # seq = self._seq
        a = to_hex(
            cmds.request,
            cmds.zero16,
            cmds.zero16,
            cmds.mac_address(self.mac),
            cmds.zero16,
            cmds.order_byte(seq),
            cmds.len4(command),
            command
        )
        print("REQUEST", a)
        self.socket.send(a)
        data = self.socket.recv(1024)
        print("RESPONSE", data)


haier = HaierAC(IP, MAC)
haier.connect()
haier.send(cmds.hello, 0)
haier.send(cmds.init, 1)
haier.send(cmds.on, 2)
haier.disconnect()
