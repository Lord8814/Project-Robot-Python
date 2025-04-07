# -*- coding: utf-8 -*-
"""
Created on Fri Mar 21 18:29:09 2025

@author: lione
"""

from dynamixel_sdk import * 
import keyboard 
import time

# -------- Configuration --------
DEVICENAME = 'COM19'    # À adapter : COMx 
BAUDRATE = 1000000
PROTOCOL_VERSION = 1.0

# IDs des servos
DXL_IDS = [1, 2, 3, 4]  #  1,2 MX-64 / 3,4 AX-12A

# Addresses communs
ADDR_TORQUE_ENABLE = 24
ADDR_GOAL_POSITION = 30
ADDR_PRESENT_POSITION = 36
ADDR_MOVING_SPEED = 32
ADDR_CW_ANGLE_LIMIT = 6
ADDR_CCW_ANGLE_LIMIT = 8

TORQUE_ENABLE = 1
TORQUE_DISABLE = 0

# Limites des positions
LIMITS = {
    1: (0, 1901),
    2: (298, 1956),
    3: (510, 961),
    4: (99, 1001),
}

# Vitesse par servo
SPEEDS = {
    1: 100,
    2: 100,
    3: 100,
    4: 100,
}

# -------- Initialisation --------
portHandler = PortHandler(DEVICENAME)
packetHandler = PacketHandler(PROTOCOL_VERSION)

if not portHandler.openPort():
    print("Erreur ouverture port")
    exit()

if not portHandler.setBaudRate(BAUDRATE):
    print("Erreur baudrate")
    exit()

# -------- Configuration des servos --------
for dxl_id in DXL_IDS:
    # Désactiver torque avant config
    packetHandler.write1ByteTxRx(portHandler, dxl_id, ADDR_TORQUE_ENABLE, TORQUE_DISABLE)

    # Régler limites d'angles
    #min_limit, max_limit = LIMITS[dxl_id]
    #packetHandler.write2ByteTxRx(portHandler, dxl_id, ADDR_CW_ANGLE_LIMIT, min_limit)
    #packetHandler.write2ByteTxRx(portHandler, dxl_id, ADDR_CCW_ANGLE_LIMIT, max_limit)
    #print(f"Servo {dxl_id} : Limites fixées [{min_limit}, {max_limit}]")

    # Régler vitesse
    speed = SPEEDS[dxl_id]
    packetHandler.write2ByteTxRx(portHandler, dxl_id, ADDR_MOVING_SPEED, speed)
    print(f"Servo {dxl_id} : Vitesse réglée à {speed}")

    # Activer torque
    packetHandler.write1ByteTxRx(portHandler, dxl_id, ADDR_TORQUE_ENABLE, TORQUE_ENABLE)

# -------- Contrôle : Positionnement --------

# init :
def posinit():
    pos=[1700,1950,512,512]
    packetHandler.write2ByteTxRx(portHandler, 1, ADDR_GOAL_POSITION, 1700)
    packetHandler.write2ByteTxRx(portHandler, 2, ADDR_GOAL_POSITION, 1950)

    packetHandler.write2ByteTxRx(portHandler, 3, ADDR_GOAL_POSITION, 512)
    packetHandler.write2ByteTxRx(portHandler, 4, ADDR_GOAL_POSITION, 512)

#♠posinit()    
def lecturepos():
    l = []
    for dxl_id in DXL_IDS:
        dxl_present_position, dxl_comm_result, dxl_error = packetHandler.read2ByteTxRx(portHandler, dxl_id, ADDR_PRESENT_POSITION)
        if dxl_comm_result != COMM_SUCCESS:
            print(f"Erreur lecture Servo {dxl_id}")
        else:
            print(f"Servo {dxl_id} : Position actuelle = {dxl_present_position}")
            l.append(dxl_present_position)
    return l
    

def pos(a,b,c,d):
    """commande les 4 servos en pos absolue"""
    if LIMITS[1][0]<a<LIMITS[1][1]:
        packetHandler.write2ByteTxRx(portHandler, 1, ADDR_GOAL_POSITION, a)
    else :
        print("hors limite pour l'angle de servo 1")
    if LIMITS[2][0]<b<LIMITS[2][1]:
        packetHandler.write2ByteTxRx(portHandler, 2, ADDR_GOAL_POSITION, b)
    else :
        print("hors limite pour l'angle de servo 2")
    if LIMITS[3][0]<c<LIMITS[3][1]:
        packetHandler.write2ByteTxRx(portHandler, 3, ADDR_GOAL_POSITION, c)
    else :
        print("hors limite pour l'angle de servo 3")
    if LIMITS[4][0]<d<LIMITS[4][1]:
        packetHandler.write2ByteTxRx(portHandler, 4, ADDR_GOAL_POSITION, d)
    else :
        print("hors limite pour l'angle de servo 4")

    time.sleep(0.2)
    lecturepos()
    
def bouge1(a):
    packetHandler.write2ByteTxRx(portHandler, 1, ADDR_GOAL_POSITION, a)
def bouge2(a):
    packetHandler.write2ByteTxRx(portHandler, 2, ADDR_GOAL_POSITION, a)
def bouge3(a):
    packetHandler.write2ByteTxRx(portHandler, 3, ADDR_GOAL_POSITION, a)
def bouge4(a):
    packetHandler.write2ByteTxRx(portHandler, 4, ADDR_GOAL_POSITION, a)
    
def toff():
    """desactive le torque"""
    for dxl_id in DXL_IDS:
        packetHandler.write1ByteTxRx(portHandler, dxl_id, ADDR_TORQUE_ENABLE, TORQUE_DISABLE)
    
def ton():
    """active le torque"""
    for dxl_id in DXL_IDS:
        packetHandler.write1ByteTxRx(portHandler, dxl_id, ADDR_TORQUE_ENABLE, TORQUE_ENABLE)
    
def pos1():
    pos(724,1358,748,500)
    
def coucou():
    pos1()
    time.sleep(1)
    for i in range(3):
        bouge3(700)
        time.sleep(0.3)
        bouge3(748)
        time.sleep(0.3)
        
def seq1():
    time.sleep(5)
    posinit()
    time.sleep(2)
    coucou()
    posinit()

dicoAct = {0:[],
          1:[],
         2:[],
        3:[]  
        }

def savePos():
    toff()
    while True:
        if keyboard.is_pressed("q"):
            break
        time.sleep(0.5)
        act = lecturepos()  
        for i in range(len(act)):
            dicoAct[i].append(act[i])
            
        print(dicoAct)
        
    return dicoAct
        

def go(dicoAct):
        for i in range(len(dicoAct[0])):
            a = dicoAct[0][i]
            b = dicoAct[1][i]
            c = dicoAct[2][i]
            d = dicoAct[3][i]
            pos(a, b, c, d)
            time.sleep(0.001)


    
    


    
"""
try:
    while True:
        print("\nCommande des positions des servos :")
        for dxl_id in DXL_IDS:
            pos = int(input(f"Position pour Servo {dxl_id} (entre {LIMITS[dxl_id][0]} et {LIMITS[dxl_id][1]}): "))
            if pos < LIMITS[dxl_id][0] or pos > LIMITS[dxl_id][1]:
                print(f"Position hors limites pour Servo {dxl_id}")
                continue

            # Envoyer la position
            packetHandler.write2ByteTxRx(portHandler, dxl_id, ADDR_GOAL_POSITION, pos)
            print(f"Servo {dxl_id} déplacé à {pos}")

        # Lecture des positions actuelles
        print("\nLecture des positions actuelles :")
        for dxl_id in DXL_IDS:
            dxl_present_position, dxl_comm_result, dxl_error = packetHandler.read2ByteTxRx(portHandler, dxl_id, ADDR_PRESENT_POSITION)
            if dxl_comm_result != COMM_SUCCESS:
                print(f"Erreur lecture Servo {dxl_id}")
            else:
                print(f"Servo {dxl_id} : Position actuelle = {dxl_present_position}")

except KeyboardInterrupt:
    print("\nArrêt...")
# -------- Désactiver torque --------
for dxl_id in DXL_IDS:
    packetHandler.write1ByteTxRx(portHandler, dxl_id, ADDR_TORQUE_ENABLE, TORQUE_DISABLE)

portHandler.closePort()
print("Fin du programme.")
"""