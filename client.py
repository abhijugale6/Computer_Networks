import socket
import tkinter as tk
from tkinter import messagebox

def send_dns_query(query, server_address):
    # Create a UDP socket
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as client_socket:
        try:
            # Send the DNS query to the server
            client_socket.sendto(query.encode(), server_address)

            # Receive and return the response from the server
            data, _ = client_socket.recvfrom(1024)
            return data.decode()
        except Exception as e:
            return f"Error: {e}"

def resolve_domain():
    domain = entry.get()

    if domain.lower() == 'exit':
        root.destroy()
    else:
        result = send_dns_query(domain, server_address)
        if result != "Domain not found":
            messagebox.showinfo("Result", f"Resolved IP Address is {domain}: {result}")
        else:
            messagebox.showwarning("Not Found", "Domain not found")

def close_window():
    root.destroy()

def main():
    global root, entry, server_address
 
    root = tk.Tk()
    root.title("DNS System")

    # Configure styles
    root.configure(bg="#f0f0f0") 

    label = tk.Label(root, text="Enter domain name to lookup (or type 'exit' to quit):", bg="#f0f0f0", fg="black")
    label.pack()

    entry = tk.Entry(root)
    entry.pack()

    resolve_button = tk.Button(root, text="Resolve", command=resolve_domain, bg="#008CBA", fg="white")
    resolve_button.pack()

    exit_button = tk.Button(root, text="Exit", command=close_window, bg="#f44336", fg="white")
    exit_button.pack()

    root.mainloop()

if __name__ == "__main__":
    server_address = ('localhost', 12345)

    main()
