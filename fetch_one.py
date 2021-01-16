import requests
import re
from bs4 import BeautifulSoup

class FetchOne:
    def __init__(self, url):
        self.name = None
        self.address = ""
        self.city = None
        self.state = None
        self.zip = None
        self.email = None
        self.website = None
        self.bus_env = None
        self.exp_area = None
        self.serv_type = None
        self.medi_care = None
        self.url = "https://findanrd.eatright.org" + url
        response = requests.get(self.url).text
        soup = BeautifulSoup(response, 'lxml')
        self.name = soup.findAll("span", {"class": "active-name"})[0].text
        mydivs = soup.findAll("div", {"class": "user-info-box clearfix"})
        for div in mydivs:
            # print(f"{i}, {div.text}")
            details = div.text.split('\n')
            # print(details)
            if ('Go to map' in details):
                self.get_address_city_state_zip_website(details)
            # print(details)
            elif ('Business Environment' in details):
                self.get_bus_env(details)
            elif ('Expertise Area' in details):
                self.get_exp_area(details)
            elif ('Service Type' in details):
                self.get_serv_type(details)
            elif ('Medicare' in details):
                self.get_medi_care(details)
                
    
    def get_address_city_state_zip_website(self, l):
        temp = []
        for d in l:
            if (d == "" or d == "Go to map" or d == "Get Directions" or d.startswith("Phone")):
                continue
            if (d.startswith('Email')):
                self.email = d[6:]
            elif (d.startswith('Website')):
                self.website = d[8:]
            else:
                temp.append(d)
        # print(temp)
        for i in range(0, len(temp)-1):
            self.address += temp[i] + '\n'
        try:
            self.city = temp[-1].split(',')[0]
            self.state, self.zip = temp[-1].split(',')[1].strip().split(' ')
        except:
            print(f"\t\t\033[33mWarning: CITY/STATE/ZIP not found for {self.name}\033[0m")
        # print(temp[-1].split(' '))
    def get_bus_env(self, l):
        bus_env = ""
        for d in l:
            if (d == "" or d == "Business Environment"):
                continue
            else:
                bus_env += d.strip() + "\n"
        self.bus_env = bus_env
    
    def get_exp_area(self, l):
        exp_area = ""
        for d in l:
            if (d == "" or d == "Expertise Area"):
                continue
            else:
                exp_area += d.strip() + "\n"
        self.exp_area = exp_area

    def get_serv_type(self, l):
        serv_type = ""
        for d in l:
            if (d == "" or d == "Service Type"):
                continue
            else:
                serv_type += d.strip() + "\n"
        self.serv_type = serv_type

    def get_medi_care(self, l):
        medi_care = ""
        for d in l:
            if (d == "" or d == "Medicare"):
                continue
            else:
                medi_care += d.strip() + "\n"
        self.medi_care = medi_care
    def get_data(self):
        data = [self.name, self.address, self.city, self.state, self.zip, self.email, self.website, self.bus_env, self.exp_area, self.serv_type, self.medi_care]
        return data

if __name__ == "__main__":
    fo = FetchOne("/listing/details/8174?page=1")
    print(fo.get_data())
