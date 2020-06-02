def scan_good_wifi(sta_if, wifi_configs):
    import ubinascii

    wifi_scan = sta_if.scan()
    wifi_scan =  [[w[0].decode(), ubinascii.hexlify(w[1]).decode(),w[2],w[3],w[4],w[5]] for w in wifi_scan]
    wifi_scan_sorted = sorted(wifi_scan, key=lambda e:e[3], reverse=True)
    good_wifis = [[w[0],wifi_configs[w[0]]] for w in wifi_scan_sorted if (w[0] in list(wifi_configs.keys()))]
    return good_wifis

def do_connect(timeout = 10):
    import json, network, time
    try:
        with open('wifi.secret','r') as f:
            wifi_configs = json.load(f)
    except:
        return

    sta_if = network.WLAN(network.STA_IF)
    sta_if.active(True)
    if not sta_if.isconnected():
        print('connecting to network...')
        good_wifis = scan_good_wifi(sta_if, wifi_configs)
        for good_wifi in good_wifis:
            sta_if.connect(good_wifi[0], good_wifi[1])
            startT = time.time()
            while not sta_if.isconnected():
                time.sleep(0.1)
                if (time.time()-startT)>timeout:
                    break
            if sta_if.isconnected():
                break

    print('network config:', sta_if.ifconfig())
    return sta_if

def disable_wifi(wifi):
    if wifi:
        wifi.disconnect()
        wifi.active(False)
    else:
        print('why u do dis?')
