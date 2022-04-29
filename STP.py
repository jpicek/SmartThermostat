# Author: Johnathan Picek
# Term Project - Smart Thermostat Language Prototype
# STP.py
# CPSC 46000-003 - Programming Languages
# Professor Dr. Eric Chou

# Thermostat Class containing all functions
# of the Smart Thermostat operation

from datetime import datetime

class Thermostat():
    def __init__(self):
        self.schedule = {}
        # key : value
        # hour : temp
        for i in range(0,24):
            self.schedule[int(i)] = 70;                 # DEFAULT TEMP FOR ALL HOURS
        self.boundaries = { 0: 7, 1: 9, 2: 17, 3: 23 }  # DEFAULT HOUR FOR EACH PERIOD TRANSITION
        # 0 is time of SLEEP -> WAKE, default 7
        # 1 is time of WAKE -> AWAY, default 9
        # 2 is time of AWAY -> HOME, default 17
        # 3 is time of HOME -> SLEEP, default 23

    def run_set(self, temp, target):
        print("changing", target, "to temp", temp)
        # for target = NOW
        if target == 'NOW':
            now = datetime.now()
            currHour = int(now.strftime("%H"))
            print("current Hour:", currHour)
            # change only actual temp for hour and hour + 1
            # do not change schedule temp
            self.schedule[currHour] = temp
            self.schedule[currHour + 1] = temp
        else:
            # change temp for all hours within target zone
            if target == "SLEEP":
                a = self.boundaries[0]  # lower than a
                b = self.boundaries[3]  # higher than or equal to b
                for i in range(0,24):
                    if i < a or i >= b:
                        self.schedule[i] = temp
            elif target == "WAKE":
                a = self.boundaries[1]  # lower than or equal to a
                b = self.boundaries[0]  # higher than b
                for i in range(b, a):
                        self.schedule[i] = temp
            elif target == "AWAY":
                a = self.boundaries[2]  # lower than or equal to a
                b = self.boundaries[1]  # higher than b
                for i in range(b, a):
                        self.schedule[i] = temp
            elif target == "HOME":
                a = self.boundaries[3]  # lower than or equal to a
                b = self.boundaries[2]  # higher than b
                for i in range(b, a):
                        self.schedule[i] = temp
            elif target == "ALL":
                for i in range(0, 24):
                    self.schedule[i] = temp

    def run_boundary(self, bound, time):
        # if boundary change attempted,
        # verify that the newlimit logically fits in relation to adjacent limits,
        # change the boundary,
        # and re-set scheduled temps for both periods before and after boundary
        newlimit = time
        if bound == 0:                        # between SLEEP and WAKE
            temp = self.schedule[self.boundaries.get(0) - 1]
            postbound = self.boundaries[1]
            if newlimit < postbound:
                self.boundaries[0] = newlimit
                self.run_set(self.schedule[postbound - 1], "WAKE")
                self.run_set(temp, "SLEEP")
            else:
                print("ERROR: equested boundary out of bounds.")
        elif bound == 1:                        # between WAKE and AWAY
            temp = self.schedule[self.boundaries.get(1) - 1]
            prebound = self.boundaries[0]
            postbound = self.boundaries[2]
            if newlimit < postbound and newlimit > prebound:
                self.boundaries[1] = newlimit
                self.run_set(self.schedule[postbound - 1], "AWAY")
                self.run_set(temp, "WAKE")
            else:
                print("ERROR: Requested boundary out of bounds.")
        elif bound == 2:                        # between AWAY and HOME
            temp = self.schedule[self.boundaries.get(2) - 1]
            prebound = self.boundaries[1]
            postbound = self.boundaries[3]
            if newlimit < postbound and newlimit > prebound:
                self.boundaries[2] = newlimit
                self.run_set(self.schedule[postbound - 1], "HOME")
                self.run_set(temp, "AWAY")
            else:
                print("ERROR: Requested boundary out of bounds.")
        elif bound == 3:                        # between HOME and SLEEP
            temp = self.schedule[self.boundaries.get(3) - 1]
            prebound = self.boundaries[2]
            postbound = self.boundaries[0]
            if newlimit > prebound:
                self.boundaries[3] = newlimit
                self.run_set(self.schedule[postbound - 1], "SLEEP")
                self.run_set(temp, "HOME")
            else:
                print("ERROR: Requested boundary out of bounds.")

    def displaySchedule(self):
        # display schedule
        print("Current Schedule Settings:")
        print("SLEEP from ", self.boundaries[3], " to ", self.boundaries[0], sep="")
        bound = 0
        prePended = False
        for k in self.schedule:
            if self.boundaries[3] > k and not prePended:
                # SLEEP period wraps-around overnight, so print stating from boundaries[3] (default 23)
                for i in range(self.boundaries[3], 24):
                    s = "h:" + str(i) + " t:" + str(self.schedule.get(k))
                    print(s.rjust(14))
                    prePended = True
            if k < self.boundaries[3]:
                # print all, except those greater than boundaries[3] which already printed because they came first
                s = "h:" + str(k) + " t:" + str(self.schedule.get(k))
                print(s.rjust(14))
            if k+1 in self.boundaries.values() and bound != 3:
                # when k+1 is a boundary value, print the headers for each period
                bound += 1
                if bound == 1:
                    print("WAKE from ", end="")
                elif bound == 2:
                    print("AWAY from ", end="")
                elif bound == 3:
                    print("HOME from ", end="")
                print(self.boundaries[bound - 1], " to ", self.boundaries[bound], sep="")
        print("\n", end="")

    def displayBoundaries(self):
        # display boundaries
        print("Current Boundary Time Settings:")
        for k,v in self.boundaries.items():
            if k == 0:
                # print SLEEP time period
                print("SLEEP: ", self.boundaries.get(3), " - ", self.boundaries.get(k), sep="")
            else:
                # print other time periods that don't need wrap-around
                if k == 1:
                    print(" WAKE: ", end="")
                elif k == 2:
                    print(" AWAY: ", end="")
                elif k == 3:
                    print(" HOME: ", end="")
                print(k, ": ", self.boundaries.get(k - 1), " - ", self.boundaries.get(k), sep="")
        print("\n", end="")

    def clear(self):
        self.__init__()

if __name__ == "__main__":
    STP = Thermostat()

    STP.displaySchedule()
    STP.displayBoundaries()