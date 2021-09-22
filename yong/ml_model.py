import pandas as pd
from sklearn.model_selection import train_test_split
import joblib
from lightgbm import LGBMRegressor

url = 'https://blog.kakaocdn.net/dn/bR9gSb/btrfpfQD0U1/KU4xLBx0gcKk4tfOeXKqu1/refrained.csv?attach=1&knm=tfile.csv'
df = pd.read_csv(url, encoding='cp949')
df['model'] = df['model'].astype('category')
df['fuel'] = df['fuel'].astype('category')
df['color'] = df['color'].astype('category')


y = df['price']
X = df.drop('price', axis=1)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=2, stratify=X['model'])

lgbm = LGBMRegressor()
lgbm.fit(X_train, y_train, eval_set=[(X_test, y_test)], eval_metric='l1', early_stopping_rounds=100)

joblib.dump(lgbm, 'model.pkl')