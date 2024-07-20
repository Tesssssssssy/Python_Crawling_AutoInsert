import pandas as pd
from selenium import webdriver
from bs4 import BeautifulSoup

# Selenium 설정
options = webdriver.ChromeOptions()
options.add_argument('--ignore-ssl-errors=yes')
options.add_argument('--ignore-certificate-errors')
driver = webdriver.Chrome(options=options)

# URL 설정
url = 'WEB PAGE URL WHERE I WANT TO CRAWL DATA'
# 페이지 요청
driver.get(url)

# 페이지 소스 가져오기
page_source = driver.page_source

# BeautifulSoup으로 파싱
soup = BeautifulSoup(page_source, 'html.parser')

# 데이터 수집을 위한 빈 리스트 생성
training_info = []

# 각 li 태그에서 데이터 추출
for li in soup.select('div.detailListWrap > ul.detailList > li'):
    info = {}
    # 훈련과정 정보 추출
    info['기관'] = li.select_one('.content .term dd').text.strip()
    info['프로그램 이름'] = li.select_one('.content .tit a').text.strip()

    # 훈련기간 및 시간 추출
    term = li.select_one('.content .time2 dd').text.strip()
    info['훈련시간'] = term.split(',')[1].split()[0]  # "시간"만 추출

    # 다른 회차 정보 추출
    additional_info = li.select_one('.content > .infoView ul')
    if additional_info:
        other_sessions = additional_info.select('li')
        session_info = []
        for session in other_sessions:
            session_text = session.get_text(strip=True).replace(' ~ ', '~').replace(',', ' ~').replace('회차', '회차,')
            session_info.append(session_text)
        info['다른 회차'] = '\n'.join(session_info)
    else:
        info['다른 회차'] = None

    training_info.append(info)

# 데이터프레임 생성
df = pd.DataFrame(training_info)

# 데이터프레임 출력
with pd.option_context('display.max_colwidth', None):  # 출력 컬럼의 너비 제한 해제
    for index, row in df.iterrows():
        print(f"기관: {row['기관']}\n프로그램 이름: {row['프로그램 이름']}\n훈련시간: {row['훈련시간']}\n다른 회차:\n{row['다른 회차']}\n{'-'*50}\n")

# 엑셀 파일로 저장
excel_file_path = '/.../training_info.xlsx'  # 저장할 엑셀 파일 경로
df.to_excel(excel_file_path, index=False)

# 웹 드라이버 종료
driver.quit()

print("엑셀 파일이 성공적으로 저장되었습니다.")
