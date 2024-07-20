import pandas as pd
import mysql.connector

# 엑셀 파일에서 데이터 읽기
excel_file = '/.../questions_new.xlsx'
df = pd.read_excel(excel_file)

# 'nan' 값을 빈 문자열로 대체
df['boardTitle'] = df['boardTitle'].fillna('')
df['boardContent'] = df['boardContent'].fillna('')
df['Tags'] = df['Tags'].fillna('')

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
    insert_board_query = """
    INSERT INTO Board (
        User_idx, BoardCategory_idx, boardTitle, boardContent, status, createdAt, updatedAt, viewCnt, upCnt, scrapCnt, commentCnt
    ) VALUES (
        %s, %s, %s, %s, %s, NOW(), NOW(), %s, %s, %s, %s
    );
    """
    cursor.execute(insert_board_query, (1, 1, row['boardTitle'], row['boardContent'], True, 0, 0, 0, 0))
    board_idx = cursor.lastrowid  # 방금 삽입된 Board의 ID를 가져옵니다.

    # Tags 처리
    if pd.notna(row['Tags']):
        tags = row['Tags'].split(',')  # 태그를 쉼표로 분리하여 리스트로 변환
        for tag in tags:
            tag = tag.strip()  # 공백 제거
            # 해당 태그가 Tag 테이블에 있는지 확인
            cursor.execute("SELECT idx FROM Tag WHERE tagName = %s", (tag,))
            tag_data = cursor.fetchone()

            if tag_data:
                tag_idx = tag_data[0]  # 태그 ID
            else:
                # 새 태그 삽입 (status를 True로 설정)
                cursor.execute("INSERT INTO Tag (tagName, status) VALUES (%s, TRUE)", (tag,))
                tag_idx = cursor.lastrowid  # 새로 삽입된 태그의 ID

            # BoardTag 테이블에 레코드 삽입
            cursor.execute("INSERT INTO BoardTag (Board_idx, Tag_idx, status, createdAt, updatedAt) VALUES (%s, %s, TRUE, NOW(), NOW())", (board_idx, tag_idx))

# 변경 사항을 데이터베이스에 커밋
mydb.commit()

# 연결 종료
cursor.close()
mydb.close()