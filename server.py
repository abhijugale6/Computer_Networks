import socket

dns_cache = {}

def resolve_dns(query):

    if query in dns_cache:
        return dns_cache[query]

    dns_server = '8.8.8.8'
    dns_port = 53  

    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        try:
            # Sending DNS query to the specified DNS server
            s.sendto(query, (dns_server, dns_port))

            data, _ = s.recvfrom(1024)

            ip_address, ttl = extract_ip_address(data), extract_ttl(data)

            # Update the cache with the new result and TTL
            dns_cache[query] = {'result': ip_address, 'ttl': ttl}

            return ip_address, ttl
        except Exception as e:
            print(f"Error resolving DNS query: {e}")
            raise

def construct_dns_query(domain, query_type):
    # Construct a simple DNS query
    header = b'\xaa\xbb\x01\x00\x00\x01\x00\x00\x00\x00\x00\x00'
    footer = b'\x00\x01\x00\x01'

    labels = [len(label).to_bytes(1, byteorder='big') + label.encode() for label in domain.split('.')]
    query = b''.join(labels) + b'\x00' + query_type + b'\x00\x01'

    return header + query + footer

def extract_ip_address(response):

    ip_bytes = response[-4:]
    ip_address = '.'.join(str(byte) for byte in ip_bytes)
    return ip_address

def extract_ttl(response):
    # Extract and return the TTL (Time to Live) from the DNS response
    ttl_bytes = response[-12:-8]
    ttl = int.from_bytes(ttl_bytes, byteorder='big')
    return ttl

if __name__ == "__main__":
    # Specify the server address and port
    server_address = ('localhost', 12345)

    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as server_socket:
        # Bind the socket to the specified address and port
        server_socket.bind(server_address)

        print(f"Server listening on {server_address[0]}:{server_address[1]}")

        while True:
            # Receive DNS query from the client
            data, client_address = server_socket.recvfrom(1024)

            # Decode the query and resolve DNS for A record only
            query = data.decode()
            try:
                result_ipv4, ttl = resolve_dns(construct_dns_query(query, b'\x00\x01'))

                print(f"Resolved DNS query from {client_address}: {query} -> IPv4: {result_ipv4}, TTL: {ttl}")
            except Exception as e:
                print(f"Error resolving DNS query: {e}")
                result_ipv4, ttl = "Error: Unable to resolve DNS query", 0

            # Send the result back to the client
            server_socket.sendto(f"IPv4: {result_ipv4}, TTL: {ttl}".encode(), client_address)
