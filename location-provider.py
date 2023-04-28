from flask import Flask
#from signal import pause

app = Flask(__name__)


@app.route("/", methods=['GET', 'POST'])
def hello_world():
    f = open("location.txt", "r")
    location = f.read()
    f.close
    bits = location.split(",")
    
    # latitude first
    temp = bits[0].lstrip("0")
    numbers = float(bits[0])/100
    strnumbers = str(numbers)
    temp = strnumbers.split(".")
    value1 = int(temp[0])
    temp = numbers - value1
    lat = int(value1) + (temp*100)/60
    if (bits[1] == "S"):
        lat = lat * -1
        
    # longitude first
    temp = bits[0].lstrip("0")
    numbers = float(bits[2])/100
    strnumbers = str(numbers)
    temp = strnumbers.split(".")
    value1 = int(temp[0])
    temp = numbers - value1
    lng = int(value1) + (temp*100)/60
    if (bits[3] == "W"):
        lng = lng * -1
    
    return("{\"location\": {\"lat\": "+str(lat) +", \"lng\": "+str(lng)+"}, \"accuracy\": "+bits[5]+"}")
    #return(f.read());
    #return"{\"location\": {\"lat\": -33.7, \"lng\": 18.4}, \"accuracy\": 25000}"

#pause()
if __name__ == "__main__":
    app.run(debug=True)