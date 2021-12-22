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
- 차종, 연식, 주행거리, 연료 타입, 색상 등의 정보를 입력하면 해당 중고차 매물의 가격을 예측해 줍니다.
- 중고차 거래를 위해 매물을 등록 및 탐색할 수 있으며 예측 시세를 토대로 허위매물에 경고 표시를 해줍니다.
- 질문 글/답글을 통해 유저 간 정보를 공유하는 자유게시판이 있습니다.



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

## 5. 트러블 슈팅
### 5.1. 배포 후 DB 조회 오류
- 서버 배포 전 매물 리스트와 게시판 데이터가 문제없이 조회되는 것을 확인 후 배포를 마쳤습니다.

- 첫 웹 애플리케이션 제작의 뿌듯함으로 인해 수시로 사이트를 접속하다가, 우연히 약 12시간 간격으로 DB 조회 시 한차례 에러가 났다가 새로 고침 후
원상복구되는 버그를 발견했습니다.

- 로컬 환경의 MySQL 서버로 재연결하여 테스트시 해당 문제가 발생하지 않았고, AWS RDS 인스턴스의 모니터링 탭을 확인한 결과 에러가 난 시점마다 로그가 찍혀 있었습니다.
그래서 로그 메세지를 토대로 문제를 해결하려 했으나 RDS에 대한 지식 부족으로 인해 근원적인 문제를 해결하지 못했습니다.

- 그러나 다른 방법으로, 매물과 게시판 DB를 조회 할 때 예외처리 구문을 추가하여 에러를 한차례 흘려주도록 하여 문제를 해결했습니다.

- 이론을 공부할 때는 조건문이 있는데 예외처리를 왜 해주어야 하는지 이해하지 못했지만, 해당 트러블슈팅 경험으로 예외처리의 필요성을 느끼게 되었습니다.

- 또한 RDS같은 서비스를 잘 이용하기 위해서는 단순히 사용 방법만 터득하는 것이 아니라 어떤 방식으로 동작하는지에 대한 이해도 중요하다고 생각하게 됐습니다.


    
</br>

## 6. 회고 / 느낀점

* AI 공부를 위해 머신러닝 모델을 만드는 프로젝트를 진행했고, 그것을 활용한 실제 서비스 또한 제작해 보고 싶었습니다.
마침 개발 경험이 부족한 사람도 쉽게 웹어플리케이션을 만들 수 있다는 Flask를 공부할 기회가 있던 덕에 이를 이용해 중고차 거래 플랫폼을 만들어 보기로 결심했습니다.   

* 처음에는 간단한 형태의 게시판부터 시작하여 기능을 하나씩 추가해 나가다 보니 마치 작은 생태계를 창조해 내는 기분이 들었습니다. 원하는대로 기능이 동작하지 않거나 원인불명의 오류가 발생할 때면
너무 답답한 기분이 들었지만 문제가 해결되는 순간마다 즐겁고 오히려 코드는 거짓말을 하지 않는다는 생각이 들어 이번 프로젝트로 인해 백엔드 개발에 대한 흥미를 발견하게 됐습니다.   

* 이번 프로젝트를 통해 스스로 발전 한 부분도 많았지만, 프로젝트를 진행하는 도중과 프로젝트를 완료하고 난 시점에서 주요하게 느꼈던 점들은 다음과 같습니다.   

</br>

 1. 코드 리팩토링의 필요성과 시점

- 한창 새로운 기능 개발에 몰두하고 있을때면 제가 머릿속으로 구상한 기능이 실제로 동작하는 모습을 빨리 보고싶은 마음에 날림식으로 코드를 작성했습니다.
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

4. Test 자동화의 필요성
    
- 어떤 기능을 새롭게 만들었을 때, 그 전까지는 잘 작동하던 기능이 갑자기 고장나 버리는 경우가 있었습니다. 소규모 웹사이트의 경우에는 그런 경우를 운좋게 발견한다 치더라도
대규모 웹사이트에선 그렇지 못할것입니다.

- 이번 프로젝트에서는 메인 기능을 추가할 때 마다 다른 기능들이 정상동작 하는지 일일이 확인 했지만, 다음 프로젝트에서는 기능별 테스트코드를 작성해서
기능 검사에 쓰는 시간을 줄여야겠다고 생각했습니다.
