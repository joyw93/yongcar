from yong.utils import Utils


class CarPredict:
    def __init__(self, manufact, model, age, odo, fuel, color):
        
        self.manufact = manufact
        self.model = model
        self.age = age
        self.odo = odo
        self.fuel = fuel
        self.color = color
        self.price = Utils.predict_price(model, age, odo, fuel, color)
