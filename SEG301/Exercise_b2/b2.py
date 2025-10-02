# cài đặt hệ thống IR mã nguồn mở 
# pip install whoosh


from whoosh.fields import Schema, TEXT, ID
from whoosh import index
import os

# 1. Định nghĩa schema (mô tả tài liệu)
schema = Schema(title=TEXT(stored=True), path=ID(stored=True), content=TEXT)

# 2. Tạo thư mục index
if not os.path.exists("indexdir"):
    os.mkdir("indexdir")
ix = index.create_in("indexdir", schema)

# 3. Thêm tài liệu vào index
writer = ix.writer()
docs = {
    "email1.txt": "Xin chào, đây là email test về lịch họp tuần sau",
    "memo1.txt": "Team cần hoàn thành báo cáo công việc vào thứ Sáu",
    "news1.txt": "AI đang thay đổi cách vận hành của công cụ tìm kiếm"
}
for name, text in docs.items():
    writer.add_document(title=name, path=name, content=text)
writer.commit()

# 4. Tìm kiếm tài liệu
from whoosh.qparser import QueryParser

with ix.searcher() as searcher:
    query = QueryParser("content", ix.schema).parse("tìm kiếm")
    results = searcher.search(query)
    for r in results:
        print(r['title'], "->", r.score)



# Query: "AI" → nên trả về news1.txt.
# Query: "báo cáo" → nên trả về memo1.txt.S
# Query: "lịch họp" → nên trả về email1.txt.