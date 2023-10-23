#getiing official station list from nextbike dataset 

import geopy        
import pandas as pd
import csv
from geopy.geocoders import Nominatim
from geopy.distance import geodesic



data_file2022 = "./data_brno/2022/nextbike_dash_2.csv"
data_file2023a = "./data_brno/2023/nextbike_23_08.csv"
data_file2023b = "./data_brno/2023/nextbike_23_09.csv"

nextbike_2022 = pd.read_csv(data_file2022, delimiter =";", decimal='.')

nextbike_2023a = pd.read_csv(data_file2023a, delimiter =",", decimal=',')
nextbike_2023b = pd.read_csv(data_file2023b, delimiter =",", decimal=',')



nextbike_2023 = pd.concat([nextbike_2023a, nextbike_2023b], ignore_index = True)



start22 = (nextbike_2022[["start_place", "start_lat", "start_lng"]])
start22 = (start22.rename(columns={"start_place": "place", "start_lat": "lat", "start_lng": "lng"}))
 
end22 = (nextbike_2022[["end_place", "end_lat", "end_lng"]])
end22 = (end22.rename(columns={"end_place": "place", "end_lat": "lat", "end_lng": "lng"}))



start23 = (nextbike_2023[["start_place", "start_latitude", "start_longitude"]])
start23 = (start23.rename(columns={"start_place": "place", "start_latitude": "lat", "start_longitude": "lng"}))

end23 = (nextbike_2023[["end_place", "end_latitude", "end_longitude"]])
end23 = (end23.rename(columns={"end_place": "place", "end_latitude": "lat", "end_longitude": "lng"}))



all = pd.concat([start22, end22, start23, end23], ignore_index = True)
all["count"] = 1 

all.lat = all.lat.str.replace(',', '.').astype(float)
all.lng = all.lng.str.replace(',', '.').astype(float)


all = all.groupby("place").agg({'count': 'sum', 'lat': 'median',"lng":"median"})

all = all.sort_values(by='count', ascending=False)

all.to_csv("nextbike_stations_from_data.csv")

stations = pd.read_csv("nextbike_stations_from_data.csv")


stations_of = stations[~stations["place"].str.startswith("BIKE")] 
stations_of = stations_of[stations["lat"] > 0]

stations_of.reset_index(inplace = True, drop = True)

stations_of["address"] = ""

geolocator = Nominatim(user_agent="myGeocoder")


for row in range(len(stations_of)): 
    latitude = float(stations_of.loc[row, "lat"])
    longitude = float(stations_of.loc[row, "lng"])
    location = geolocator.reverse(f"{latitude}, {longitude}")
    address = str(location)
    stations_of.loc[row, "address"] = (",".join(address.split(",")[:-4]))
    
    

    
stations_of.to_csv("nextbike_stations_with_adr", index = False)


