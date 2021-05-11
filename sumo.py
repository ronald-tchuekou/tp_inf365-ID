import os, sys
import traci
import time
import random
import math
from t_state import TrafficState

def getCurrentFileDir ():
    """ Function that return the dir name of the current file. """
    return os.path.dirname(__file__)

def check_sumo_environ():
    """ Function that check if the SUMO_HOME is add to the path. """
    if 'SUMO_HOME' in os.environ:
        tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
        sys.path.append(tools)
        return True
    else:
        sys.exit("Please declare environment variable 'SUMO_HOME'.")
        return False

def getCmdLine():
    """ Function that make the simulation. """
    # Compose the comment line to start either sumo or sumo-gui.
    sumoBinary = "D:/Sumo/bin/sumo-gui"
    # Pour lancer la simulation et commencer la lecture.
    sumoConf = getCurrentFileDir() + "./Sumo/sumo.sumocfg"
    sumoCmd = [sumoBinary, "-c", sumoConf, "-S"]
    return sumoCmd

def setCars(vehID):
    """ Function that set random cars. """
    rand = random.randint(1, 30)
    if rand == 1:
        traci.vehicle.add(vehID="{:00}".format(vehID), routeID='o_e', typeID='car_1', depart=10)
        vehID += 1
    elif rand == 2:
        traci.vehicle.add(vehID="{:00}".format(vehID), routeID='s_n', typeID='car_2', depart=10)
        vehID += 1

    elif rand == 3:
        traci.vehicle.add(vehID="{:00}".format(vehID), routeID='e_o', typeID='car_3', depart=10)
        vehID += 1
    elif rand == 4:
        traci.vehicle.add(vehID="{:00}".format(vehID), routeID='n_s', typeID='car_4', depart=10)
        vehID += 1
    return vehID
def detectCars():
    """ Function that detect cars numbers in edges at one time. """
    west = traci.edge.getLastStepVehicleNumber('edg1')
    suth = traci.edge.getLastStepVehicleNumber('edg6')
    est = traci.edge.getLastStepVehicleNumber('edg4')
    north = traci.edge.getLastStepVehicleNumber('edg7')
    return north, suth, est, west

def changeTrafficLight(state):
    """ Function that change the state of traffic light """
    if state == TrafficState.NORTH_SUTH_GREEN:
         traci.trafficlight.setRedYellowGreenState("node0", "GGGGGrrrrrGGGGGrrrrr")
    elif state == TrafficState.NORTH_SUTH_YELLOW:
        traci.trafficlight.setRedYellowGreenState('node0', 'yyyyyrrrrryyyyyrrrrr')
    elif state == TrafficState.WEST_EST_GREEN:
        traci.trafficlight.setRedYellowGreenState('node0', 'rrrrrGGGGGrrrrrGGGGG')
    else:
        traci.trafficlight.setRedYellowGreenState('node0', 'rrrrryyyyyrrrrryyyyy')

def max (a, b):
    if a >= b:
        return a
    return b

def calTime (max_cars, min_cars):
    if max_cars != 0:
        return (max_cars/2) + 45
    elif max_cars == 0 and min_cars != 0:
        return 0
    elif max_cars == 0 and min_cars == 0:
        return 45

def getOptimisTime (openRoute, north, suth, est, west):
    """ function that return the priority traffic light. """
    max_north_suth = max(north, suth)
    max_west_est = max(west, est)
    if(openRoute == 1):
        return math.floor(calTime(max_west_est, max_north_suth))
    else:
        return math.floor(calTime(max_north_suth, max_west_est))

def simulation():
    """Start the simulation and connect this to sumo with the script above."""
    traci.start(getCmdLine())
    step = 0
    vehID = 0
    openRoute = 1
    stopTime = 5
    while step < 500:
        time.sleep(0.1) # Endormir le programme pendant une seconde.
        traci.simulationStep()  # Lancement de la simulation.

        cars_north, cars_suth, cars_est, cars_west = detectCars()
        print(' CARS ({}) => North: {} ------ Suth: {} ------- Est: {} ------- West: {}'.format(step, cars_north, cars_suth, cars_est, cars_west))

        if stopTime == 0:
            if openRoute == 1:
                changeTrafficLight(TrafficState.WEST_EST_GREEN)
                openRoute = 2
            else:
                openRoute = 1
                changeTrafficLight(TrafficState.NORTH_SUTH_GREEN)
            stopTime = getOptimisTime(openRoute, cars_north, cars_suth, cars_est, cars_west)
            print ('New time = {}, open Route = {}'.format(stopTime, openRoute))
        else:
            if openRoute == 1 and max (cars_est, cars_west):
                changeTrafficLight(TrafficState.WEST_EST_GREEN)
                openRoute = 2
                stopTime = getOptimisTime(openRoute, cars_north, cars_suth, cars_est, cars_west)
                print ('New time = {}, open Route = {}'.format(stopTime, openRoute))
            elif openRoute == 2 and max (cars_north, cars_suth):
                changeTrafficLight(TrafficState.NORTH_SUTH_GREEN)
                openRoute = 1
                stopTime = getOptimisTime(openRoute, cars_north, cars_suth, cars_est, cars_west)
                print ('New time = {}, open Route = {}'.format(stopTime, openRoute))

        vehID = setCars(vehID)
        step += 1
        if stopTime  > 0:
            stopTime -= 1

    # Pour le changement de direction des vehicules.
    # if False:
    #     traci.vehicle.changeTarget(vehID="v1", edgeID="edg1")
    #     traci.vehicle.changeTarget(vehID="v3", edgeID="edg2")
    traci.close()

# Main function.
if __name__ == "__main__":
    if check_sumo_environ():
        simulation()