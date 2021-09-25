import pandas as pd
import numpy as np


class Predict:

    @staticmethod
    def price(ml_model, model, age, odo, fuel, color):
        data = pd.DataFrame({'model': [model],
                             'age': [age],
                             'odo': [odo],
                             'fuel': [fuel],
                             'color': [color]})

        data['model'] = data['model'].astype('category')
        data['fuel'] = data['fuel'].astype('category')
        data['color'] = data['color'].astype('category')
        price = int(np.expm1(ml_model.predict(data))[0])

        return price
