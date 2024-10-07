# Magi

Magi는 재귀적 메타 프로세스를 사용하여 스스로 발전하고 업데이트하는 AI 서비스입니다.

## 개요

Magi 프로젝트는 AI가 자체적으로 프롬프트를 개선하고 최적화하는 능력을 탐구합니다. 이는 더 정확하고 효과적인 AI 응답을 생성하는 것을 목표로 합니다.

## 주요 기능

-   재귀적 프롬프트 업그레이드
-   다중 관점 분석 (전략, 효율성, 창의성)
-   자동 개선 및 최적화

## 설치 방법

1. 저장소 클론:
    ```
    git clone https://github.com/your-username/magi.git
    ```
2. 의존성 설치:
    ```
    pip install -r requirements.txt
    ```

## 사용 예시

```
python
from magi import Magi
magi = Magi(model_name="gpt-4o-mini")
initial_prompt = "AI의 자기 발전에 대해 설명해주세요."
improved_prompt = magi.recursive_prompt_upgrade(5, initial_prompt)
print(improved_prompt)
```

## 작동 원리

Magi는 다음과 같은 단계로 작동합니다:

1. 초기 프롬프트 분석
2. 장단점 평가
3. 개선 전략 수립
4. 프롬프트 업그레이드
5. 결과 평가 및 반복

이 과정을 통해 프롬프트는 점진적으로 개선되며, 더 정확하고 유용한 AI 응답을 이끌어냅니다.

## 기여하기

프로젝트에 기여하고 싶으시다면 다음 단계를 따라주세요:

1. 이 저장소를 포크합니다.
2. 새 브랜치를 만듭니다 (`git checkout -b feature/AmazingFeature`).
3. 변경사항을 커밋합니다 (`git commit -m 'Add some AmazingFeature'`).
4. 브랜치에 푸시합니다 (`git push origin feature/AmazingFeature`).
5. Pull Request를 열어주세요.

## 라이선스

이 프로젝트는 MIT 라이선스 하에 배포됩니다. 자세한 내용은 `LICENSE` 파일을 참조하세요.

## 연락처

프로젝트 관리자 - parallelkim12@gmail.com

프로젝트 링크: [https://github.com/ParallelKim/Magi](https://github.com/ParallelKim/Magi)
