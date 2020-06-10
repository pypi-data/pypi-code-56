'''
Created on Jun 9, 2020

Using ECS Version 1.5
https://www.elastic.co/guide/en/ecs/current/ecs-client.html

'''
import socket
import json
import datetime
import configparser
from elasticsearch import Elasticsearch
from scapy.all import ARP, Ether, srp
from elasticsearch.helpers.actions import bulk

def genereate_actions(data):
    for item in data:
        yield {
            "_index": "lanclient",
            "_source" : item
        }

def send_to_elastic(clients):
    print('loading ElasticSearch...')
    config = configparser.ConfigParser()
    config.read('config.ini')
    host = [config['DEFAULT']['hosts']]
    verify_cert = True if config['DEFAULT']['verify_certs'] == 'True' else False
    ssl_warn =  True if config['DEFAULT']['ssl_show_warn'] == 'True' else False
        
    es = Elasticsearch(
            host,
            verify_certs=verify_cert,
            ssl_show_warn=ssl_warn
        )  
    
    with open('index.json', 'r') as file:
        mapping = json.load(file)
    
    # ignore 400 already exists code
    es.indices.create(index="lanclient", body=mapping, ignore=400)
      
    bulk(es, genereate_actions(clients))
    print('Bulk Upload to ElasticSearch Complete')
    
def get_domain(clientname):
    # Default Google wifi Primary & Guest unless you switch them
    domain = 'unknown'
    if '192.168.86' in clientname:
        domain = 'primary'
    if '192.168.87' in clientname:
        domain = 'guest'
    return domain

def scan_network(print_results=False, load_to_elastic=True):
    current_time = datetime.datetime.utcnow().isoformat()
    print("Starting at "+ current_time)
    print("scanning....")
        
    clientname = [ip for ip in socket.gethostbyname_ex(socket.gethostname())[2] if not ip.startswith("127.")][0]        
    target_ip = (clientname+"/24")
    domain = get_domain(clientname)
          
    arp = ARP(pdst=target_ip)
    ether = Ether(dst="ff:ff:ff:ff:ff:ff")
    packet = ether/arp
    result = srp(packet, timeout=3, verbose=0)[0]
    
    clients = []
    for sent, received in result:
        client = {'@timestamp': current_time,
                    'client' : {
                    'ip': received.psrc, 
                    'mac': received.hwsrc, 
                    'name': socket.getfqdn(received.psrc),
                    'domain' : domain
                      }
                  }        
        clients.append(client)
    
    if print_results:
        print("IP" + " "*18 +"MAC" + " "*19 + "Host Name")    
        for client in clients:
            print("{:16}    {}     {}".format(client['client']['ip'], client['client']['mac'], client['client']['name']))
    if load_to_elastic:    
        send_to_elastic(clients)
        
    print('Scan Complete')
    
def run_scan():
    scan_network()