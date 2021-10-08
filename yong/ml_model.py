import pandas as pd
from sklearn.model_selection import train_test_split
import joblib
from lightgbm import LGBMRegressor


url = 'https://yongket.s3.ap-northeast-2.amazonaws.com/csv/used_car.csv'
df = pd.read_csv(url, encoding='cp949')
df['model'] = df['model'].astype('category')
df['fuel'] = df['fuel'].astype('category')
df['color'] = df['color'].astype('category')


y = df['price']
X = df.drop('price', axis=1)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=2, stratify=X['model'])

lgbm = LGBMRegressor(n_estimators=1500,n_jobs=-1,learning_rate=0.05,max_depth=9,num_leaves=24)
lgbm.fit(X_train, y_train, eval_set=[(X_test, y_test)], eval_metric='l1', early_stopping_rounds=500)

joblib.dump(lgbm, 'model.pkl')