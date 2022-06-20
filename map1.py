import folium
import pandas

map = folium.Map(location=[38.58,-99.09], zoom_start=6, titles = "Mapbox Bright")

#1）add a marker to your map
fg = folium.FeatureGroup(name="My Map")
#add markers
fg.add_child(folium.Marker(location=[38.2,-79.1],popup="Hi, I am a Marker", icon=folium.Icon(color='green')))#在地图上加marker,点击marker，可以看到信息
fg.add_child(folium.Marker(location=[38.2,-99.1],popup="Hi, I am a Marker", icon=folium.Icon(color='green')))#在地图上加marker,点击marker，可以看到信息

#2）for loop add markers by location
for coordinates in [[38.2,-99.1],[39.2,-97.1]]:
    fg.add_child(folium.Marker(location= coordinates,popup="Hi, I am a Marker", icon=folium.Icon(color='green')))#在地图上加marker,点击marker，可以看到信息
#真实生活中不可以一个一个的输入location，此时location存放在文件中

#3）add markers from files
data = pandas.read_csv("Volcanoes.txt")
lat = list(data["LAT"])
lon = list(data["LON"])

#for lt, ln in zip(lat, lon): #for i, j in zip([1,2,3],[4,5,6]) print(i, "and", j)
#    fg.add_child(folium.Marker(location=[lt,ln],popup="Hi, I am a Marker", icon=folium.Icon(color='green')))#在地图上加marker,点击marker，可以看到信息

#4)add text on the map popup window
elev = list(data["ELEV"]) #,海拔，the popup window of the markers name

#5）color generation fuction
def color_productor(el):  #根据不同的高度来决定颜色
    if el < 1000:
        return 'green'
    elif 1000<= el <3000 :
        return 'orange'
    else:
        return 'red'
    
fgv = folium.FeatureGroup(name="Volcanoes")

for lt, ln, el in zip(lat, lon, elev): #for i, j in zip([1,2,3],[4,5,6]) print(i, "and", j)
    fgv.add_child(folium.CircleMarker(location=[lt,ln],popup=str(el)+"m", fill_color=color_productor(el), color = 'grey', fill_opacity = 0.7))#在地图上加marker,点击marker，可以看到信息

#6) JSON data add population map layer from the data
#7) stylizing the population layer 给人口层加颜色 要记住使用一行式！！
fgp = folium.FeatureGroup(name="Population")

fgp.add_child(folium.GeoJson(data=open('world.json','r',encoding='utf-8-sig').read(), 
                            style_function=lambda x: {'fillColor':'green' if x['properties']['POP2005'] < 10000000 
                            else 'orange' if 10000000 <= x['properties']['POP2005']<20000000 else 'red'}))
#l = lambda x: x**2
#l(5) == 25

#8）add a layer Control Panel
#增添一个layer control选项'
#因为layer control panel是对应多个层，因此fgv与fgp添加后会多出两层,并且这两层要单独定义
map.add_child(fg)
map.add_child(fgp)
map.add_child(fgv)


map.add_child(folium.LayerControl())

map.add_child(fg)
map.save("Map.html")
