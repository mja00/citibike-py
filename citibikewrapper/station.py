from . import session


class Station(object):
    def __init__(self, id:int):
        self.id = id
        self.status = self.__get_station_status_json__()
        self.info = self.__get_station_info_json__()
    
    def __get_station_status_json__(self):
        path = 'https://gbfs.citibikenyc.com/gbfs/en/station_status.json'
        response = session.get(path)
        statusJson = response.json()
        for station in statusJson['data']['stations']:
            if station['station_id'] == str(self.id):
                return station
        return {'error': 'Station not found'}

    def __get_station_info_json__(self):
        path = 'https://gbfs.citibikenyc.com/gbfs/en/station_information.json'
        response = session.get(path)
        responseJson = response.json()
        for station in responseJson['data']['stations']:
            if station['station_id'] == str(self.id):
                return station
        return {'error': 'Station not found'} 
    
    def updateData(self):
        self.status = self.__get_station_status_json__()
        self.info = self.__get_station_info_json__()

    @property
    def bikes_available(self):
        self.updateData()
        return self.status['num_bikes_available']

    @property
    def ebikes_available(self):
        self.updateData()
        return self.status['num_ebikes_available']
    
    @property
    def bikes_disabled(self):
        self.updateData()
        return self.status['num_bikes_disabled']

    @property
    def docks_available(self):
        self.updateData()
        return self.status['num_docks_available']

    @property
    def docks_disabled(self):
        self.updateData()
        return self.status['num_docks_disabled']

    @property
    def is_installed(self):
        self.updateData()
        return self.status['is_installed']
    
    @property
    def is_renting(self):
        self.updateData()
        return self.status['is_renting']

    @property
    def is_returning(self):
        self.updateData()
        return self.status['is_returning']
    
    @property
    def name(self):
        self.updateData()
        return self.info['name']
    
    @property
    def short_name(self):
        self.updateData()
        return self.info['short_name']

    @property
    def region_id(self):
        self.updateData()
        return self.info['region_id']

    @property
    def lat(self):
        self.updateData()
        return self.info['lat']

    @property
    def lon(self):
        self.updateData()
        return self.info['lon']
    
    @property
    def rental_methods(self):
        self.updateData()
        return self.info['rental_methods']
    
    @property
    def capacity(self):
        self.updateData()
        return self.info['capacity']

    @property
    def rental_url(self):
        self.updateData()
        return self.info['rental_url']
    
    @property
    def ebike_waiver(self):
        self.updateData()
        return self.info['electric_bike_surcharge_waiver']
    
    @property
    def eightd_dispenser(self):
        self.updateData()
        return self.info['eightd_has_key_dispenser']
    
    @property
    def has_kiosk(self):
        self.updateData()
        return self.info['has_kiosk']
    
    @property
    def at_capacity(self):
        totalBikes = self.bikes_available + self.ebikes_available
        if totalBikes == self.capacity:
            return True
        return False
    
    @property
    def empty(self):
        totalBikes = self.bikes_available + self.ebikes_available
        if totalBikes == 0:
            return True
        return False
    
    @property
    def bikes_rented(self):
        return self.capacity - self.bikes_available

class Network(object):
    def __init__(self):
        self._infoPath = 'https://gbfs.citibikenyc.com/gbfs/en/station_information.json'
        self._statusPath = 'https://gbfs.citibikenyc.com/gbfs/en/station_status.json'
        self.station_list = self.get_all_stations()

    def get_all_stations(self):
        path = 'https://gbfs.citibikenyc.com/gbfs/en/station_information.json'
        response = session.get(path)
        return response.json()['data']['stations']
    
    @property
    def station_count(self):
        response = session.get(self._infoPath)
        return len(response.json()['data']['stations'])
    
    def get_station_by_name(self, name:str):
        stationList = self.station_list
        for station in stationList:
            if name == station['name']:
                return Station(station['station_id'])
        return {'error': f'No station found with the name "{name}"'}
    
    @property
    def total_bikes(self):
        stationList = self.station_list
        totalBikes = 0
        for station in stationList:
            totalBikes += station['capacity']
        return totalBikes
    #Adds an "alias" for total_bikes
    capacity = total_bikes
    
    @property
    def total_bikes_rented(self):
        response = session.get(self._statusPath)
        response2 = session.get(self._infoPath)
        statusJson = response.json()['data']['stations']
        infoJson = response2.json()['data']['stations']
        totalBikes = 0
        for index, station in enumerate(statusJson):
            capacity = infoJson[index]['capacity']
            available = station['num_bikes_available']
            rented = capacity - available
            totalBikes += rented
        return totalBikes
