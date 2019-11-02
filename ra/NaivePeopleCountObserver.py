from ra.Observer import Observer

class NaivePeopleCountObserver(Observer):
    
    LABEL = "label"
    PERSON = "person"

    def update(self, subject):
        # count the number of people in detection result
        peopleCount = 0

        for detectedObject in subject.detection:
            if(detectedObject[self.LABEL] == self.PERSON):
                peopleCount += 1
        print("People Count: " + str(peopleCount))