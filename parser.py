import xml.etree.ElementTree as ET
import re
import math
from downloadpano import makepano

file_template = ""

# Open the file in read mode ("r")
with open("template360.html", "r") as file:
    # Read the entire file content into the string variable
    file_template = file.read()

# Parse the XML file
tree = ET.parse("p360tour.xml")
root = tree.getroot()

#print(len(root.findall("scene")))
#exit(0)

# Iterate through the XML elements and extract the tokens
count = 0
for token_element in root.findall("scene"):
    name = token_element.get("name")
    sound = token_element.get("backgroundsound")
    thumburl = token_element.get("thumburl")
    substrings = re.findall(r'/(.*?)/', thumburl)
    panourl = substrings[0]
    print("## scene strings", substrings, panourl)
    hotspots = ""
    #print(len(token_element.findall("hotspot")))
    for token_element2 in token_element.findall("hotspot"):
        if(token_element2.get("ath")!=None):
            count = count + 1
            ath = math.radians(float(token_element2.get("ath")))
            atv = math.radians(float(token_element2.get("atv")))
            #print(ath, atv)
            r = 20
            x = r * math.cos(ath)
            z = r * math.sin(ath)
            y = r * math.sin(atv)
            #print(x,y,z)

            onclick = token_element2.get("onclick")
            hotcounter = 1
            for token_element3 in token_element.findall("action"):
                if(token_element3.get("name")==onclick):
                    pattern = r'mainloadscene\((.*?)\)'
                    matches = re.findall(pattern, token_element3.text)
                    #print(matches)

                    if(len(matches)>0):
                        hotspots = hotspots + "<a-sphere href=\"http://google.com\" id=\"marker" + str(hotcounter) + "\"position=\"" + str(x) + " " + str(y) + " " + str(z) + "\" radius=\"0.65\" color=\"#00ff00\" marker=\"url:"+ matches[0] +".html\"></a-sphere>" 
                        hotcounter = hotcounter + 1

    with open(name + ".html", "w") as file:
       file_content = file_template.replace("__AUDIOURL__",sound)
       file_content = file_content.replace("__ROOMNAME__",name)
       file_content = file_content.replace("__PANORAMAURL__",panourl+".png")
       file_content = file_content.replace("__HOTSPOTS__",hotspots)
        
       file.write(file_content)

    try:
        #makepano(pano, pano_directory)
        makepano(name, panourl)
    except:
        print("Erro ao criar o PANO")


    count = count + 1
    if(count > 3):
       exit(0)
       
print(count)    

# Print the filtered tokens
#for token in filtered_tokens:
#    print(token)
