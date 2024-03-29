# Firewall
# How to use
1. requirements.txt 에 해당하는 파일들을 설치한다.
2. 창을 열고 sudo -E env "PATH=$PATH" python3 Web_Firewall.py 명령어로 웹 방화벽을 실행한다.
3. 다른 창을 열고 python3 app.py 명령어로 플라스크 웹서버를 실행한다.
4. 로그대쉬보드의 경우 본웹서비스의 create를 통해 만들어야 시그니처넘버가 찍히고 그것을 기반으로 불러오기에 반드시 본서비스의 create를 이용하도록 한다.

# Demonstration
## 로그 대쉬보드 테스트
1. create를 누르고 inbound를 선택 후 src ip를 10.1.2.3 dst ip를 10.1.2.2 로설정한다.
2. ping을 날린다.
3. 대쉬보드를 확인해본다.

## 웹 로그 대쉬보드 테스트
1. create를 누르고 outbound를 선택 후 웹방화벽을 사용함에 체크한다.(디폴트)
2. index에서 iptable에 nfque가 뜬것을 확인한다.
3. 웹방화벽을 킨다.(sudo -E env "PATH=$PATH" python3 Web_Firewall.py)
3. 해당 호스트에서 curl -X POST < http사이트 > -d "param1=< script >alert('hi2');< /script >"
4. 웹 방화벽 대쉬보드 페이지를 확인한다.

# CRUD
## 1. Index Page(Read, Update, Delete, Unused Policy)
### 1> Read, Delete, Unused Policy

![그림3](https://github.com/BoB-Dev-Top30/Firewall/assets/109223193/f9cecc43-ce09-48dd-b977-606a82c46051)


페이지에는 사용자가 체크박스를 선택하여 삭제와 업데이트를 수행할 수 있는 기능이 포함되어 있으며, 이 기능은 iptables의 'num'이라는 인덱스를 기반으로 한 알고리즘을 사용합니다. 삭제와 업데이트 기능을 사용하기 위해서는 사용자가 체크박스를 선택한 상태에서 POST 요청을 보내야 합니다. 이 과정은 JavaScript를 사용하여 구현되어 있어 사용자가 체크박스를 반드시 선택하도록 설계되었습니다. 특히, 사용자는 여러 체크박스를 한 번에 선택하여 삭제할 수 있으며, 삭제 시에는 iptables의 '-D' 옵션을 사용합니다. 또한 Unused 버튼을 통해 사용자는 실제로 사용하지 않고 있느 정책들을 필터링 할 수 있습니다.



### 2> Update

![그림4](https://github.com/BoB-Dev-Top30/Firewall/assets/109223193/54758f2d-4bd3-4e09-947d-2715dbf1135f)


그러나 업데이트 기능은 한 번에 하나의 항목만 가능하도록 제한되어 있으며, 이 역시 JavaScript를 통해 구현되어 여러 체크박스 선택을 방지합니다.

'number' 필드와 'chain' 필드 같은 특정 항목들을 변경할 수 없습니다. 이들은 마치 프라이머리 키와 같은 역할을 하기 때문에, 프론트엔드에서 이 필드들을 읽기 전용으로 설정하여 사용자가 이를 변경하지 못하도록 합니다. 사용자가 나머지 값을 채우고 'Create' 버튼을 누르면, 선택된 'num' 필드의 값이 사용자가 입력한 새로운 정보로 업데이트됩니다. 이 과정에는 iptables의 '-R' 옵션이 사용됩니다.

## 2.  Create Page

![그림-2](https://github.com/BoB-Dev-Top30/Firewall/assets/109223193/e7af8268-6bfc-4670-a600-a21e9338e6c5)



사용자 입장에서 실제로 필요하고 자주 사용될 수 있는 핵심 요소들만을 포함시켰습니다. 또한, 프론트엔드에서는 JavaScript를 활용하여 CIDR을 포함한 IP 주소와 포트 번호의 유효성을 검증했습니다. 
# Monitoring
## 1. Network-State Page(Conntrack)

![그림5](https://github.com/BoB-Dev-Top30/Firewall/assets/109223193/e8d61c08-abcd-4082-84e7-c689a0235513)



이 기능의 핵심은 사용자에게 중요한 정보를 필터링하여 보여주는 것에 있었습니다. 그래서 내부 프로세스 간 통신(ipc 통신)을 명시적으로 제외하고, 'established'와 'related' 상태에 있는 연결만을 필터링하도록 특정 명령어를 설정했습니다.
또한, 사용자가 필요한 정보를 쉽게 찾을 수 있도록 검색 기능을 추가했습니다. 이 기능은 테이블의 모든 열을 검사하여 사용자의 검색 조건과 일치하는 결과가 있을 때 해당 결과를 화면에 렌더링하도록 구성되어 있습니다. 이러한 방식으로, 사용자는 네트워크 상태 정보를 보다 효과적으로 모니터링 할 수 있습니다.

## 2. Dashboard Page(Log Info)

![그림6](https://github.com/BoB-Dev-Top30/Firewall/assets/109223193/6f997596-36c9-4bac-a1ef-ec059aaf61c8)


명확하고 직관적인 로그 분석을 위해, 다섯 가지 주요 파트로 구성된 대쉬보드를 제공하였습니다. 사용자는 비동기식으로 데이터를 요청하며, Flask 서버는 JSON 형태로 데이터를 응답합니다. 이 데이터는 레이블(label)과 값(value) 필드로 구성되어 있으며, 받아온 데이터를 기반으로 그래프를 작성하여 대쉬보드에 렌더링합니다.

데이터 전달을 위한 가공 과정은 필수적입니다. 이를 위해 log_parser라는 자체 제작 모듈을 통해 로그 데이터를 JSON 구조에 맞게 파싱하여 전달하도록 구현하였습니다. 이러한 접근 방식은 사용자가 로그 데이터를 보다 효과적으로 이해하고 분석할 수 있게 돕습니다.

# Deatail_Management
## 1. Packet Simulation

![그림9](https://github.com/BoB-Dev-Top30/Firewall/assets/109223193/f532f63e-5458-4ef4-a1ec-58600114ff0b)


방화벽의 네트워크 정책의 매칭 여부를 확인하고 이를 바 그래프 형태로 시각화하는 기능이 주요 기능입니다. 이 과정을 위해 비동기식 통신이 필요하며, AJAX 방식을 사용하여 구현하였습니다. 처음에 사용자가 /packet_simulate 경로로 접속하면, GET 요청을 통해 packet_simulate.html 페이지가 렌더링됩니다.


사용자는 IP 주소를 입력하는 폼을 채우고, 같은 엔드포인트로 POST 요청을 보냅니다. 이후, Flask 서버는 JSON 데이터 형식으로 응답을 받아 처리합니다.
Match_Rule이라는 자체 개발된 모듈의 함수를 통해 매칭된 체인, 매칭되지 않은 체인, 그리고 각각의 개수를 반환합니다. 이 모듈은 자체 알고리즘을 기반으로 작동합니다.

![그림10](https://github.com/BoB-Dev-Top30/Firewall/assets/109223193/28b6da5a-d09e-45e8-9c87-a751cb679a69)

서버에서 생성된 데이터는 프론트엔드로 전달되며, 데이터 전달 시 sort_keys=false 옵션을 사용하여 데이터가 키 기반으로 자동 정렬되지 않도록 합니다. 프론트엔드는 이 데이터를 바탕으로 기존의 그래프를 지우고 새로운 바 그래프를 그려 사용자에게 매칭된 정책과 매칭되지 않은 정책의 개수를 시각적으로 보여줍니다.

또한, 사용자는 두 개의 버튼을 통해 매칭된 정책과 매칭되지 않은 정책을 볼 수 있습니다. 이 버튼들은 JavaScript를 사용하여 동적으로 생성되며, 기존 버튼이 있을 경우 제거한 후 새로 만들어 항상 두 개의 버튼이 유지되도록 설계되었습니다. 이러한 방식으로 사용자는 매칭 여부에 따른 정책들을 더욱 효과적으로 확인하고 분석할 수 있습니다.

각각의 버튼은 사용자를 다른 엔드포인트로 안내하는 역할을 하며, 버튼 클릭 시 matched_chain 또는 unmatched_chain 데이터(리스트 형태)를 각각 ./matched나 ./unmatched 엔드포인트로 POST 요청을 통해 전송합니다. 이러한 요청은 Flask 서버에서 데이터 형식을 재구성하는 목적으로 사용됩니다.

마지막은 /match_table로 요청을 보내줍니다.

![그림11](https://github.com/BoB-Dev-Top30/Firewall/assets/109223193/febe7349-d8c9-4c87-bad1-cdb54d39b71b)



## 2. Web-Firewall

Linux의 NetfilterQueue를 사용하여, 패킷을 인터셉트하고 사용자 정의 함수(process_packet)로 전달합니다. Scapy를 이용해 가로챈 패킷에서 소스 및 목적지 IP, 포트 번호, 프로토콜 정보를 추출합니다. 특히, HTTP 프로토콜을 사용하는 패킷의 내용을 분석하여 GET 및 POST 요청을 확인합니다. 제작한 모듈(DP_Xss, DP_Sql_Injection)을 통해 XSS 및 SQL 인젝션 공격 패턴을 감지합니다. 이 과정에서 감지된 공격 유형에 따라 해당 패킷을 수정하거나, 공격 정보를 로깅합니다. 공격이 감지되면, 공격 유형, 소스 및 목적지 정보, 프로토콜, 공격 횟수 등의 상세 정보를 로그 파일에 기록합니다. 이를 통해 대쉬보드 형태의 서비스를 제공하도록 합니다. 감지된 보안 위협에 대응하여 안전하게 수정된 패킷으로 원본 패킷을 교체한 후, 네트워크로 다시 전송합니다. 스크립트는 사용자가 종료 요청을 할 때까지 넷필터 큐를 통해 패킷을 처리하는 루프에서 실행됩니다. 사용자가 종료(예: 키보드 인터럽트)를 요청하면, 넷필터 큐 바인딩을 해제하고 스크립트를 안전하게 종료합니다.

![그림14](https://github.com/BoB-Dev-Top30/Firewall/assets/109223193/e1b06a5b-1d8d-4c5e-ab8e-b769222da038)

![그림15](https://github.com/BoB-Dev-Top30/Firewall/assets/109223193/dc4a25fb-6823-4ded-b978-22a9a9581eed)

![그림16](https://github.com/BoB-Dev-Top30/Firewall/assets/109223193/904e0924-544e-43a0-8be9-c580c882e9c0)

![그림17](https://github.com/BoB-Dev-Top30/Firewall/assets/109223193/b56b5fcf-a46c-4196-a172-c57a25372ec7)


