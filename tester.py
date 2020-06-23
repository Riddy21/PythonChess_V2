class Car(object):
    def __init__(self):
        self.brand = 'ford'
    def __setitem__(self, key, value):
        return setattr(self, key, value)

car = Car()
car['brand'] = 'mazda'
print(car.brand)