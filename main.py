from citibikewrapper import Station, Network

def test_station_info():
    station_instance = Station(304)
    networkInstance = Network()

    print(networkInstance.capacity)

test_station_info()