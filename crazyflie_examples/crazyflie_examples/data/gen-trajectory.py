def header() -> str:
    return "duration,x^0,x^1,x^2,x^3,x^4,x^5,x^6,x^7,y^0,y^1,y^2,y^3,y^4,y^5,y^6,y^7,z^0,z^1,z^2,z^3,z^4,z^5,z^6,z^7,yaw^0,yaw^1,yaw^2,yaw^3,yaw^4,yaw^5,yaw^6,yaw^7"

def fly_to(x: float, y: float, z: float, duration: float):
    data = [0.0] * 33
    data[0] = float(duration)
    data[2] = float(x)
    data[10] = float(y)
    data[18] = float(z)

    return ",".join([str(e) for e in data])

DURATION = 0.5

def print_circle():
    print(fly_to(1, 0, 0, DURATION), ",")
    print(fly_to(0.75, 0.75, 0, DURATION), ",")
    print(fly_to(0, 1, 0, DURATION), ",")
    print(fly_to(-0.75, 0.75, 0, DURATION), ",")
    print(fly_to(-1, 0, 0, DURATION), ",")
    print(fly_to(-0.75, -0.75, 0, DURATION), ",")
    print(fly_to(0, -1, 0, DURATION), ",")
    print(fly_to(0.75, -0.75, 0, DURATION), ",")


print(header() + ",")
print_circle()
print_circle()
print_circle()
print_circle()
print_circle()
