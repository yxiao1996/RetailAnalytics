from ra.Observer import Observer

class NaivePeopleCountObserver(Observer):
    
    def update(self, result):
        # count the number of people in detection result
        peopleCount = 0
        detectDict = result[0]
        #if(not isinstance(result, dict)):


        for label, confidence in detectDict.items():
            if(label == "person"):
                peopleCount += 1
        print("People Count: " + str(peopleCount))