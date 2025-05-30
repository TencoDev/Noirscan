from datetime import datetime
import json


class ScrapedPage:
    def __init__(self, url:str, title:str, text:str, status_code:int, links:list, ip_address:str, geolocation:str):
        self.__url = url
        self.__title = title
        self.__text = text
        self.__status_code = status_code
        self.__links = links
        self.__timestamp = datetime.now()
        self.__ip_address = ip_address or "N/A"
        self.__geolocation = geolocation or "N/A"
    
    def get_url(self):
        return self.__url
    
    def get_title(self):
        return self.__title
    
    def get_text(self):
        return self.__text
    
    def get_status_code(self):
        return self.__status_code
    
    def get_links(self):
        return self.__links
    
    def get_timestamp(self):
        return self.__timestamp
    
    def get_ip_address(self):
        return self.__ip_address
    
    def get_geolocation(self):
        return self.__geolocation
    
    def to_dict(self):
        return {
            'url': self.__url,
            'title': self.__title,
            'text': self.__text,
            'links': self.__links,
            'status_code': self.__status_code,
            'timestamp': self.__timestamp.isoformat(),
            'ip_address': self.__ip_address,
            'geolocation': self.__geolocation
        }
        
    def to_json(self):
        return json.dumps(self.to_dict(), ensure_ascii = False, indent = 2)
    
    def __str__(self):
        return self.to_json()