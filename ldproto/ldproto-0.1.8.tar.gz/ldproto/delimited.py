import struct

def write_ld(writer, protomsg):
    """
    Write a length delimited protobuf message to the provided writer
    
    Arguments:
        writer: a writer, e.g. a file opened in 'wb' mode or a BytesIO or StringIO object
        protomsg: a protobuf message
    """
    
    # serialize the message to a bytes array
    s = protomsg.SerializeToString()
    
    # get the length of the message (unsigned 32-bit integer) as a bytes array of size 4
    len_uint64_bytes = struct.pack('>L', len(s))
    
    # return the length + serialized string
    writer.write(len_uint64_bytes + s)


def read_ld(reader, msgtype):
    """
    Reads length-delimited protobuf messages from the provided reader.

    Example:
        with open('users.ld', 'rb') as f:
            for pb_user in read_ld(f, pb.User):
                print(pb_user)
    
    Arguments:
        reader: a reader, e.g. a file opened with 'rb' or a BytesIO or StringIO object
        msgtype: the descriptor of the protobuf message, typically the name of the message,
            e.g. mypb.User
    """
    assert reader is not None, "reader is required"
    assert msgtype is not None, "msgtype is required"

    while True:
        # read 4 bytes from the message
        msg_len_bytes = reader.read(4)
        
        # EOF yields 0 bytes when reading 
        if len(msg_len_bytes) == 0:
            return
        
        # parse the 8 bytes as a 32-bit unsigned long
        msg_len_tuple = struct.unpack('>L', msg_len_bytes)
        
        # struct.unpack always returns a tuple, in this case with one entry - the message length
        msg_len = msg_len_tuple[0]

        # read the message as a byte string
        proto_str = reader.read(msg_len)
        
        # EOF yields 0 bytes when reading 
        if len(msg_len_bytes) == 0:
            return
        
        # de-serialize the bytes string as the msgtype
        msg = msgtype()
        
        # return the protobuf message
        yield msg.ParseFromString(proto_str)