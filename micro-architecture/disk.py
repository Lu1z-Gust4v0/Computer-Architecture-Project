from memory import memory


class Disk:
    def __init__(self, memory=memory):
        self.memory = memory

    def read(self, image):
        byte_address = 0

        with open(image, "rb") as file:
            byte = file.read(1)

            while byte:
                litte_end_byte = int.from_bytes(byte, "little")
                self.memory.write_byte(byte_address, litte_end_byte)
                byte = file.read(1)

                byte_address += 1


disk = Disk()
