def validate_byte_as_printable(byte):
    ## Check if byte is a printable ascii character. If not replace with a '.' character ##
    if byte < 128 and byte >= 32:
        return byte
    else:
        return '.'

def print_as_hex(new_string):
    memory_address = 0
    ascii_string = ""
    line = ""


    print("Offset 00 01 02 03 04 05 06 07 08 09 0A 0B 0C 0D 0E 0F")
    print("")
    ## Loop through the given file while printing the address, hex and ascii output ##
    for byte in new_string:
        ascii_string = ascii_string + str(validate_byte_as_printable(byte))
        if memory_address % 16 == 0:
            line = line + format(memory_address, '06X') + " "
            line = line + format(byte, "02X") + " "
        elif memory_address % 16 == 15:
            line = line + format(byte, "02X") + " "
            line = line + ascii_string
            print(line)
            ascii_string = ""
            line = ""
        else:
            line = line + format(byte, "02X") + " "

        memory_address = memory_address + 1

    for i in range((55 - len(line))):
        line = line + " "
    line = line + ascii_string
    print(line)

def print_details(r):
    print ("Headers:")
    print (r.headers)
    print ("Body")
    print ("Length of Body: "+str(len(r.data)))
    print (r.data)
