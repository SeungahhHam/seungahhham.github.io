### Object (객체)
- 데이터베이스 안에서 정의하는 모든 것
- 데이터를 관리하기 위해 생성
- 대표적으로 table, index, view, sequence, synonym
- SQL 명령어는 객체가 아님
### Schema
- object를 담는 그릇
### Segment
- object 중 독자적인 저장 공간을 갖고 있는 것, 데이터가 증가하면 용량이 증가하는 것
  - Data Segment → table, table partition, cluster
  - Index Segment → index-organised table, index partiion
  - Undo Segment → rollback segment
  - Temporary Segment
- 하나 이상의 extent가 모여서 만들어진 것
  - extent: 연속적으로 있는 Block을 묶은 논리적 단위
  - data block: 데이터를 저장하는 최소 논리 단위, logical block or page로 명칭, 데이터를 읽고 쓰는 단위 8K
### Data Dictionary
- DBMS를 효율적으로 사용하기 위해 DB에 저장된 정보를 요약한 것
- DB 정보를 분류하고 처리하기 위한 시스템과 절차로서 데이터를 이해하는 과정에서 발생하는 오류 또는 해석 상의 어려움을 제거하기 위해
- table과 view로 정의
- 사용자 유형 별 접근 권한 차이
  - DBA: 직접 접근 가능, 데이터 사전 갱신 가능
  - 일반 사용자: view를 통해 접근 가능, 읽기만 가능
- Base Table: 중복된 데이터를 제거하는 정규화 과정을 거친 테이블
- View
  - Static View: 하나 이상의 base table과 다른 정적/동적 view를 기반으로 정의된 view, 조인을 이용하여 생성
  - Dynamic View: 동적으로 변경되는 데이터를 테이블 형태로 보여주는 뷰, 동적 뷰를 사용할 때마다 실시간으로 테이블 형태로 생성 ex) 서버 프로세스의 상태, 트랜잭션의 수행 상태, 사용자 권한
### Table
- 데이터를 담고 있는 object, column과 row로 구성
- column(열): row 가 어떻게 구성에 대한 구조 제공, 저장된 데이터 특성 설정
- row(행): 단일 구조 데이터 항목
### View
- 하나 이상의 table을 연결해서 마치 table처럼 사용
- select 문으로 표현되는 질의에 이름을 부여한 가상 table
- 실제 데이터를 포함하지 않음
- 정적뷰 동적뷰
### Index
- 테이블에서 원하는 데이터를 효율적으로 검색하기 위해 사용하는 데이터 구조
- Single Index (단일 컬럼 인덱스): 하나의 column으로 구성
- Concatenated Index (복합 컬럼 인덱스): 하나 이상의 column으로 구성
- Unique Index (유일 인덱스): table에서 유일한 값을 가진 column으로 구성
- Non-Unique Index (비유일 인덱스): 값이 중복 가능한 column으로 구성
- B-Tree 구조(기본): 자식 노드의 개수가 2개 이상인 Tree, 노드 내 데이터가 1개 이상
### Sequence
- 순차적으로 부여되는 고유 번호
  - start with n : 초기화 값
  - increment by n : 증가 값 
  - maxvalue n (nomaxvalue) : 최대값
  - minvalue n (nominvalue) : 최소값
  - cache n : sequence 제공이 용이하도록 메모리에 cache 하는 개수  지정
  - order (noorder) : 병렬 서버일 경우 요청 순서에 따라 정확히 sequnce를 생성하기 원할 때 order로 지정
  - cycle (nocycle) :  cycle로 지정하면 maxvalue에 도달 했을 때 다시 minvalue부터 시작
- 여러 개의 transaction이 서로 겹치지 않는 고유 번호를 만들기 위해 사용
- primary key 값을 생성하기 위해 사용
### Synonym
- object의 alias(별칭)
- 실제 데이터를 포함하지 않음
### Trigger 
- 테이블의 row 삽입, 변경, 삭제할 때 자동으로 수행되도록 지정한 PSM procedure
  - PSM: 절차적 기능을 갖춘 확정된 SQL을 생성하는 강력한 프로그래밍 언어
### Partitio
- 하나의 논리적 테이블을 여러 개의 물리적인 공간으로 나눔
  - Range Partition: 각 파티션에 포함될 Range를 지정하여 파티션 정의
  - Hash Partition: HASH 함수를 이용하여 파티션 정의
  - List Partition: 각 파티션에 포함될 값을 직접 지정하여 파티션 정의
- table을 partition으로 나눌 경우 partition에 실질적 data가 저장
### Object 종류
| DATABASE LINK | 다른 Data Base에 접속할 수 있는 링크 |
| --- | --- |
| DIRECTORY | os directory와 mapping하는 객체 |
| FUNCTION | 특정 연산을 하고 값을 반환하는 객체 |
| INDEX |  |
| LOB | Large Object 구조화되지 않은 데이터를 처리하기 위한 객체
CLOB, BLOB, NCLOB, BFILE |
| PACKAGE | 용도에 맞게 함수나 프로시저 하나로 묶어 놓은 객체 |
| PROCEDURE | 함수와 비슷하지만 값을 반환하지 않는 객체 |
| SEQUENCE |  |
| SQL TRANSLATION PROFILE |  |
| SYNONYM |  |
| TABLE |  |
| TRIGGER |  |
| TYPE |  |
| VIEW |  |

