import pandas as pd
import mysql.connector

# 엑셀 파일에서 데이터 읽기
excel_file = '/.../training_data.xlsx'
df = pd.read_excel(excel_file)

# MySQL 데이터베이스 연결 설정
mydb = mysql.connector.connect(
    host="Database IP",
    user="DB ID",
    password="DB PW",
    database="test"
)
cursor = mydb.cursor()
# 테이블 생성
create_table_query = """
CREATE TABLE IF NOT EXISTS training_data (
    id INT AUTO_INCREMENT PRIMARY KEY,
    training_institution VARCHAR(255),
    program_name VARCHAR(255),
    start_date DATE,
    end_date DATE,
    duration INT
)
"""
cursor.execute(create_table_query)

# 데이터 삽입
for index, row in df.iterrows():
    insert_query = """
    INSERT INTO training_data 
    (training_institution, program_name, start_date, end_date, duration)
    VALUES (%s, %s, %s, %s, %s)
    """
    cursor.execute(insert_query, (row['training_institution'], row['program_name'], row['start_date'], row['end_date'], row['duration']))

# 변경 사항을 커밋
mydb.commit()

# 연결 종료
cursor.close()
mydb.close()
