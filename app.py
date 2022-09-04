import sys
from FlagReader import FlagReader

# Do not close console after error
def exc_handler(exc_type, exc_value, tb):
    import traceback
    traceback.print_exception(exc_type, exc_value, tb)
    input("Press Enter to exit.")
    sys.exit(-1)
sys.excepthook = exc_handler

dropped_file = sys.argv[1]
if dropped_file.endswith('.wdt'):
    with open(sys.argv[1], 'rb+') as file:
        flags_start = file.read().find(b'DHPM') + 4 + 4 # MPHD + Skip chunk name + Skip chunk size
        file.seek(flags_start)

        flags = int.from_bytes(file.read(4), byteorder='little')
        flags = FlagReader.read(flags)

        new_flags = 0
        for i in range(len(flags)):
            if (flags[i] == 0x100) or (flags[i] == 0x8000):
                continue
            new_flags += flags[i]

        new_flags = int.to_bytes(new_flags, 4, 'little')
        file.seek(flags_start)
        file.write(new_flags)