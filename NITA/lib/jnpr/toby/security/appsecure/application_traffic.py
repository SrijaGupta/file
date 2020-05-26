#!/usr/bin/python3
"""
Application traffic key words
"""

from jnpr.toby.utils.linux.l4_session import L4_Session
from jnpr.toby.utils.linux.linux_network_config import get_ip_address_type
from jnpr.toby.hldcl.device import Device


def msrpc_traffic(server, client, server_ip, client_ip, close_sess=True):
    """
    Generate MSRPC traffic using two linux instances
    Example :-
        msrpc_traffic(client, server)

    ROBOT Example:
        Msrpc Traffic    ${client_handle}    ${server_handle}

    :param Device server:
        **REQUIRED** Device Handle of the server linux
    :param Device client:
        **REQUIRED** Device Handle of the client linux
    :param str server_ip:
        **REQUIRED** Server IP address
    :param str client_ip:
        **REQUIRED** Client IP address
    :param bool close_sess:
        *OPTIONAL* To close the session or not. if False, the session will not be closed
    """

    server_port = 139
    client_port = 33761
    ipv6 = False
    if get_ip_address_type(client_ip) == "ipv6":
        ipv6 = True

    # The data derived from packet capture
    a1 = "00 00 00 b8 ff 53 4d 42 72 00 00 00 00 18 01 20 00 00 00 00 00 00 00 00 00 00 00 00 " \
         "00 00 2f 6d 00 00 d2 0f 00 95 00 02 50 43 20 4e 45 54 57 4f 52 4b 20 50 52 4f 47 52 " \
         "41 4d 20 31 2e 30 00 02 4d 49 43 52 4f 53 4f 46 54 20 4e 45 54 57 4f 52 4b 53 20 31 " \
         "2e 30 33 00 02 4d 49 43 52 4f 53 4f 46 54 20 4e 45 54 57 4f 52 4b 53 20 33 2e 30 00 " \
         "02 4d 45 54 41 53 50 4c 4f 49 54 00 02 4c 41 4e 4d 41 4e 31 2e 30 00 02 4c 4d 31 2e " \
         "32 58 30 30 32 00 02 44 4f 53 20 4c 41 4e 4d 41 4e 32 2e 31 00 02 4e 54 20 4c 41 4e " \
         "4d 41 4e 20 31 2e 30 00 02 4e 54 20 4c 4d 20 30 2e 31 32 00"

    v1 = "00 00 00 61 ff 53 4d 42 72 00 00 00 00 98 01 20 00 00 00 00 00 00 00 00 00 00 00 00 " \
         "00 00 2f 6d 00 00 d2 0f 11 08 00 03 32 00 01 00 04 11 00 00 00 00 01 00 00 00 00 00 " \
         "fd 43 00 00 da ee 78 ad 4f 0e c5 01 2c 01 08 1c 00 19 52 5f 92 92 78 9e 70 57 00 4f " \
         "00 52 00 4b 00 47 00 52 00 4f 00 55 00 50 00 00 00"

    a2 = "00 00 00 9c ff 53 4d 42 73 00 00 00 00 18 01 20 00 00 00 00 00 00 00 00 00 00 00 00 " \
          "00 00 2f 6d 00 00 d2 0f 0d ff 00 00 00 00 44 a0 f5 00 00 00 00 00 00 18 00 18 00 00 " \
          "00 00 00 00 00 00 00 5f 00 33 fc d8 fa d8 b4 89 06 fb 97 d7 5f 7f 37 7d 18 1e 46 8b " \
          "63 ce 22 5b b9 c8 01 e2 e9 f1 72 28 72 5e 73 54 98 5c 27 ee b0 e7 bb c2 7f f8 39 f7 " \
          "f4 41 64 6d 69 6e 69 73 74 72 61 74 6f 72 00 66 6f 6f 62 61 72 00 55 6e 69 78 00 4d " \
          "65 74 61 73 70 6c 6f 69 74 20 46 72 61 6d 65 77 6f 72 6b 00"

    v2 = "00 00 00 55 ff 53 4d 42 73 00 00 00 00 98 01 20 00 00 00 00 00 00 00 00 00 00 00 00 " \
          "00 00 2f 6d 00 08 d2 0f 03 ff 00 55 00 00 00 2c 00 57 69 6e 64 6f 77 73 20 4e 54 20 " \
          "34 2e 30 00 4e 54 20 4c 41 4e 20 4d 61 6e 61 67 65 72 20 34 2e 30 00 57 4f 52 4b 47 " \
          "52 4f 55 50 00"

    a3 = "00 00 00 44 ff 53 4d 42 75 00 00 00 00 18 01 20 00 00 00 00 00 00 00 00 00 00 00 00 " \
          "00 00 2f 6d 00 08 d2 0f 04 ff 00 00 00 00 00 01 00 19 00 00 5c 5c 31 30 2e 32 2e 31 " \
          "2e 31 36 33 5c 49 50 43 24 00 3f 3f 3f 3f 3f 00"

    v3 = "00 00 00 2e ff 53 4d 42 75 00 00 00 00 98 01 20 00 00 00 00 00 00 00 00 00 00 00 00 " \
          "00 08 2f 6d 00 08 d2 0f 03 ff 00 2e 00 01 00 05 00 49 50 43 00 00"

    a4 = "00 00 00 5b ff 53 4d 42 a2 00 00 00 00 18 01 20 00 00 00 00 00 00 00 00 00 00 00 00 " \
          "00 08 2f 6d 00 08 d2 0f 18 ff 00 00 00 00 07 00 16 00 00 00 00 00 00 00 9f 01 02 00 " \
          "00 00 00 00 00 00 00 00 00 00 00 00 03 00 00 00 01 00 00 00 40 00 00 00 02 00 00 00 " \
          "03 08 00 5c 6c 6c 73 72 70 63 00"

    v4 = "00 00 00 67 ff 53 4d 42 a2 00 00 00 00 98 01 20 00 00 00 00 00 00 00 00 00 00 00 00 " \
          "00 08 2f 6d 00 08 d2 0f 22 ff 00 67 00 00 00 08 01 00 00 00 00 00 00 00 00 00 00 00 " \
          "" \
          "00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 80 00 00 00 " \
          "00 10 00 00 00 00 00 00 00 00 00 00 00 00 00 00 02 00 ff 05 00 00 00"

    a5 = "00 00 00 92 ff 53 4d 42 25 00 00 00 00 18 01 20 00 00 00 00 00 00 00 00 00 00 00 00 " \
          "00 08 2f 6d 00 08 d2 0f 10 00 00 48 00 00 00 ff ff 00 00 00 00 00 00 00 00 00 00 00 " \
          "00 4a 00 48 00 4a 00 02 00 26 00 00 08 4f 00 5c 50 49 50 45 5c 00 05 00 0b 00 10 00 " \
          "00 00 48 00 00 00 01 00 00 00 30 16 30 16 00 00 00 00 01 00 00 00 00 00 01 00 40 fd " \
          "2c 34 6c 3c ce 11 a8 93 08 00 2b 2e 9c 6d 00 00 00 00 04 5d 88 8a eb 1c c9 11 9f e8 " \
          "08 00 2b 10 48 60 02 00 00 00"

    v5 = "00 00 00 7c ff 53 4d 42 25 00 00 00 00 98 01 20 00 00 00 00 00 00 00 00 00 00 00 00 " \
          "00 08 2f 6d 00 08 d2 0f 0a 00 00 44 00 00 00 00 00 38 00 00 00 44 00 38 00 00 00 00 " \
          "00 45 00 48 05 00 0c 03 10 00 00 00 44 00 00 00 01 00 00 00 30 16 30 16 25 33 00 00 " \
          "0d 00 5c 70 69 70 65 5c 6c 6c 73 72 70 63 00 00 01 00 00 00 00 00 00 00 04 5d 88 8a " \
          "eb 1c c9 11 9f e8 08 00 2b 10 48 60 02 00 00 00"

    rep = "41 00 41 00 41 00 41 00 41 00 41 00 41 00 41 00 41 00 41 00 41 00 41 00 41 00 41 00 "
    repeat_value1 = ""
    repeat_value2 = ""
    repeat_value3 = ""
    for i in range (0, 8):
        repeat_value1 += rep
    for i in range (8, 22):
        repeat_value2 += rep
    for i in range (22, 35):
        repeat_value2 += rep
    a61 = "00 00 04 70 ff 53 4d 42 25 00 00 00 00 18 01 20 00 00 00 00 00 00 00 00 00 00 00 00 " \
          "00 08 2f 6d 00 08 d2 0f 10 00 00 26 04 00 00 ff ff 00 00 00 00 00 00 00 00 00 00 00 " \
          "00 4a 00 26 04 4a 00 02 00 26 00 00 08 2d 04 5c 50 49 50 45 5c 00 05 00 00 03 10 00 " \
          "00 00 26 04 00 00 01 00 00 00 0e 04 00 00 00 00 00 00 01 02 00 00 00 00 00 00 01 02 " \
          "00 00 41 00 41 00 41 00 41 00 41 00 41 00 41 00 41 00 41 00 41 00 41 00 41 00 41 00 " \
          + repeat_value1

    a62 = repeat_value2
    a63 = repeat_value3 + "41 00 41 00 41 00 41 00 41 00 41 00 41 00 41 00 41 00 00 00"

    v6 = "00 00 00 23 ff 53 4d 42 25 01 00 6d 00 98 01 20 00 00 00 00 00 00 00 00 00 00 00 00 " \
          "00 08 2f 6d 00 08 d2 0f 00 00 00"


    # Create Server and Client obj
    cli = L4_Session(client)
    svr = L4_Session(server)

    # Start client and server
    svr.start(mode='server', server_ip=server_ip, protocol="tcp", server_port=server_port)
    cli.start(mode='client', server_ip=server_ip, protocol="tcp", server_port=server_port,
              client_ip=client_ip, client_port=client_port)

    cli.send_data(data=a1, ipv6=ipv6, hex_format=True)
    svr.send_data(data=v1, ipv6=ipv6, hex_format=True)
    cli.send_data(data=a2, ipv6=ipv6, hex_format=True)
    svr.send_data(data=v2, ipv6=ipv6, hex_format=True)
    cli.send_data(data=a3, ipv6=ipv6, hex_format=True)
    svr.send_data(data=v3, ipv6=ipv6, hex_format=True)
    cli.send_data(data=a4, ipv6=ipv6, hex_format=True)
    svr.send_data(data=v4, ipv6=ipv6, hex_format=True)
    cli.send_data(data=a5, ipv6=ipv6, hex_format=True)
    svr.send_data(data=v5, ipv6=ipv6, hex_format=True)
    cli.send_data(data=a61, ipv6=ipv6, hex_format=True)
    cli.send_data(data=a62, ipv6=ipv6, hex_format=True)
    cli.send_data(data=a63, ipv6=ipv6, hex_format=True)
    svr.send_data(data=v6, ipv6=ipv6, hex_format=True)

    # Close connection
    if close_sess is True:
        cli.close()
        svr.close()
