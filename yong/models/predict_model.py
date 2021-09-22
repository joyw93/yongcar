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
        data['age'] = (pd.to_datetime('now') - pd.to_datetime(data['age'])) / np.timedelta64(1, 'M')
        data['age'] = data['age'].apply(lambda x: int(x))
        price = int(np.expm1(ml_model.predict(data))[0])

        lower_price = int(price * 0.95)
        upper_price = int(price * 1.05)
        result = str('해당 매물의 예상 시세는 {0} ~ {1} 만원 입니다.'.format(lower_price, upper_price))

        return price
