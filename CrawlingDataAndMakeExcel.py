from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import time

# Excel에서 허용하지 않는 문자를 제거하는 함수
def remove_illegal_characters(text):
    # Excel에서 허용하지 않는 문자를 제거 (ASCII 0~31, 제외: \n, \r, \t)
    return ''.join(filter(lambda x: x == '\n' or x == '\r' or x == '\t' or ord(x) > 31, text))

# Selenium 설정
options = webdriver.ChromeOptions()
options.add_argument('--ignore-ssl-errors=yes')
options.add_argument('--ignore-certificate-errors')

driver = webdriver.Chrome(options=options)

# 데이터를 저장할 리스트
data = []

def crawl_page(page_number):
    url = f'WEB PAGE URL WHERE I WANT TO CRAWL DATA?page={page_number}'
    driver.get(url)

    # 페이지가 완전히 로드될 때까지 기다림
    time.sleep(5)

    # 현재 페이지의 소스를 가져옴
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    # 모든 질문 항목 찾기
    questions = soup.find_all('li', class_='py-3.5 sm:py-4')

    for question in questions:
        # 제목 추출
        title = remove_illegal_characters(question.find('a',
                                                        class_='line-clamp-1 w-fit truncate whitespace-normal break-all text-sm font-semibold text-gray-900 hover:text-blue-500 sm:text-lg dark:text-gray-100 dark:hover:text-blue-200').text.strip())

        # 내용 요약 추출
        summary = remove_illegal_characters(question.find('a',
                                                          class_='line-clamp-2 w-fit truncate whitespace-normal break-all text-xs font-normal text-gray-500 hover:text-blue-500 sm:text-sm dark:text-gray-100 dark:hover:text-blue-200').text.strip())

        # 태그 추출
        tags = ', '.join(remove_illegal_characters(tag.text) for tag in question.find_all('a',
                                                                                          class_='line-clamp-1 text-xs font-normal leading-5 text-gray-600 hover:text-blue-500 sm:text-sm dark:text-gray-400 dark:hover:text-blue-200'))

        # 데이터 저장
        data.append([title, summary, tags])

    return True  # 페이지 처리 성공

# 첫 페이지부터 500페이지까지 순회
for page in range(1, 50000):
    print(f'Crawling page {page}')
    if not crawl_page(page):
        print(f'Failed to crawl page {page}')
        break

# 모든 페이지 크롤링이 끝난 후 WebDriver 종료
driver.quit()

# 데이터를 pandas DataFrame으로 변환
df = pd.DataFrame(data, columns=['reviewTitle', 'reviewContent', 'Tags'])

# Excel 파일로 저장
excel_filename = 'okky_questions_new.xlsx'
df.to_excel(excel_filename, index=False)

print(f'Data saved to {excel_filename}')