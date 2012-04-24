import logging

def byteListPrintables(bytes):
    """Return string of printable ASCII characters in a given byte array.
    
    Similarly to many Hex-Editors, non-printable charaters are replaced
    by an period.
    
    """    
    return ''.join([chr(x) if 31 < x < 128 else '.' for x in bytes])


def typeName(typeNo):
    """"Return a human-readable name string for an DER Type identifier byte.
    
    Unknown type bytes return TYPEn, where n is the decimal type number.
    
    """
    types = {0x01: "BOOLEAN", 
        0x02: "INTEGER", 0x03: "BIT STRING",
        0x04: "OCTET STRING", 0x05: "NULL",
        0x06: "OBJECT IDENTIFIER", 
        0x0c: "UTF8String", 0x0d: "RELATIVE-OID",
        0x13: "PrintableString", 0x14: "T61String", 0x16: "IA5String"}
    return ("TYPE%d" % (typeNo)) if not typeNo in types else types[typeNo]


def readDer(bytes):
    """Dump DER data given as byte array in human-readable form to STDOUT.
    
    Output consist of one line per DER field stating its position, type,
    length and content.
    
    """
    pos = 0
    afterSeq = {}
    while pos < len(bytes):            
        # determine position and length of value
        # treat bytes at pos as (type, len, data ...)
        dataPos = pos + 2            
        dataLen = bytes[pos+1] if pos < len(bytes)-1 else 0
        # if in length=n, bit 0x80 is set, length field takes n-0x80 bytes
        if dataLen > 128: 
            lenlen = dataLen-128
            logging.debug("lenlen=%d, len=%s" % (lenlen, bytes[pos+2:pos+2+lenlen]))
            if 0 < dataLen-128 < 3:
                dataLen = 0
                for i in range(lenlen):
                    dataLen *= 256
                    dataLen += bytes[pos+2+i]
                dataPos += lenlen
        
        print("%d %s(%d)" % (pos, typeName(bytes[pos]), dataLen)),
        
        # output value, depending on type
        if bytes[pos] == 0x30:
            print("BEGIN")
            afterSeq.setdefault(dataPos + dataLen, []).append("SEQUENCE@%d" % (pos))
            pos = dataPos
        elif bytes[pos] == 0x01:
            print("= %r" % (bytes[dataPos] > 0))
            pos = dataPos + dataLen
        elif bytes[pos] == 0x02: 
            print("= %s" % (repr(bytes[dataPos:dataPos+dataLen]))) 
            pos = dataPos + dataLen
        elif bytes[pos] == 0x04:
            print("= \"%s\"" % (byteListPrintables(bytes[dataPos:dataPos+dataLen])))
            pos = dataPos + dataLen
        elif bytes[pos] == 0x05:
            print()
            pos = dataPos
        elif bytes[pos] == 0x06:
            print("= \"%s\"" % ''.join([hex(x)[2:] for x in bytes[dataPos:dataPos+dataLen]]))
            pos = dataPos + dataLen
        else:
            # set/sequence type?
            if bytes[pos] & 32:
                print("FROM HERE")
                afterSeq.setdefault(dataPos + dataLen, []).append("SET@%d" % (pos))
                pos = dataPos
            else:
                print("= \"%s\"" % (byteListPrintables(bytes[dataPos:dataPos+dataLen])))
                pos = dataPos + dataLen

        for message in afterSeq.get(pos, []):
            print("%d END %s" % (pos, message))

