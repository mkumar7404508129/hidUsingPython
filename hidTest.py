import hid
import sys
VendorID=0x16c0
ProductID=0x0486

def twos(val_str, bytes):
    
    val = val_str
    b = val.to_bytes(bytes, byteorder=sys.byteorder, signed=False)                                                          
    return int.from_bytes(b, byteorder=sys.byteorder, signed=True)

def extractData(data):

    dataForUse=data[4:]
    sagment=[dataForUse[x:x+20] for x in range(0,len(dataForUse),20)]
    gRos=sagment[0:3]
    aRos=sagment[3:6]
    giros=[]
    acce=[]
    for x in range(0,3):
        if(int(gRos[x][:2])==45):
           giros.append(twos(int("0x"+sagment[x][2:8],16), 3))
        
        elif int(gRos[x][:2])==60 :
            giros.append(int("0x"+sagment[x][2:8],16))

        if(int(aRos[x][:2])==45):
           acce.append(twos(int("0x"+sagment[x][2:8],16), 3))
        
        elif int(aRos[x][:2])==60 :
            acce.append(int("0x"+sagment[x][2:8],16))
    return (giros,acce)   
    
try:
    print("Opening the device")

    h = hid.Device(VendorID,ProductID)
    

    # read back the answer
    print("Read the data")
    while True:
        d = h.read(64)
        if d:
            print("GiRos ",extractData(d.hex())[0])
            print("Acc ",extractData(d.hex())[1])
        else:
            break

    print("Closing the device")
    h.close()

except IOError as ex:
    print(ex)
    print("You probably don't have the hard-coded device.")
    print("Update the h.open() line in this script with the one")
    print("from the enumeration list output above and try again.")

print("Done")