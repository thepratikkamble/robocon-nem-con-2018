import Credits
def scan_up(thresh):
    for i in range(0, Credits.width):
        z = thresh[Credits.scanUp, i]
        if z == 255:
            break
    for j in range(Credits.width, -1, -1):
        z = thresh[Credits.scanUp, j]
        if z == 255:
            break
    if j == 0:
        return 0
    else:
        return (i+j)/2


def scan_down(thresh):
    for i in range(0, Credits.width):
        z = thresh[Credits.scanDown, i]
        if z == 255:
            break
    for j in range(Credits.width, -1, -1):
        z = thresh[Credits.scanDown, j]
        if z == 255:
            break
    if j == 0:
        return 0
    else:
        return (i+j)/2


def scan_right(thresh):
    for i in range(0, Credits.length):
        z = thresh[i, Credits.scanRight]
        if z == 255:
            break
    for j in range(Credits.length, -1, -1):
        z = thresh[j, Credits.scanRight]
        if z == 255:
            break
    if j == 0:
        return 0
    else:
        return (i+j)/2


def scan_left(thresh):
    for i in range(0, Credits.length):
        z = thresh[i, Credits.scanLeft]
        if z == 255:
            break
    for j in range(Credits.length, -1, -1):
        z = thresh[j, Credits.scanLeft]
        if z == 255:
            break
    if j == 0:
        return 0
    else:
        return (i+j)/2

def plus(thresh):
    if (scan_up(thresh)!=0) and (scan_down(thresh)!=0) and (scan_left(thresh)!=0) and (scan_right(thresh)!=0):
        return 1
    else:
        return 0
