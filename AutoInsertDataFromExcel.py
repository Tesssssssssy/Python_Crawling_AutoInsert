import pandas as pd
import mysql.connector

# 엑셀 파일에서 데이터 읽기
excel_file = '/.../questions.xlsx'
df = pd.read_excel(excel_file)

# 'nan' 값을 빈 문자열로 대체
df['reviewTitle'] = df['reviewTitle'].fillna('')
df['reviewContent'] = df['reviewContent'].fillna('')

# MySQL 데이터베이스 연결 설정
mydb = mysql.connector.connect(
    host="DATABASE IP",
    user="DATABASE ID",
    password="DATABASE PW",
    database="DATABASE NAME"
)
cursor = mydb.cursor()

# 데이터 삽입
for index, row in df.iterrows():
    insert_query = """
    INSERT INTO Review (
        User_idx, ReviewCategory_idx, reviewTitle, reviewContent, courseName, 
        courseEvaluation, status, createdAt, updatedAt, viewCnt, upCnt, scrapCnt, commentCnt
    ) VALUES (
        %s, %s, %s, %s, %s, %s, %s, NOW(), NOW(), %s, %s, %s, %s
    );
    """
    cursor.execute(insert_query, (1, 1, row['reviewTitle'], row['reviewContent'], 'REVIEW NAME', 5, True, 0, 0, 0, 0))

# 변경 사항을 커밋
mydb.commit()

# 연결 종료
cursor.close()
mydb.close()
