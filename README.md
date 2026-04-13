                                    [Backend] FastAPI 기반 병원 관리 시스템 (Mini Project)
<img width="1322" height="505" alt="image" src="https://github.com/user-attachments/assets/26c25f92-4229-47fc-aacc-24181b022a03" />

🏥 Hospital Management System (FastAPI)
FastAPI와 MySQL을 활용한 병원 관리 시스템 백엔드 프로젝트입니다. 
환자, 의사, 예약 및 처방 정보를 체계적으로 관리할 수 있도록 설계되었습니다.

🛠 Tech Stack
- Framework: FastAPI
- Database: MySQL
- ORM: SQLAlchemy
- Language: Python 3.10+
- Tools: Visual Studio Code, MySQL Workbench

📊 Database ERD
이 프로젝트는 데이터 무결성을 위해 정규화된 5개의 테이블로 구성되어 있습니다.

- Patients: 환자 기본 정보 관리
- Doctors: 의사 정보 및 전공 분야 관리
- Appointments: 환자와 의사 간의 예약 스케줄링 (중간 테이블 역할을 겸함)
- Prescriptions: 진료 후 발급되는 약처방 정보
- Wards: 병동 관리 및 담당 의사 배정

🚀 Key Features (API 명세)
- 상세한 기능 명세 및 실행 화면은 아래 노션 링크에서 확인하실 수 있습니다.
- 병원 관리 시스템 프로젝트 상세 문서 (Notion)

1. 환자 및 의사 관리
환자 정보 등록, 수정, 조회 (CRUD)

의사 전공 및 면허 번호 관리

2. 예약 시스템
환자와 의사를 매칭하여 예약 생성

진료 상태(SCHEDULED, COMPLETED 등) 업데이트

3. 진료 및 병동 관리
예약 기반의 처방전 발행

병동별 병상 수 관리 및 담당 의사 연결


FastAPI/api명세서, 결과물
https://www.notion.so/FastAPI-336c4baf3ec880879c15ff988c002178
