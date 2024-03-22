# 24-1 선문대학교 스마트정보통신공학과 캡스톤디자인2(14분반)</br>
### 팀명: 과사앞집애들</br>

### 팀원: 이규석(팀장), 김범준, 이건우</br>

## 주제<br>
인공지능을 활용한 뇌파 기반 이미지 생성 GUI 프로그램<br>

## 프로젝트 개요</br>
현대 뇌과학에서 EEG(뇌전도)는 저렴한 가격과 비침습적 방법으로 측정한 데이터로 뇌 분석 시 많이 활용하고 있다.</br>
그러나 측정 시 환경적 영향으로 인한 잡음 전처리 및 사람 개개인의 특성에 따른 차이로 인해 분석하는데 어려움이 있다.</br>
이와 같은 문제로 인해 EEG를 Text, Image 등 다른 양식의 데이터로 변환하는 기술에 대한 관심이 높아졌다.</br>
특히, 사람은 시각적인 정보를 통해 이해하는 방법이 더 효과적이기 떄문에 이러한 기술은 사람의 생각과 심리를 이해하는데</br>
EEG 자체를 분석하는 방법보다 더 효과적이기 때문에 이 기술은 뇌 과학에서 중요한 연구 프로젝트로 자리 잡았다.</br>
우리 팀은 EEG-to-Image Generation를 위한 딥러닝 네트워크를 설계하고 이를 사용하기 위한 서비스로</br>
GUI 프로그램 개발을 목적으로 한다.


## 데이터셋<br>
### EEG-Image</br>

(1) [**EEG-ImageNet**](https://drive.google.com/drive/u/0/folders/1Nmoj1Qg3TkLtHvfp3ypKfPAiQZgBQcLJ)</br>
ImageNet Dataset에서 가져온 40 Class에 대한 50장의 이미지를 가져와 총 2000장의 이미지에 대한 6명의 피험자의</br>
EEG 데이터를 측정하여 공개한 EEG-Image 쌍 데이터이다. EEG는 128-channel 센서를 사용하였으며 이미지 당 0.5 [s] 단위로<br>
측정을 하였으며 데이터는 6명(피험자) x 2000장(이미지) = 12,000 Segment에서 측정 품질이 낮은 36개 샘플은 제거하여</br>
11,964 Segment의 EEG-Image 쌍 데이터이다.</br>
전처리로 각각의 Segment들의 측정 시 정확한 지속시간이 다르기에 초기 0.2 [ms](= 0.02 [s])는 제거하는 방법을 제시하였다.

**[참조]** [github link](https://github.com/perceivelab/eeg_visual_classification)

(2) [**A large and rich EEG dataset for modeling human visual object recognition**](https://osf.io/3jk45/)</br>
64-channel

### EEG-Text<br>

(1) ZuCo 2.0</br>
[download](https://osf.io/2urht/)
