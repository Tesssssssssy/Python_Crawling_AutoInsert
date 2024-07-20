from selenium import webdriver
from bs4 import BeautifulSoup
import time

# Selenium 설정
options = webdriver.ChromeOptions()
options.add_argument('--ignore-ssl-errors=yes')
options.add_argument('--ignore-certificate-errors')

driver = webdriver.Chrome(options=options)

def crawl_page(page_number):
    url = f'WEB PAGE URL WHERE I WANT TO CRAWL DATA?page={page_number}'
    driver.get(url)

    # 페이지가 완전히 로드될 때까지 기다림 (조정 가능)
    time.sleep(5)

    # 현재 페이지의 소스를 가져옴
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    # 모든 질문 항목 찾기
    questions = soup.find_all('li', class_='py-3.5 sm:py-4')

    for question in questions:
        # 제목 추출
        title = question.find('a', class_='line-clamp-1 w-fit truncate whitespace-normal break-all text-sm font-semibold text-gray-900 hover:text-blue-500 sm:text-lg dark:text-gray-100 dark:hover:text-blue-200').text.strip()

        # 내용 요약 추출
        summary = question.find('a', class_='line-clamp-2 w-fit truncate whitespace-normal break-all text-xs font-normal text-gray-500 hover:text-blue-500 sm:text-sm dark:text-gray-100 dark:hover:text-blue-200').text.strip()

        # 태그 추출
        tags = [tag.text for tag in question.find_all('a', class_='line-clamp-1 text-xs font-normal leading-5 text-gray-600 hover:text-blue-500 sm:text-sm dark:text-gray-400 dark:hover:text-blue-200')]

        print(f'Title: {title}')
        print(f'Summary: {summary}')
        print(f'Tags: {tags}\n')

    return True  # 페이지 처리 성공

# 첫 페이지부터 10페이지까지 순회
for page in range(1, 11):
    print(f'Crawling page {page}')
    if not crawl_page(page):
        print(f'Failed to crawl page {page}')
        break

# 모든 페이지 크롤링이 끝난 후 WebDriver 종료
driver.quit()