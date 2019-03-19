from pyknow import *
#<editor-fold desc="MedicalExpertSystems">
class symptoms(Fact):
    list = ["one,two"]
    if Fact in list:
        pass

class Patient(Fact):
    pass
class Disease(Fact):
    pass

class Diagnoses(Fact):
    pass

def Contains(p, fields):
    c = 0
    for i in p:
        if i in fields:
            c += 1
    return c

low_sugar_symptoms = {'shakiness', 'hunger', 'sweating', 'headache', 'pale'}
high_sugar_symptoms = {'thirst', 'blurred vision', 'headache', 'dry mouth', 'smelling breath','shortness of breath'}
measles_symptoms = {'brownish-pink rash', 'high and fast temperature', 'bloodshot eyes', 'white spots'}
cold_symptoms = {'runny nose', 'harsh cough'}
mumps_symptoms = {'moderate temperature', 'saliva is not normal', 'swollen lymph nodes in neck', 'mouth dry'}
flu = {'conjunctives', 'strong body aches', 'weakness', 'vomiting', 'sore throat and sneezing'}


#symptoms=low_sugar_symptoms|cold_symptoms|high_sugar_symptoms|measles_symptoms|mumps_symptoms|flu;
symptoms=set()
class MedicalExpertSystems(KnowledgeEngine):
    @DefFacts()
    def needed_data(self):
        yield Disease(name="Mumps", symptoms=cold_symptoms,age="child")
        yield Disease(name="low sugar",symptoms=low_sugar_symptoms,count=2,age="child")
        yield Disease(name="high sugar", symptoms=high_sugar_symptoms, count=2, age="child")
        yield Disease(name="child flu", symptoms=flu, age="child",disease='cold')
        yield Disease(name="adult flu", symptoms=flu, age="adult",disease='cold')
        yield Disease(name="measles", symptoms=measles_symptoms, age="child",disease='cold')
        yield Disease(name="cold", symptoms=cold_symptoms)
        yield Disease(name="diabetic",disease="low sugar",diabetic_Parents=True)

    @Rule(Disease(name="cold", symptoms=MATCH.symptoms), Patient(symptoms=MATCH.symps))
    def Type0(self, symps, symptoms):
        if (Contains(symps, symptoms) == len(symptoms) and Diagnoses(any)):
            self.declare(Diagnoses("cold"))
        pass


    @Rule(Disease(name=MATCH.name,symptoms=MATCH.symptoms,age=MATCH.age,disease=MATCH.any) ,  Patient(symptoms=MATCH.symps),Patient(age=MATCH.Page))
    def Type1(self,age,Page,symps,symptoms,name,any):
        if(age==Page and Contains(symps,symptoms)==len(symptoms) and Diagnoses(any)):
            self.declare(Diagnoses(name))
        pass
    @Rule(Disease(name=MATCH.name,symptoms=MATCH.symptoms,age=MATCH.age) ,  Patient(symptoms=MATCH.symps),Patient(age=MATCH.Page))
    def Type2(self,age,Page,symps,symptoms,name):
        if(age==Page and Contains(symps,symptoms)==len(symptoms) and Diagnoses(any)):
            self.declare(Diagnoses(name))
        pass
    #high or low suger
    @Rule(Disease(name=MATCH.name,symptoms=MATCH.symptoms,count=MATCH.count,age=MATCH.age),Patient(symptoms=MATCH.symps),Patient(age=MATCH.Page))
    def Type3(self,name,symptoms,count,age,symps,Page):
        if(Contains(symptoms, symps)>count and age==Page):
            self.declare(Diagnoses(name))
        pass

    @Rule(Patient(diabetic_parents=True),Diagnoses("low sugar"))
    def Typed(self):
        self.declare(Diagnoses("diabetic"))
        pass

#</editor-fold>

#<editor-fold desc="PlantExprtSystem">
class temperature (Fact):
    pass


class humidity (Fact):
    pass


class tuber (Fact):
    pass


class Plant(KnowledgeEngine):

    @Rule(temperature("high"), humidity("normal"), tuber("reddish-brown",W(),"spots"))
    def planttype1(self):
        print("the plant has black heart")

    @Rule(temperature("low"), humidity("high"), tuber(W(),"normal","spots"))
    def planttype2(self):
        print("the plant has late blight")

    @Rule(temperature("high"), humidity("normal"), tuber(W(),"dry","circles"))
    def planttype3(self):
        print("the plant has dry rot")

    @Rule(temperature("normal"), humidity("normal"), tuber("brown",W(),"wrinkles"))
    def planttype4(self):
        print("the plant has early blight")


#</editor-fold>

def main():
    print("------------- Pixelz TEAM -------------")
    print("Press 1 To Run Medical Expert Systems: ")
    print("Press 2 To Run Plant Diagnoses Expert System: ")

    x = int(input("Enter Your Choice : "))
    print("-------------------------------------------------")
    if x == 1:
        print("Welcome To Medical Expert Systems")
        print("I Will Ask You Some Question To Specify The Your Disease -- Enjoy :)")
        print("============================================================================")
        engine = MedicalExpertSystems()
        engine.reset()
        engine.declare(Patient(age=int(input("Enter Age:\t"))))
        if (input("Are Your parents diabetic'Y\\N\': ") == "Y"):
            engine.declare(Patient(diabetic_parents=True))
        else:
            engine.declare(Patient(diabetic_parents=False))

        symptoms = set(input("Enter List of symptoms per line Finish with \'$\'\n").split(','))
        while (True):
            x = input()
            if (x == '$'):
                break;
            symptoms.add(x)
        engine.declare(Patient(symptoms=symptoms))
        engine.run()
        # print(engine.facts)

    elif x==2:
        print("Welcome To Diagnoses Expert System")
        print("I Will Ask You Some Question To Specify The Plant Diagnoses -- Enjoy :)")
        print("============================================================================")
        engine = Plant()
        engine.reset()
        engine.declare(
            temperature(input("Enter The Temperature : ")),
            humidity(input("Enter Humidity Type : ")),
            tuber(input("Enter Tuber Color : "), input("Enter Tuber Type : "), input("Enter Tuber Style : "))
        )
        engine.run()
    else:
        print("Sorry, Try again")

main()
