import requests
from bs4 import BeautifulSoup
import pandas as pd
import json
from tqdm import tqdm
from requests.exceptions import RequestException
import os
import re
import time
import random

""" 
IMPORT MODULES USING CODE
import sys
import subprocess

subprocess.call([sys.executable, '-m', 'pip', 'install', 'html5lib'])
"""

'''
from fp.fp import FreeProxy

proxyPool = cycle(FreeProxy().get())  '''

'''

import socketserver
import threading
import socket 
# Define proxy settings

# Function to create and start the proxy server
def start_proxy_server():
    class ProxyHandler(socketserver.BaseRequestHandler):
        def handle(self):
            data = self.request.recv(1024)
            self.request.sendall(data)  # Simple proxy: forward received data back to the client

    with socketserver.ThreadingTCPServer((proxy_host, proxy_port), ProxyHandler) as httpd:
        print(f"Proxy server is running at http://{proxy_host}:{proxy_port}")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nProxy server stopped.")

# Start the proxy server in a separate thread
proxy_thread = threading.Thread(target=start_proxy_server)
proxy_thread.start() '''

       

# Function to make requests delayed *(using a proxy)*
def make_request(url):
    # to rotate through the list of IPs
    #proxy = next(proxyPool)

    try:
        # random sleep time between 1 and 3 seconds
        time.sleep(3)
                
        
        response = requests.get(url, timeout=5) #, proxies={"http": proxy, "https": proxy}  # Make the request using the proxy
        response.raise_for_status()  # Raise an error for bad responses (status code >= 400)
        return response
    except requests.RequestException as e:
        print(f"Error making request to {url} using proxy: {e}")
        return None

# Set options
pd.set_option('mode.chained_assignment', None)
pd.set_option('display.max_columns', None)

# Read the existing CSV data if not add column names in pandas
gsm = pd.read_csv("gsm.csv") if "gsm.csv" in os.listdir() else pd.DataFrame(columns=["oem","model","network_technology","network_2g_bands","network_gprs","network_edge","launch_announced","launch_status","body_dimensions","body_weight","body_sim","display_type","display_size","display_resolution","display","memory_card_slot","memory_phonebook","memory_call_records","sound_loudspeaker","sound_alert_types","sound_3.5mm_jack","comms_wlan","comms_bluetooth","comms_gps","comms_radio","comms_usb","features_sensors","features_messaging","features_browser","features_clock","features_alarm","features_games","features_java","features","misc_colors","network_3g_bands","network_speed","platform_os","platform_chipset","platform_cpu","platform_gpu","memory_internal","main_camera_single","main_camera_video","misc_price","main_camera_features","body","network_4g_bands","body_build","display_protection","memory","main_camera_dual","selfie_camera_dual","selfie_camera_features","selfie_camera_video","comms_nfc","battery_charging","misc_models","tests_performance","tests_camera","tests_loudspeaker","tests_audio_quality","tests_battery_life","tests_display","selfie_camera_single","comms_infrared_port","network_5g_bands","main_camera_quad","main_camera_triple","sound","misc_sar_eu","main_camera_five","features_languages","body_keyboard","misc_sar","battery","main_camera_dual_or_triple","battery_music_play","selfie_camera_triple","main_camera_v1","selfie_camera","camera","main_camera","network","battery_talk_time","battery_stand.by"])

# Function to build the OEM table
def build_oem_table():
    url = "http://webcache.googleusercontent.com/search?q=cache:https://www.gsmarena.com/makers.php3"
    response = make_request(url)
    makers = BeautifulSoup(response.text, 'html.parser')

    maker_nodes = makers.select(".st-text a")
    
    maker_names = [node.get_text() for node in maker_nodes]
    maker_devices_count = [node.get_text() for node in makers.select(".st-text span")]
    oem_names = [name.replace(count, '').strip() for name, count in zip(maker_names, maker_devices_count)]
    maker_devices_count = [int(count.replace(' devices', '')) for count in maker_devices_count]
    maker_url = [node.get('href') for node in maker_nodes]

    oem_table = pd.DataFrame({
        'maker': oem_names,
        'device_count': maker_devices_count,
        'resource_location': maker_url
    })

    return oem_table

# Function to parse resource locator
def parse_resource_locator(location):
    return "http://webcache.googleusercontent.com/search?q=cache:https://www.gsmarena.com/" + location

# Function to get OEM URLs
def oem_urls(oem_base_url):
    response = make_request(oem_base_url)
    src = BeautifulSoup(response.text, 'html.parser')

    items = src.select(".nav-pages strong , .nav-pages a")
    if items:
        page_range = range(1, int(items[-1].get_text()) + 1)
        maker_id = re.search(r'https://www.gsmarena.com/(.*?)-phones-', oem_base_url).group(1)
        maker_indx = re.search(r'.*-phones-(.*?).php', oem_base_url).group(1)
        return [f"http://webcache.googleusercontent.com/search?q=cache:https://www.gsmarena.com/{maker_id}-phones-f-{maker_indx}-0-p{pg_count}.php" for pg_count in page_range]
    else:
        return [oem_base_url]

# Function to get listed devices on a page
def listed_devices(page_url):
    response = make_request(page_url)
    src = BeautifulSoup(response.text, 'html.parser')
    nodes = src.select("#review-body a")

    devices = [node.get_text() for node in nodes]
    devices_url = [node.get('href') for node in nodes]

    return pd.DataFrame({
        'device_name': devices,
        'device_resource': devices_url
    })

# Function to scrape data from a URL
def scrape_df(url):
    response = make_request(url)
    doc = BeautifulSoup(response.text, 'html.parser')

    n_head = len(doc.select("th"))

    def get_head_tbl(head_indx):
        try:
            return pd.read_html(url, match='.+', header=0, flavor='bs4')[0]
        except Exception as e:
            print(f"Fetching chunk {head_indx} of {n_head}")
            xp = '//th | //*[contains(concat( " ", @class, " " ), concat( " ", "ttl", " " ))]//*[contains(concat( " ", @class, " " ), concat( " ", "nfo", " " ))]'
            return pd.read_html(url, match='.+', header=0, flavor='bs4', attrs={'xpath': xp})[0]

    dfs = [get_head_tbl(i) for i in range(1, n_head + 1)]
    return pd.concat(dfs, ignore_index=True)

# Function to safely scrape data
def safe_scraper(url):
    try:
        return scrape_df(url)
    except RequestException as e:
        print(f"Error scraping {url}: {e}")
        return None

# Function to convert long format to wide format
def long_to_wide(df):
    return pd.DataFrame(df['val'].values.reshape(1, -1), columns=[f"{t}_{s}".strip('_') for t, s in zip(df['type'], df['sub_type'])])

# Function to loop through OEMs and devices
def loop_the_loop():
    if 'oem_table' in locals():
        print("oem table exists")
    else:
        print("building oem table...")
        oem_table = build_oem_table()
        print("oem table built!")

    ll = {'devices': {}}

    for _, row in tqdm(oem_table.iterrows(), total=len(oem_table), desc="Processing OEMs"):
        oem = row['maker']
        print(f"Processing OEM: {oem}")

        oem_listings = oem_urls(parse_resource_locator(row['resource_location']))
        print(f"Pages found: {len(oem_listings)}")

        ll['devices'][oem] = {}

        for page in tqdm(oem_listings, desc="Processing pages", leave=False):
            devices_on_page = listed_devices(page)

            for _, device_row in tqdm(devices_on_page.iterrows(), total=len(devices_on_page), desc="Processing devices", leave=False):
                device = device_row['device_name']

                if device in gsm['model'].values and oem in gsm['oem'].values:
                    print("Device exists. Skipping...")
                else:
                    print(f"Retrieving data for: {device}")
                    gsm_data = safe_scraper(parse_resource_locator(device_row['device_resource']))

                    if gsm_data is not None:
                        gsm_data = pd.concat([pd.DataFrame({'type': ['oem', 'model'], 'sub_type': ['', ''], 'val': [oem, device]}), gsm_data], ignore_index=True)
                        ll['devices'][oem][device] = gsm_data
                        
                        print(ll)
'''
                        with open('gsm.json', 'w') as json_file:
                            json.dump(ll, json_file)
'''
# Execute the main loop
loop_the_loop()

# Read the JSON data and convert to DataFrame
with open('gsm.json', 'r') as json_file:
    new_data_json = json.load(json_file)

gsm_new_devices = pd.concat([long_to_wide(pd.DataFrame.from_dict(new_data_json['devices'][oem][device])) for oem in new_data_json['devices'] for device in new_data_json['devices'][oem]], ignore_index=True)

# Clean column names
gsm_new_devices.columns = gsm_new_devices.columns.str.replace(r'_na|_\.\.\.\.\d+', '', regex=True)
gsm_new_devices.columns = gsm_new_devices.columns.str.replace(r'_\Z', '', regex=True)
gsm_new_devices.columns = gsm_new_devices.columns.str.replace(r' ', '_', regex=True)
gsm_new_devices.columns = gsm_new_devices.columns.str.lower()

# Read the existing CSV data
gsm = pd.read_csv("gsm.csv") if "gsm.csv" in os.listdir() else pd.DataFrame()

# Combine new and existing data and save to CSV
df = pd.concat([gsm_new_devices, gsm], ignore_index=True)
df.to_csv("gsm.csv", index=False)

# Stop the proxy server thread
# proxy_thread.join()