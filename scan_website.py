import requests
from bs4 import BeautifulSoup
import socket
import datetime

def scan_web(url):
    try:
        # Mengambil informasi IP
        domain = url.replace("http://", "").replace("https://", "")
        ip_address = socket.gethostbyname(domain)
        print(f"IP: {ip_address}")

        # Mengambil informasi header
        response = requests.get(url)
        headers = response.headers
        print("\nHeader:")
        for key, value in headers.items():
            print(f"{key}: {value}")

        # Mengambil informasi DNS
        print(f"\nDNS: {domain} -> {ip_address}")

        # Mengambil informasi Cloudflare
        if 'cloudflare' in str(headers).lower():
            print("\nCloudflare: Terproteksi")
        else:
            print("\nCloudflare: Tidak terproteksi")

        # Mengambil informasi CMS
        cms_list = ['wordpress', 'joomla', 'drupal', 'magento']
        cms_detected = False
        for cms in cms_list:
            if cms in str(response.text).lower():
                print(f"\nCMS: {cms.capitalize()}")
                cms_detected = True
                break
        if not cms_detected:
            print("\nCMS: Tidak terdeteksi")

        # Mengambil informasi Status Website
        if response.status_code == 200:
            print(f"\nStatus: Online ({response.status_code})")
        elif response.status_code == 404:
            print(f"\nStatus: Not Found ({response.status_code})")
        elif response.status_code == 500:
            print(f"\nStatus: Internal Server Error ({response.status_code})")
        else:
            print(f"\nStatus: {response.status_code}")

        # Mengambil informasi HTML
        soup = BeautifulSoup(response.text, 'html.parser')
        print("\nHTML:")
        print(soup.title.text)

        # Mengambil informasi meta tag
        meta_tags = soup.find_all('meta')
        print("\nMeta Tag:")
        for tag in meta_tags:
            print(f"{tag.get('name')}: {tag.get('content')}")

    except Exception as e:
        print(f"Error: {e}")

url = input("URL: ")
scan_web(url)
