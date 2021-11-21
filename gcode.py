import time


def writeBoard(ser):
    print("Writing board")
    # home
    gcode("G28", ser)

    # draw first v line
    gcode("G0 Z5", ser)
    gcode("G0 Y5", ser)
    gcode("G0 X25", ser)
    gcode("G0 Z0", ser)
    gcode("G0 Y70", ser)

    # draw second v Line
    gcode("G0 Z5", ser)
    gcode("G0 X50", ser)
    gcode("G0 Z0", ser)
    gcode("G0 Y5", ser)

    # draw first h line
    gcode("G0 Z5", ser)
    gcode("G0 X5 Y25", ser)
    gcode("G0 Z0", ser)
    gcode("G0 X70", ser)

    # draw the second h line
    gcode("G0 Z5", ser)
    gcode("G0 Y50", ser)
    gcode("G0 Z0", ser)
    gcode("G0 X5", ser)

    # go back home
    gcode("G0 Z5", ser)
    gcode("G0 Y0 X0", ser)
    gcode("G0 Z0", ser)
    time.sleep(40)


def gcode(code, ser):
    code = code + '\r\n'
    ser.write(bytes(code, "utf-8"))


def drawSymbol(location, symbol, ser):

    print("location" + str(location))

    locations = {
        1: {"x": 5, "y": 50},
        2: {"x": 30, "y": 50},
        3: {"x": 52, "y": 50},
        4: {"x": 5, "y": 25},
        5: {"x": 27, "y": 25},
        6: {"x": 55, "y": 25},
        7: {"x": 5, "y": 5},
        8: {"x": 30, "y": 0},
        9: {"x": 52, "y": 5}
    }

    def drawX(locationObj):
        gcode(f'G0 X{locationObj["x"]} Y{locationObj["y"]} Z5', ser)
        gcode(f'G0 X{locationObj["x"] + 5} Y{locationObj["y"] + 5} Z0', ser)
        gcode(f'G0 X{locationObj["x"] + 15} Y{locationObj["y"] + 15}', ser)
        gcode("G0 Z5", ser)
        gcode(f'G0 X{locationObj["x"] + 5} Y{locationObj["y"] + 15}', ser)
        gcode("G0 Z0", ser)
        gcode(f'G0 X{locationObj["x"] + 15} Y{locationObj["y"] + 5}', ser)
        gcode("G0 Z5", ser)
        gcode("G0 X0 Y0", ser)
        gcode("G0 Z0", ser)

    locObj = locations[location]
    print(locObj)
    if symbol == "X":
        drawX(locObj)

    time.sleep(15)


obj = {
    1: {"x": 15, "y": 60, "x1": 60, "y1": 60},
    2: {"x": 15, "y": 37, "x1": 60, "y1": 37},
    3: {"x": 15, "y": 15, "x1": 60, "y1": 15},
    4: {"x": 15, "y": 60, "x1": 15, "y1": 15},
    5: {"x": 37, "y": 60, "x1": 37, "y1": 15},
    6: {"x": 60, "y": 60, "x1": 60, "y1": 15},
    8: {"x": 15, "y": 15, "x1": 60, "y1": 60},
    7: {"x": 15, "y": 60, "x1": 60, "y1": 15}
}


def drawWinLine(index, ser):
    moves = obj[index]

    print(moves)

    gcode("G0 Z5", ser)
    gcode(f"G0 X{moves['x']} Y{moves['y']}", ser)
    gcode("G0 Z0", ser)
    gcode(f"G0 X{moves['x1']} Y{moves['y1']}", ser)
    gcode("G0 Z5", ser)
    gcode("G0 X0 Y0", ser)
    gcode("G0 Z0", ser)
    time.sleep(10)
