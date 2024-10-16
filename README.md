# Magi

[한국어](README.md) | [English](docs/en/README.md)

Magi는 AI가 스스로 프롬프트를 개선할 수 있는지 실험하는 개인 토이 프로젝트입니다.

## 개요

Magi 프로젝트는 LLM(Large Language Model)을 이용해 LLM의 출력을 분석하고, 그 결과를 바탕으로 프롬프트를 개선하는 과정을 반복합니다. 이를 통해 AI의 자기 개선 가능성과 한계를 탐구합니다.

## 핵심 아키텍처

Magi의 아키텍처는 세 가지 핵심 요소로 구성됩니다:

1. 재귀적 프롬프트 업그레이드
2. 다중 관점 분석 시스템
3. 메타 평가 및 최적화

### 재귀적 프롬프트 업그레이드

LLM을 통해 LLM의 출력을 분석하고, 그 결과를 바탕으로 프롬프트를 개선하는 과정을 반복합니다.

### 다중 관점 분석 시스템

여러 캐릭터를 통해 프롬프트를 다각도로 분석합니다:

1. 멜키오르(전략가): 전체적인 관점에서 작업의 효과를 평가하고 발전시킵니다.
2. 카스파르(혁신가): 혁신적이고 독창적인 아이디어를 제시합니다.
3. 발타사르(분석가): 데이터와 논리에 기반해 효율적이지 못한 작업을 최소화합니다.

### 메타 평가 및 최적화

Magi 캐릭터가 관리자 역할을 수행하여 프로세스의 최중요 책임 사항을 결정합니다:

1. 사용자의 초기 프롬프트에서 의도 분석
2. 각 캐릭터의 제안을 객관적으로 평가
3. 다양한 아이디어를 종합
4. 프로젝트의 방향성 유지

## 설치 방법

1. 저장소 클론:
    ```
    git clone https://github.com/ParallelKim/Magi.git
    ```
2. 의존성 설치:
    ```
    pip install -r requirements.txt
    ```
3. 환경변수 설정:
    ```
    export OPENAI_API_KEY=<your_openai_api_key>
    ```

## 사용 예시

```python
from magi import Magi
magi = Magi(model_name="gpt-4o-mini")
initial_prompt = "AI의 자기 발전에 대해 설명해주세요."
improved_prompt = magi.recursive_prompt_upgrade(5, initial_prompt)
print(improved_prompt)
```

## 현재 과제

1. 캐릭터 페르소나 개선
2. 개선 평가 기준 고도화
3. 확장성 향상
4. 사용자 피드백 통합

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

## 추가 정보

프로젝트의 전체 코드와 실험 결과는 [GitHub 저장소](https://github.com/ParallelKim/Magi)에서 확인할 수 있습니다.
