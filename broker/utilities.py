def validate_byte_as_printable(byte):
    """
    @param byte: a Byte
    @return: either the byte or a . if the byte is note printable

    This function returns either the character passed to it or a period (.) if it is not able to be printed
    """
    ## Check if byte is a printable ascii character. If not replace with a '.' character ##
    if ord(byte) < 128 and ord(byte) >= 32:
        return byte
    else:
        return '.'


def print_as_hex(new_string):
    memory_address = 0
    ascii_string = ""
    line = ""

    print("Offset 00 01 02 03 04 05 06 07 08 09 0A 0B 0C 0D 0E 0F")
    ## Loop through the given file while printing the address, hex and ascii output ##
    for byte in new_string:
        ascii_string = ascii_string + validate_byte_as_printable(byte)
        if memory_address % 16 == 0:
            line = line + format(memory_address, '06X') + " "
            line = line + format(ord(byte), "02X") + " "
        elif memory_address % 16 == 15:
            line = line + format(ord(byte), "02X") + " "
            line = line + ascii_string
            print(line)
            ascii_string = ""
            line = ""
        else:
            line = line + format(ord(byte), "02X") + " "

        memory_address = memory_address + 1

    for i in range((55 - len(line))):
        line = line + " "
    line = line + ascii_string
    print(line)

def print_details(r):
    print ("Headers:")
    print ("--------")
    print (r.headers)
    print ("Parameters")
    print ("----------")
    print (str(r.args.to_dict()))
    print ("Body:")
    print ("-----")
    print ("Length: "+str(len(r.data)))
    new_string = str(r.data.decode('utf-8'))
    print_as_hex(new_string)
