# :pushpin: yongcar
>중고차 시세 예측 서비스  
>http://yongcar.co.kr 

</br>

## 1. 제작 기간 & 참여 인원
- 2021.9.18 ~ 2021.10.12
- 개인 프로젝트

</br>

## 2. 사용 기술
#### `Back-end`
  - Python 3
  - Flask
  - MySQL
  - AWS S3
#### `Front-end`
  - Bootstrap
#### `데이터 수집 및 전처리`
  - Beautifulsoup
  - Selenium
  - Pandas
#### `ML`
  - Sickit-learn
#### `Deploy`
  - AWS lightsail
  - AWS RDS
  - NGINX
  - Gunicorn
</br>

## 3. ERD 설계
![yongcar_erd](https://user-images.githubusercontent.com/48177285/146889299-d5002237-f220-452c-bb2a-97c4c9655844.png)


## 4. 핵심 기능
차종, 연식, 주행거리, 연료 타입, 색상 등의 정보를 입력하면 해당 중고차 매물의 가격을 예측해 줍니다.
</br>
</br>
<img width="589" alt="predict" src="https://user-images.githubusercontent.com/48177285/158297603-a1851963-797a-4f39-bd34-9dce45534a13.PNG">
</br>
</br>
중고차 거래를 위해 매물을 등록 및 탐색할 수 있으며 예측 시세를 토대로 허위매물에 경고 표시를 해줍니다.
</br>
</br>
<img width="568" alt="carlist_alert" src="https://user-images.githubusercontent.com/48177285/158297647-af738eba-ea74-4e19-939c-f6f99e8f3ed7.PNG">
</br>
</br>
질문 글/답글을 통해 유저 간 정보를 공유하는 자유게시판이 있습니다.
</br>
</br>
<img width="597" alt="board" src="https://user-images.githubusercontent.com/48177285/158297693-3372f796-3291-44a2-bf7d-2c26b882cf4d.PNG">


<details>
<summary><b>개발과정 펼치기</b></summary>
<div markdown="1">

### 4.1. 머신러닝 모델 개발
- 동적 크롤링(Selenium)을 이용해 범주별 데이터 수집 및 전처리
  
  ![image](https://user-images.githubusercontent.com/48177285/146894491-cb278e59-15f7-4a48-9228-6f07a3452c5e.png)

- 교차검증을 통한 하이퍼 파라미터 튜닝 및 모델 학습
  ~~~python
  def print_best_params(model, params):
      grid_model = GridSearchCV(model,
                                param_grid=params,
                                scoring='neg_mean_squared_error',
                                cv=5)
      grid_model.fit(X_train, y_train)
      r2 = grid_model.best_score_
      rmse = np.sqrt(-1*grid_model.best_score_)
      print('{0} 5 CV 시 최적 평균 RMSE 값 : {1}, 최적 parameter : {2}'.format(model.__class__.__name__,
                                                                   np.round(rmse, 4),grid_model.best_params_))
  ~~~
  ~~~python
  lgbm_params = {'n_estimators':[100, 300, 500, 1000],
               'learning_rate':[0.1, 0.05, 0.01],
               'max_depth':[3, 4, 5, 6, 7, 8, 9],
               'num_leaves':[6, 12, 24, 36]               
               }

  lgbm_reg = LGBMRegressor(n_estimators='n_estimators',
                           learning_rate='learning_rate',
                           objective='regression',
                           boosting='gbdt',
                           metric= 'rmse',
                           n_jobs=-1)


  ~~~
  ~~~python
  lgbm = LGBMRegressor()
  lgbm.fit(X_train, y_train,
                   eval_set=[(X_test, y_test)],
                   eval_metric='l1',
                   early_stopping_rounds=1000)
  pred = lgbm.predict(X_test)
  evaluate_model(y_test, pred)
  ~~~
  ~~~python
  lgbm = LGBMRegressor(n_estimators=1000,n_jobs=-1,learning_rate=0.05,max_depth=9,num_leaves=24)
  lgbm.fit(X_train, y_train)
  pred = lgbm.predict(X_test)
  evaluate_model(y_test, pred)
  ~~~
  ~~~python
  R2 score : 0.9527
  MAE score : 0.1140
  MSE score : 0.0254
  RMSE score : 0.00064712
  ~~~
 
- 전체과정
  
  https://github.com/joyw93/AI_Project/blob/main/AI_06_%EC%A1%B0%EC%9A%A9%EC%9B%90_section2.ipynb
  
### 4.2. auth
  
- **회원가입/로그인 기능** :pushpin: [코드 확인](https://github.com/joyw93/yongcar/blob/main/yong/views/auth_view.py)
  
  - flask-WTF를 이용하여 백엔드에서도 유효성을 검사 합니다. 
  - 파이썬 bcrypt 라이브러리를 이용해 패스워드를 암호화 합니다.
  
  
### 4.3. car
  
- **시세 조회/매물 등록** :pushpin: [코드 확인](https://github.com/joyw93/yongcar/blob/main/yong/views/car_view.py)
  
  - pickle 형태로 저장된 ML 모델을 불러와 predict method를 구현 했습니다.
  - 매물 등록시 사진은 서버가 아닌 S3 버킷에 저장 되도록 했습니다.
  
  
### 4.4. question
  
- **자유게시판** :pushpin: [코드 확인](https://github.com/joyw93/yongcar/blob/main/yong/views/question_view.py)
  
  - 페이지네이션 기능을 구현 했습니다.
  
  

</div>
</details>

    
</br>

## 5. 회고 / 느낀점


 1. 코드 리팩토링의 필요성과 시점

- 새로운 기능 개발에 몰두하고 있을때면 머릿속으로 구상한 기능이 실제로 동작하는 모습을 빨리 보고싶은 마음에 날림식으로 코드를 작성했습니다.
복잡하면서 가독성이 떨어지는 코드라는것을 스스로 알았지만, 어차피 기능이 잘 돌아가는지가 가장 중요한것이고 필요하다면 추후 한꺼번에 고치면 된다고 생각했습니다.   

- 하지만 시간이 조금만 지나도 코드를 해석하기 힘들었고 또다른 기능 구현에 신경쓰느라 악순환이 반복 되었습니다.
예시로, 게시판의 한 페이지에 표시되는 게시물 수를 조정하기 위해 페이지네이션 코드를 수정할 일이 있었는데 각 변수가 뜻하는 바가 무엇인지 알기가 힘들고 코드의 가독성이 떨어져서
어떤 변수값을 조정해야 하는지 난감한 경우가 있었습니다.   

- 다른 개발자와의 협업과 유지보수의 용이성을 높이기 위해서 코드 리팩토링은 반드시 필요함을 깨달았고 그것을 나중으로 미뤄서는 안되겠다고 생각했습니다.

</br>

2. 불필요하게 중복되는 코드들

- 기존에 만들어놓은 클래스를 잘 활용하면 구현할 수 있는 기능도 당장의 위기를 모면하기 위해 비슷한 형태의 클래스를 만들어 사용했습니다.
당시에는 문제라고 인식을 잘 못했지만 지나고 보니 코드에서 한심함이 느껴졌습니다.

- 코드의 중복을 피하기 위해서 최대한 기능을 분할시켜서 구현하고 오버로딩, 오버라이딩, 상속 등 
클래스에 대한 더 많은 공부와 연습이 필요함을 느꼈습니다.

</br>

3. How 만큼 Why 에도 신경쓰자
    
- 어떤 기능을 구현하기 위해 각종 라이브러리를 불러오거나 AWS같은 서비스를 사용해야 할 일이 많았습니다. 사실 그러한 것들이 어떤 원리로 작동하는지와 코드를 까보면 어떤 형태인지
잘 알지 못하더라도 어떻게 쓰는것인지만 알면 기능 구현에는 큰 어려움이 없었습니다.

- 하지만 완벽하게는 아니더라도 어느정도는 동작 방식을 알아두어야 추후 관련 문제가 발생했을 때 해결에 좀 더
용이할 수 있다고 생각했습니다.

</br>

4. 테스트 코드의 필요성
    
- 어떤 기능을 새롭게 만들었을 때, 그 전까지는 잘 작동하던 기능이 갑자기 고장나 버리는 경우가 있었습니다. 소규모 웹사이트의 경우에는 그런 경우를 운좋게 발견한다 치더라도
대규모 웹사이트에선 그렇지 못할것입니다.

- 이번 프로젝트에서는 메인 기능을 추가할 때 마다 다른 기능들이 정상동작 하는지 일일이 확인 했지만, 다음 프로젝트에서는 기능별 테스트코드를 작성해서
기능 검사에 쓰는 시간을 줄여야겠다고 생각했습니다.
