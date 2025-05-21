from notion_client import Client
import os
from notion2md.exporter.block import MarkdownExporter

NOTION_TOKEN = os.getenv("NOTION_TOKEN")
DATABASE_ID = os.getenv("NOTION_DATABASE_ID")

client = Client(auth=NOTION_TOKEN)

# 1. 필터: Status가 'Publish'인 페이지만
response = client.databases.query(
    **{
        "database_id": DATABASE_ID,
        "filter": {
            "property": "Status",  # 이 이름은 DB 속성명과 일치해야 함
            "multi_select": {
                "contains": "Publish"
            }
        }
    }
)

exporter = MarkdownExporter(client)

# 2. 해당 조건을 만족하는 각 페이지를 Markdown으로 변환
for page in response["results"]:
    page_id = page["id"]

    # 1. title 속성 자동 추출
    title_property = next(
        (k for k, v in page["properties"].items() if v.get("type") == "title"), None
    )

    # 2. 제목 텍스트 추출
    if title_property and page["properties"][title_property]["title"]:
        title = page["properties"][title_property]["title"][0]["plain_text"]
    else:
        title = "Untitled"

    print(title_property)
    md = exporter.export(page_id)

    # 3. 파일로 저장
    filename = f"posts/{title.replace(' ', '_')}.md"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(md)

    print(f"✅ {title} → {filename} Upload!")
