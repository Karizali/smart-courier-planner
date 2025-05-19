import psycopg2
import requests
import os
from dotenv import load_dotenv
import math
from google_or_tools import google_OR_tools

load_dotenv()

def get_distance_from_lat_lon_in_km(lat1, lon1, lat2, lon2):
    lat1=float(lat1)
    lon1=float(lon1)
    lat2=float(lat2)
    lon2=float(lon2)
    R = 6371  # Radius of the earth in kilometers
    d_lat = math.radians(lat2 - lat1)
    d_lon = math.radians(lon2 - lon1)
    lat1 = math.radians(lat1)
    lat2 = math.radians(lat2)
    a = (math.sin(d_lat / 2) ** 2
         + math.cos(lat1) * math.cos(lat2)
         * (math.sin(d_lon / 2) ** 2))
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    d = (R * c *1000)/ 1609.344  # Distance in miles
    print(d)
    return d


def find_best_route():
    api_key = os.getenv("API_KEY")
    
    conn= psycopg2.connect(host="localhost", dbname="postgres" ,user="postgres", password="12345", port=5432)
    cur= conn.cursor()
    
    cur.execute("""
        SELECT des_lat,des_lng FROM lat_lng
        """)
    
    distance_from_each_courier = []
    for courier_coordinates in cur.fetchall():
        cur.execute("""
            SELECT des_lat,des_lng FROM lat_lng
            """)
        distance=[]
        for others_courier_coordinates in cur.fetchall():
            d=get_distance_from_lat_lon_in_km(courier_coordinates[0], 
                                            courier_coordinates[1], 
                                            others_courier_coordinates[0], 
                                            others_courier_coordinates[1])
            distance.append(int(d))
        distance_from_each_courier.append(distance)
    print(distance_from_each_courier)
    google_OR_tools(distance_from_each_courier)
        


     




        
        
    conn.commit()
    cur.close()
    conn.close()
# a=[
#    {"de":(0,1),"br":(0,1)},
#    {"de":(2,3),"br":(9,1)},
#    ]
find_best_route()
