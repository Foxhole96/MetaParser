import csv
import socket
import whois

def get_whois_info(domain):
    try:
        whois_info = whois.whois(domain)
        return whois_info
    except socket.gaierror:
        return "Error: Could not retrieve whois information for the domain."

def main():
    domains = []
    with open('domains.csv', 'r') as f:
        reader = csv.reader(f)
        for line in reader:
            domains.append(line[0])

    with open('whois_output.csv', 'w') as f:
        writer = csv.writer(f)
        writer.writerow(["Domain", "Whois Information"])
        for domain in domains:
            whois_info = get_whois_info(domain)
            writer.writerow([domain, whois_info])

if __name__ == '__main__':
    main()