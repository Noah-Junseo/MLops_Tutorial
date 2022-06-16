# mlflow

주차: 6

# 1. MLFlow 개요

![Untitled](images/Untitled.png)

<br/>

## A. 사용하는 이유

머신러닝 모델을 개발하기 위해선 여러 방면으로의 실험이 필요하다. 왜냐하면 딥러닝에서는 좋은 결과를 내는 원인을 제대로 알기 어렵기 때문이다. 따라서 모델을 변화 시킬 필요가 있고 하이퍼 파라미터를 변화하며 실험할 필요가 있다.

MLFlow에서 지원하는 기능은 다양하지만 MLFlow를 사용하는 일반적인 이유는 다양한 실험의 과정들을 잘 기록해두기 위함이다.

모델을 학습 시킬 때 “이 Metric(Accuracy, Loss)를 기록할거다.” 혹은 “이 Parameter(batch_size, Epoch)를 기록할거다.” 라는 정의를 해야한다. 따라서 모델을 개발하는 데이터 과학자가 이 툴을 주로 사용하게 된다. 

*MLOps의 관심이 빠르게 증가하고 있는데 이는 곧 데이터 관계자들 사이에 의사소통의 필요성을 이야기한다. 단순히 모델을 개발할 수 있는 데이터 과학자가 아니라 자신의 실험을 관리할 줄 아는 능력이 큰 장점이 될거라고 생각한다.*

**MLFlow의 기능**

- 실험 생성
- 모델 및 지표 로깅
- 모델 지표 비교
- 모델 레지스트리
- 로컬 배포

<br/>

### 1. 실험 생성

MLFlow의 실험을 통해 모델 및 관련 지표를 그룹화 할 수 있다. MNIST 분류를 위한 학습과 Fashion MNIST 분류를 위한 학습이 한 곳에서 관리된다면 시각적인 어려움이 많을 것인데 이를 실험 단위로 관리할 수 있게 해준다.

<br/>

### 2. 모델 및 지표 로깅

MLFlow를 사용하면 모델을 모듈화된 형태로 저장하고 모델 실행과 관련된 모든 지표를 기록할 수 있다. 아직까지도 구글 스프레드 시트에 모델을 학습을 기록하는 경우가 많은데 MLFlow를 통해 휴먼에러르 최소화 할 수 있다.

<br/>

### 3. 모델 지표 비교

MLFlow를 사용하면 2번에서 저장한 로깅을 기반으로 어떠한 하이퍼 파라미터를 사용했을 때 최고의 성능을 내는 지 등 지표를 손쉽게 비교할 수 있다.

<br/>

### 4. 모델 레지스트리

비교적 최근에 추가된 기능이다. 모델의 lineage를 관리할 수 있다고 공식 Docs에 기록되어 있는데 이는 모델을 버저닝하고 Production 혹은 Staging 단계에 있는 모델을 구분해 관리할 수 있는 기능을 이야기한다.

<br/>

### 5. 로컬 배포

MLFlow를 사용하면 로컬 서버에 배포해 모델 추론을 테스트할 수도 있다. 로컬 뿐만 아니라 클라우드 서비스에도 손쉽게 배포할 수 있는 기능을 제공한다.

<br/>

## B. 설치

먼저 VM에서 실행해볼것이다. 지난주의 BentoML을 VM의 Virtualenv에서 실행했었다. 기존의 VM에서 새로운 Virtualenv를 만들고 MLFlow를 설치해보자.

### 1. 가상환경 만들기

VM에 Virtualenv를 설치하는 방법은 [지난주 자료](https://github.com/Ssuwani/mlops-tutorial/tree/main/5-serving-design-pattern#0-virtualenv-%ED%99%98%EA%B2%BD%EC%84%A4%EC%A0%95)를 참고하면 된다.

```bash
virtualenv -p python3 mlflow-env # 가상환경 만들기 -> mlflow-env라는 폴더가 생성됨
source mlflow-env/bin/activate # 가상환경에 접속
```

![Untitled](images/Untitled1.png)

<br/>

### 2. MLFlow 설치

설치는 너무 간단하다.

```bash
pip install mlflow -q # quiet
```

![Untitled](images/Untitled2.png)

<br/>

### 3. 설치확인

MLFlow를 pip로 설치하면 CLI 명령어 또한 사용이 가능하다. 명령어로 설치된 버전을 체크해보자.

```bash
mlflow --version
```

![Untitled](images/Untitled3.png)

<br/>

### 4. 대시보드 확인

MLFlow의 큰 장점 중 하나는 대시보드를 제공한다는 것이다. 확인해보자

```bash
mlflow ui --host=0.0.0.0 --port=3389
```

VM에서 외부 IP로 접근하기 위해 `0.0.0.0` 이라는 host를 지정해준 것이고 VM에서 기본적으로 rdp 통신을 위해 3389 포트를 개방해두었는데 rdp를 우리가 사용하지 않기 때문에 mlflow ui 접근을 위해 지정했다.

![Untitled](images/Untitled4.png)

이제 EXTERNAL_IP:3389 로 접근해서 대시보드를 확인해보자. 

![스크린샷 2022-05-08 21.34.58.png](images/img1.png)

나의 경우 외부IP가 34.125.193.50 이기 때문에 [http://34.125.193.50:3389/](http://34.125.193.50:3389/) 로 접근했다.

![Untitled](images/Untitled5.png)

위와 같은 대시보드를 확인할 수 있다면 설치가 성공한 것이다.

<br/>

<br/>

# 2. MLFlow Tutorial

## A. 실험 생성

이는 단순히 학습들을 관리할 수 있는 그룹을 생성하는 것을 이야기한다. 생성하는 방법은 2가지 방법이 있다. 

1. MLFlow 대시보드에서 생성하기
2. MLFlow CLI를 통해 생성하기
3. MLFlow 파이썬 메소드로 생성하기

<br/>

### 1. MLFlow 대시보드에서 실험 생성

위에서 확인한 대시보드의 Experiments 옆의 더하기 버튼을 클릭하면 된다. 

![스크린샷 2022-05-08 21.40.08.png](images/img2.png)

그러면 아래와 같은 창이 뜨는데 mnist라고 입력해주었다.

![Untitled](images/Untitled6.png)

그리고 대시보드 화면을 통해 추가적으로 알 수 있는 것은 기본적으로 Default라는 Experiment가 생성되어 있음을 알 수 있다. 그리고 Experiment ID가 0 번으로 지정되어 있다.

생성된 mnist Experiment과 Experiment ID 1번을 확인하자

![Untitled](images/Untitled7.png)

<br/>

### 2. MLFlow CLI를 통해 실험 생성하기

커맨트 라인 명령어로도 실험을 생성할 수 있다. VM에서 커맨드 입력을 위해 하나 더 SSH 연결을 했다. (대시보드를 실행했던 mlflow ui 는 쉘을 리턴하지 않았기 때문이다.)

```bash
# source mlflow-env/bin/activate -> 가상환경 활성화
mlflow experiments create --experiment-name fashion-mnist
# mlflow experiments list # 실험 리스트 출력
```

아래의 사진에선 가상환경을 활성화하고 실험을 생성한 뒤 실험을 리스트까지 확인해보았다.

![Untitled](images/Untitled8.png)

<br/>

### 3. MLFlow 파이썬 메소드로 생성하기

MLFlow 라이브러리의 메소드를 활용해서도 실험을 생성할 수 있다. cifar라는 실험을 생성해보자.

```bash
import mlflow

mlflow.create_experiment("cifar") # Experiment ID를 반환함.
```

![Untitled](images/Untitled9.png)

<br/>

## B. 모델 지표 및 로깅

이제 실험을 만들었으니 MLFlow의 핵심이라 할 수 있는 Tracking을 사용해보자. 

세가지 메소드를 이용해 Tracking을 수행할 수 있다.

- log_param()
- log_metric()
- log_artifacts()

mlflow-src이라는 폴더를 만들고 시작하자.

```bash
mkdir mlflow-src
cd mlflow-src
```

<br/>

### 1. 간단한 예시

mlflow-src라는 폴더를 만들고 작업 디렉토리를 변경했는데 하나의 폴더를 더 만들고자 한다. basic이라는 폴더를 만들고 그안에 main.py 파일을 생성하자.

```bash
mlflow-src
└── basic
    └── main.py
```

`mlflow-src/basic/main.py`

```python
# main.py

import os
import mlflow

############################
uri = "file:///home/jsuwan961205_9/mlruns"
mlflow.set_tracking_uri(uri)
############################

mlflow.log_param("batch_size", 128)
mlflow.log_param("epochs", 10)

mlflow.log_metric("accuracy", 60)
mlflow.log_metric("loss", 0.5)

if not os.path.exists("outputs"):
    os.makedirs("outputs")
with open("outputs/test.txt", "w") as f:
    f.write("hello world!")
mlflow.log_artifacts("outputs")
```

파일을 실행시키기 전에 짚고 넘어가야 하는 것이 두가지 있다.

**첫번째! set_tracking_uri()**

`mlflow.set_tracking_uri()` 인데 mlflow는 실험을 관리를 위한 다양란 로그 및 아티팩트들을 저장하기 위해 mlruns 라는 폴더가 자동으로 생성된다. 기존에 HOME 디렉토리에서 `mlflow ui` 를 실행했을 때 mlruns 라는 폴더가 생성됐었고 그 안에 0번 폴더가 위치했었다. 0번은 Default 실험의 Experiment ID를 의미한다.

또한 대시보드에서 mnist Experiment를 생성했을 때 mlruns 폴더에 1 이라는 폴더가 생성됐었다. 이 또한 mnist라는 Experiment의 Experiment ID가 1번이기 때문이였다. 

fashion-mnist, cifar 라는 실험도 생성했으므로 mlruns 폴더 구성은 아래와 같다. *추가적으로 `meta.yaml` 파일은 실험의 메타 정보들을 담고있다.*

```bash
/home/jsuwan961205_9/mlruns/ # HOME 디렉토리의 mlruns 폴더를 의미한다.
├── 0
│   └── meta.yaml
├── 1
│   └── meta.yaml
├── 2
│   └── meta.yaml
└── 3
    └── meta.yaml
```

하지만 여기서 주의해야 할 점은 기본적으로 tracking을 위한 mlruns 폴더는 실행위치의 `./mlruns` 라는 상대경로에 자동으로 생성된다는 것이다. 그렇기 때문에 `mlflow.set_tracking_url()` 메소드를 통해 HOME 디렉토리의 mlruns 폴더 위치를 지정해주었다.

**두번쨰! meta.yaml**

meta.yaml 파일을 열어보면 다음과 같다.

```bash
# /home/jsuwan961205_9/mlruns/0/meta.yaml
artifact_location: ./mlruns/0
experiment_id: '0'
lifecycle_stage: active
name: Default
```

여기서 주의깊게 봐야할 점은 `artifact_location` 이다. 우리는 log_artifacts()라는 메소드를 사용해 artifact들을 저장할 것인데 artifact_location이 상대경로로 되어 있어서 파일을 실행하는 곳을 기준으로 mlruns 폴더를 생성해 artifact들을 위치시키게 된다. 궁금하면 아래의 수정을 하지 않고 파일을 실행해보면 이해할 수 있을 것이다.

우리는 결과물인 아티팩트들 또한 중앙에서 관리하고자 한다. 따라서 `meta.yaml` 파일을 간단히 수정하였다.

```bash
artifact_location: /home/jsuwan961205_9/mlruns/0 # 수정완료
experiment_id: '0'
lifecycle_stage: active
name: Default
```

이제 실행해보자!!

```bash
python main.py
```

잘 실행되었다면 HOME 디렉토리의 mlruns 폴더에서도 0번 폴더안에 정보가 기록되어 있을 것이다. 왜냐하면 기본적으로 Default 실험에서 수행되기 때문이다. 폴더 구성을 통해 확인해보자.

main.py 파일이 위치한 곳의 파일 구성은 다음과 같다. outputs 폴더를 코드에서 생성했었고 그 안에 test.txt 파일을 만들었었다. 그리고 이를 artifact로 저장하였다.

```bash
.
├── main.py
└── outputs
    └── test.txt
```

그리고 대망의 mlruns 폴더의 구성이다. 

```bash
mlruns
├── 0
│   ├── e36548a4f8fb4ba091ffdc558460af4d
│   │   ├── artifacts
│   │   │   └── test.txt
│   │   ├── meta.yaml
│   │   ├── metrics
│   │   │   ├── accuracy
│   │   │   └── loss
│   │   ├── params
│   │   │   ├── batch_size
│   │   │   └── epochs
│   │   └── tags
│   │       ├── mlflow.source.name
│   │       ├── mlflow.source.type
│   │       └── mlflow.user
│   └── meta.yaml
├── 1
│   └── meta.yaml
├── 2
│   └── meta.yaml
└── 3
    └── meta.yaml
```

<br/>

### 2. MNIST 학습 기록하기

이제 우리가 잘하는 MNIST 학습을 하고 그 과정을 기록해볼 것이다.

위에서 봤다시피 `log_param`, `log_metric`, `log_artifacts` 를 사용해 학습을 추적해보자.

기록할 내용은 다음과 같다.

parameter

- batch_size
- epochs

metric

- loss
- acc

artifacts

- model

기존의 mlflow-src 폴더에 mnist라는 폴더를 만들고 main.py 파일을 만들것이다. 여기서 신경써야 하는 것은 `mlflow.set_experiment()` 라는 메소드이다. Experiment를 지정해줘서 실행에 대한 그룹을 적용하는 것이다. 기존에 만들었던 mnist라는 실험을 사용하고자 한다.

텐서플로우 설치는 `pip install tensorflow`

`mlflow-src/mnist/main.py`

```bash
import tensorflow as tf
import argparse
import mlflow

############################
uri = "file:///home/jsuwan961205_9/mlruns"
mlflow.set_tracking_uri(uri)
experiment_name = "mnist"
mlflow.set_experiment(experiment_name)
############################

parser = argparse.ArgumentParser()
parser.add_argument(
    "--batch_size",
    type=int,
    default=512,
    help="input datasets batch size"
)
parser.add_argument(
    "--epochs",
    type=int,
    default=5,
    help="input epochs"
)

args = parser.parse_args()
mlflow.log_param("batch_size", args.batch_size)
mlflow.log_param("epochs", args.epochs)
mnist = tf.keras.datasets.mnist

(x_train, y_train), (x_test, y_test) = mnist.load_data()
x_train, x_test = x_train / 255.0, x_test / 255.0

model = tf.keras.models.Sequential([
  tf.keras.layers.Flatten(input_shape=(28, 28)),
  tf.keras.layers.Dense(256, activation='relu'),
  tf.keras.layers.Dropout(0.2),
  tf.keras.layers.Dense(10, activation='softmax')
])

model.compile(optimizer='adam',
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])

model.fit(
  x_train,
  y_train,
  batch_size=args.batch_size,
  epochs=args.epochs
)

loss, acc = model.evaluate(x_test,  y_test, verbose=2)
print(f"model loss: {loss:.4f} acc: {acc:.4f}")
mlflow.log_metric("loss", loss)
mlflow.log_metric("acc", acc)
model.save("saved_model")
mlflow.log_artifacts("saved_model")
```

실행은 다음과 같이 할 수 있다.

하지만 실행하기전에 기존에 했던 것과 같이 meta.yaml 파일을 수정해줘야 한다.

```bash
python main.py --batch_size 512 --epochs 2
```

![Untitled](images/Untitled10.png)

이번에도 mlruns 폴더 구성을 살펴보자. 1번 폴더안에 하나의 폴더가 생성되었고 saved_model도 artifacts 폴더안에 잘 저장되어 있는 것을 확인할 수 있다.

```bash
/home/jsuwan961205_9/mlruns/
├── 0
│   ├── 1685cf0a5b4643a39d9dd959039a0da1
│   │   ├── artifacts
│   │   │   └── test.txt
│   │   ├── meta.yaml
│   │   ├── metrics
│   │   │   ├── accuracy
│   │   │   └── loss
│   │   ├── params
│   │   │   ├── batch_size
│   │   │   └── epochs
│   │   └── tags
│   │       ├── mlflow.source.name
│   │       ├── mlflow.source.type
│   │       └── mlflow.user
│   └── meta.yaml
├── 1
│   ├── d5ba83a055bc4405bf77025ccf68c125
│   │   ├── artifacts
│   │   │   ├── assets
│   │   │   ├── keras_metadata.pb
│   │   │   ├── saved_model.pb
│   │   │   └── variables
│   │   │       ├── variables.data-00000-of-00001
│   │   │       └── variables.index
│   │   ├── meta.yaml
│   │   ├── metrics
│   │   │   ├── acc
│   │   │   └── loss
│   │   ├── params
│   │   │   ├── batch_size
│   │   │   └── epochs
│   │   └── tags
│   │       ├── mlflow.source.name
│   │       ├── mlflow.source.type
│   │       └── mlflow.user
│   └── meta.yaml
├── 2
│   └── meta.yaml
└── 3
    └── meta.yaml
```

이제 드디어 모델 지표 비교에 들어가기 위해 곧장 하나의 실행을 더 해보자.

```bash
python main.py --batch_size 32 --epochs=1
```

정상적으로 학습이 될 것이고 mlruns/1 에 하나의 폴더가 추가적으로 생성됐을 것이다.

<br/>

## C. 모델 지표 비교

방금전에 실험 mnist에 두번의 모델 학습을 수행했다. 이 학습을 비교해보기 위해 대시보드를 확인해보자.

혹시 대시보드가 실행되어 있지 않다면 mlruns 폴더가 위치하는 홈 디렉토리에서 아래 명령어를 통해 실행시키면 된다.

```bash
mlflow ui --host=0.0.0.0 --port=3389
```

mnist 실험을 클릭해 확인해보자.

![스크린샷 2022-05-08 23.57.08.png](images/img3.png)

acc를 기준으로 내림차순 정렬

![스크린샷 2022-05-08 23.58.54.png](images/img4.png)

Filtering - metrics.acc > 0.95 : Accuracy가 95%보다 높은 학습만 필터링해서 보기

![스크린샷 2022-05-09 00.00.21.png](images/img5.png)

<br/>

## D. 모델 레지스트리

B에서 모델을 저장하기 위해 `log_artifacts()` 메소드를 사용했다. 하지만 이는 model에 특화된 아티팩트 저장법이 아니라 일반적으로 사용할 수 있는 메소드이다. 하지만 MLFlow가 관리해주는 모델 레지스트리에 저장하기 위해서는 `mlflow.tensorflow.log_model()` 메소드를 사용해야 한다.

기존의 mlflow-src/mnist 폴더에 새로운 파일을 만들고 main.py에서 log_artifacts 부분만을 변경하였다.

`mlflow-src/mnist/mnist_with_log_model.py`

```python
import tensorflow as tf
import argparse
import mlflow

############################
uri = "file:///home/jsuwan961205_9/mlruns"
mlflow.set_tracking_uri(uri)
experiment_name = "mnist"
mlflow.set_experiment(experiment_name)
############################

parser = argparse.ArgumentParser()
parser.add_argument(
    "--batch_size",
    type=int,
    default=512,
    help="input datasets batch size"
)
parser.add_argument(
    "--epochs",
    type=int,
    default=5,
    help="input epochs"
)

args = parser.parse_args()
mlflow.log_param("batch_size", args.batch_size)
mlflow.log_param("epochs", args.epochs)
mnist = tf.keras.datasets.mnist

(x_train, y_train), (x_test, y_test) = mnist.load_data()
x_train, x_test = x_train / 255.0, x_test / 255.0

model = tf.keras.models.Sequential([
  tf.keras.layers.Flatten(input_shape=(28, 28)),
  tf.keras.layers.Dense(256, activation='relu'),
  tf.keras.layers.Dropout(0.2),
  tf.keras.layers.Dense(10, activation='softmax')
])

model.compile(optimizer='adam',
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])

model.fit(
  x_train,
  y_train,
  batch_size=args.batch_size,
  epochs=args.epochs
)

loss, acc = model.evaluate(x_test,  y_test, verbose=2)
print(f"model loss: {loss:.4f} acc: {acc:.4f}")
mlflow.log_metric("loss", loss)
mlflow.log_metric("acc", acc)
model.save("saved_model")
# mlflow.log_artifacts("saved_model")
mlflow.tensorflow.log_model(
    tf_saved_model_dir="saved_model", 
    tf_meta_graph_tags=["serve"],
    tf_signature_def_key="serving_default",
    artifact_path="model"
)
```

실행해보자.

```python
python main_with_log_model.py
```

그리고 대시보드를 확인해보자. 제일 최근의 실행에서 Models에 tensorflow라고 태깅되어 있는 것을 확인할 수 있다. 빨간색으로 표시한 부분을 클릭해보면 실행 상세 페이지로 이동할 수 있다.

![스크린샷 2022-05-09 00.14.02.png](images/img6.png)

상세 페이지를 확인해보면 기존과 다르게 Register Model 이라는 버튼이 있는 것을 확인할 수 있다.

![스크린샷 2022-05-09 00.15.21.png](images/img7.png)

모델 등록 버튼을 누르면 아래와 같이 등록을 위한 안내 팝업이 나오는데 아래와 같이 기입하고 Register를 클릭해보았다.

![Untitled](images/Untitled11.png)

하지만 여기서 에러가 나왔다. 

<aside>
❌ INVALID_PARAMETER_VALUE: Model registry functionality is unavailable; got unsupported URI './mlruns' for model registry data storage. Supported URI schemes are: ['postgresql', 'mysql', 'sqlite', 'mssql']. See [https://www.mlflow.org/docs/latest/tracking.html#storage](https://www.mlflow.org/docs/latest/tracking.html#storage) for how to run an MLflow server against one of the supported backend storage locations

</aside>

MLFlow 공식 Docs에 따르면 DB를 연결해줘야 한다고 한다.

![Untitled](images/Untitled12.png)

그래서 조금 복잡하지만 VM에 mysql을 설치하고 연결해주자.

VM에 도커가 설치되어 있다는 가정하에 진행했다.

1. mysql 설치
   
    ```bash
    # mysql 설치
    docker run --name mlflow-registry -e MYSQL_ROOT_PASSWORD=jang -d -p 3306:3306 mysql:latest
    ```
    
2. mysql-connector 설치
   
    ```bash
    pip install mysql-connector-python
    ```
    
3. mlflow server 연결
   
    ```bash
    mlflow server --host=0.0.0.0 --port=3389 --backend-store-uri mysql+mysqlconnector://root:jang@localhost:3306/mysql?charset=utf8 --default-artifact-root /home/jsuwan961205_9/mlruns/
    ```
    
    기존에는 mlflow ui를 사용했지만 지금은 mlflow server로 연결했다. server가 ui를 포함하는 상위 개념이라 생각하면 좋을 듯하다. backend-store-uri를 `sqlalchemy` 연결방식과 동일하게 URI를 지정해주고 실제 artifacts가 저장될 위치인 default-artifact-root를기존과 동일하게 /home/jsuwan961205_9/mlruns로 저장해주었다.
    

이제 다시 MLFlow Dashboard에 접속해보자. 나의 경우 [http://34.125.193.50:3389/](http://34.125.193.50:3389/) 기존 URL과 동일하다.

![Untitled](images/Untitled13.png)

아무런 실험이 없는 것을 확인할 수 있는데, 이는 쉽게말하면 mlruns 폴더가 변경되었기 때문이다. 기존에는 `/home/jsuwan961205_9/mlruns` 폴더를 MLFlow Dashboard가 바라보고 있었는데 그 대상이 MySQL로 변경된 것이다.

mnist라는 실험을 만들어보자. 이때 Artifact Location를 `/home/jsuwan961205_9/mlruns` 로 지정해주자. 말 그대로 Artifact 들이 저장될 위치이다. Artifact는 parameter, metric과 다르게 일반적으로 큰 사이즈를 가진다. 따라서 저장될 위치를 지정하는 것이다. 이는 보통 Cloud Storage를 사용한다. 

![Untitled](images/Untitled14.png)

이제 새로운 파일을 만들고 실행시켜보자.

기존의 main_with_log_model.py와 바뀐점은 tracking을 하는 URI만 변경되었다. MySQL에 Tracking 정보들이 저장된다.

`mlflow_src/mnist/main_with_db.py`

```bash
import tensorflow as tf
import argparse
import mlflow

############################
uri = "http://34.125.193.50:3389/" # 기존과 변경된 점
mlflow.set_tracking_uri(uri)
experiment_name = "mnist"
mlflow.set_experiment(experiment_name)
############################

parser = argparse.ArgumentParser()
parser.add_argument(
    "--batch_size",
    type=int,
    default=512,
    help="input datasets batch size"
)
parser.add_argument(
    "--epochs",
    type=int,
    default=5,
    help="input epochs"
)

args = parser.parse_args()
mlflow.log_param("batch_size", args.batch_size)
mlflow.log_param("epochs", args.epochs)
mnist = tf.keras.datasets.mnist

(x_train, y_train), (x_test, y_test) = mnist.load_data()
x_train, x_test = x_train / 255.0, x_test / 255.0

model = tf.keras.models.Sequential([
  tf.keras.layers.Flatten(input_shape=(28, 28)),
  tf.keras.layers.Dense(256, activation='relu'),
  tf.keras.layers.Dropout(0.2),
  tf.keras.layers.Dense(10, activation='softmax')
])

model.compile(optimizer='adam',
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])

model.fit(
  x_train,
  y_train,
  batch_size=args.batch_size,
  epochs=args.epochs
)

loss, acc = model.evaluate(x_test,  y_test, verbose=2)
print(f"model loss: {loss:.4f} acc: {acc:.4f}")
mlflow.log_metric("loss", loss)
mlflow.log_metric("acc", acc)
model.save("saved_model")
# mlflow.log_artifacts("saved_model")
mlflow.tensorflow.log_model(
    tf_saved_model_dir="saved_model", 
    tf_meta_graph_tags=["serve"],
    tf_signature_def_key="serving_default",
    artifact_path="model"
)
```

실행

```bash
python main_with_db.py
```

실행이 잘 되었으면 로컬의 파일 구성변화는 하나밖에 없다. /home/jsuwan961205_9/mlruns 폴더 내부에 새로운 폴더가 생겼고 내부에 파일이 저장되어있다.

```bash
─── d8055ee1ca7e460295cd559eb66fa8e1
    └── artifacts
        └── model
            ├── MLmodel
            ├── conda.yaml
            ├── requirements.txt
            └── tfmodel
                ├── assets
                ├── keras_metadata.pb
                ├── saved_model.pb
                └── variables
                    ├── variables.data-00000-of-00001
                    └── variables.index
```

`d8055ee1ca7e460295cd559eb66fa8e1` 의 경로는 MySQL 내부에 저장되어 있음을 짐작할 수 있을 것 같다.

대시보드를 확인해보자

![Untitled](images/Untitled15.png)

하나의 실행이 기록되었고 모델을 등록해보자

![Untitled](images/Untitled16.png)

기존과 다르게 모델이 잘 등록되는 것을 확인할 수 있다.

<br/>

## E. 모델 배포

모델을 저장했다면 이를 로컬에 배포할 수도 있다. 간단한 명령어로 할 수 있다.

```bash
export MLFLOW_TRACKING_URI=http://34.125.193.50:3389/

mlflow models serve -m "models:/mnist/latest" --no-conda
```

실행 결과

![Untitled](images/Untitled17.png)

**Reference**

- [https://databricks.com/kr/p/webinar/managing-the-machine-learning-lifecycle-with-mlflow-kr](https://databricks.com/kr/p/webinar/managing-the-machine-learning-lifecycle-with-mlflow-kr)
- [https://lsjsj92.tistory.com/623](https://lsjsj92.tistory.com/623)