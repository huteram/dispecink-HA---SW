import struct


class DataTypes:
    Types = {}

    def __init__(self):
        self.Types["SwappedFloat"] = self.SwappedFloat
        self.Types["UINT16"] = self.UINT16
        self.Types["UINT32"] = self.UINT32
        self.Types["SINT16"] = self.SINT16
        self.Types["MaskedBool"] = self.MaskedBool
        self.Types["S32-M10k-2143"] = self.SINT32

    def getStringBytes(self, Bytes):
        result = ''
        for i in Bytes:
            Hex = hex(i)[2:]
            result += "0" * (4 - len(Hex)) + Hex

        return bytes.fromhex(result)

    def SwappedFloat(self, Bytes, Scale=1, bytesNumber=4):
        Bytes = self.getStringBytes(Bytes)

        # Python 3 fix → bytes are ints, must rebuild bytes object
        BytesSwapped = bytes([
            Bytes[1], Bytes[0],
            Bytes[3], Bytes[2]
        ])

        result = struct.unpack('f', BytesSwapped)[0]
        return result / Scale

    def UINT16(self, Bytes, Scale):
        value = Bytes[0]
        return float(value / Scale)

    def convertByte(self, Byte):
        # Python 3 fix → Byte is already int
        r = str(Byte)
        r = "0" * (2 - len(r)) + r
        return r

    def UINT32(self, Bytes, Scale):
        Bytes = self.getStringBytes(Bytes)

        BytesSwapped = ''
        BytesSwapped += self.convertByte(Bytes[0])
        BytesSwapped += self.convertByte(Bytes[1])
        BytesSwapped += self.convertByte(Bytes[2])
        BytesSwapped += self.convertByte(Bytes[3])

        print(BytesSwapped)

        Int = int(BytesSwapped, 32)
        return float(Int / Scale)

    def SINT16(self, Bytes, Scale):
        Bytes = self.getStringBytes(Bytes)
        Int = struct.unpack(">h", Bytes)[0]

        print(Int, Scale)

        return float(Int / Scale)

    def SINT32(self, Bytes, Scale):
        Bytes = self.getStringBytes(Bytes)
        Int = struct.unpack(">i", Bytes)[0]

        print(Int, Scale)

        return float(Int / Scale)

    def MaskedBool(self, Bytes, Scale):
        if Bytes[0] > 0:
            return 1
        else:
            return 0


if __name__ == '__main__':
    ff = DataTypes()

    a = [
        262, 768, 0, 0, 0, 0, 1, 0, 0, 0, 0,
        17254, 26214, 16842, 0, 16512, 0,
        17372, 42598, 17384, 0, 17000,
        10486, 16588, 0, 58, 54, 0, 81, 0,
        5243, 16574, 0, 0, 0, 0, 5243, 16574,
        0, 17058, 36700, 16654, 0, 0, 0, 0,
        36700, 16654, 0, 0
    ]

    print(ff.Types["SwappedFloat"](a[20:22]))
    print(ff.Types["SwappedFloat"](a[46:48]))
    print(ff.UINT32(a[0:2], 1))