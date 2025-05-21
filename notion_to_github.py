import requests
import json
import re
from datetime import datetime

# Notion 설정
NOTION_TOKEN = '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'
DATABASE_ID_DATABASE_ID = 'e96e75c4768f47629b1c454838710074'

headers = {
    "Authorization": f"Bearer {NOTION_TOKEN}",
    "Notion-Version": "2022-06-28",  # 버전에 따라 다를 수 있음
    "Content-Type": "application/json"
}

url = f"https://api.notion.com/v1/databases/{DATABASE_ID_DATABASE_ID}/query"


# ✅ 필터 조건 추가: multi_select의 값 중 'Publish' 포함 여부
payload = {
    "filter": {
        "property": "Status",
        "multi_select": {
            "contains": "Publish"
        }
    }
}

def get_blocks(page_id):
    url = f"https://api.notion.com/v1/blocks/{page_id}/children?page_size=100"
    response = requests.get(url, headers=headers)
    return response.json().get("results", [])

def sanitize_filename(title):
    return re.sub(r'[\\/*?:"<>|]', "", title).strip()

def get_page_title(page_id):
    url = f"https://api.notion.com/v1/pages/{page_id}"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        props = response.json()["properties"]
        for key in props:
            if props[key]["type"] == "title":
                title_parts = props[key]["title"]
                return "".join([part["text"]["content"] for part in title_parts])
    return f"notion_page_{page_id}"

def rich_text_to_md(rich_text):
    md = ""
    for part in rich_text:
        text = part["text"]["content"]
        annotations = part["annotations"]
        if annotations["bold"]:
            text = f"**{text}**"
        if annotations["italic"]:
            text = f"*{text}*"
        if annotations["code"]:
            text = f"`{text}`"
        if annotations["strikethrough"]:
            text = f"~~{text}~~"
        if part["text"].get("link"):
            url = part["text"]["link"]["url"]
            text = f"[{text}]({url})"
        md += text
    return md

def block_to_md(block, indent=""):
    t = block["type"]
    b = block[t]
    content = ""

    def get_children_md():
        children = get_blocks(block["id"])
        return ''.join([block_to_md(child, indent + "  ") for child in children])

    if t == "paragraph":
        content = indent + rich_text_to_md(b["rich_text"]) + "\n"
    elif t == "heading_1":
        content = "# " + rich_text_to_md(b["rich_text"]) + "\n"
    elif t == "heading_2":
        content = "## " + rich_text_to_md(b["rich_text"]) + "\n"
    elif t == "heading_3":
        content = "### " + rich_text_to_md(b["rich_text"]) + "\n"
    elif t == "bulleted_list_item":
        content = indent + "- " + rich_text_to_md(b["rich_text"]) + "\n" + get_children_md()
    elif t == "numbered_list_item":
        content = indent + "1. " + rich_text_to_md(b["rich_text"]) + "\n" + get_children_md()
    elif t == "to_do":
        checked = "x" if b["checked"] else " "
        content = indent + f"- [{checked}] " + rich_text_to_md(b["rich_text"]) + "\n"
    elif t == "quote":
        content = "> " + rich_text_to_md(b["rich_text"]) + "\n"
    elif t == "code":
        language = b.get("language", "")
        code_text = rich_text_to_md(b["rich_text"])
        content = f"```{language}\n{code_text}\n```\n"
    elif t == "image":
        image_url = b["external"]["url"] if b.get("external") else b["file"]["url"]
        caption = rich_text_to_md(b.get("caption", []))
        content = f"![{caption}]({image_url})\n"
    elif t == "divider":
        content = "---\n"
    elif t == "table":
        # 처리: 표의 행 가져오기
        rows = get_blocks(block["id"])
        table_rows = []
        for row in rows:
            if row["type"] == "table_row":
                cells = row["table_row"]["cells"]
                row_md = [rich_text_to_md(cell) for cell in cells]
                table_rows.append(row_md)
        if table_rows:
            header = "| " + " | ".join(table_rows[0]) + " |\n"
            divider = "| " + " | ".join(["---"] * len(table_rows[0])) + " |\n"
            body = "".join([f"| {' | '.join(r)} |\n" for r in table_rows[1:]])
            content = header + divider + body
    else:
        content = f"[Unsupported block type: {t}]\n"

    return content

response = requests.post(url, headers=headers, json=payload)

if response.status_code == 200:
    data = response.json()
    pages = []

    for result in data.get("results", []):
        page_id = result["id"].replace("-", "")  # 하이픈 없는 UUID
        full_url = f"https://www.notion.so/{page_id}"
        pages.append({
            "page_id": result["id"],
            "url": full_url
        })

    #with open('notion_urls.json', 'w', encoding='utf-8') as f:
    #    json.dump(pages, f, ensure_ascii=False, indent=4)
    #print("✅ URL 목록이 notion_urls.json에 저장되었습니다!")

else:
    print(f"❌ 에러 발생: {response.status_code}")
    print(response.text)
    
for page in pages:
    page_id = page["page_id"]
    blocks_url = f"https://api.notion.com/v1/blocks/{page_id}/children"

    res = requests.get(blocks_url, headers=headers)
    if res.status_code == 200:
        content = res.json()
        title = get_page_title(page_id)
        safe_title = sanitize_filename(title)
        today = datetime.today().strftime("%Y-%m-%d")
        #with open(f'_posts/{today}-{safe_title}.json', 'w', encoding='utf-8') as f:
        #    json.dump(content, f, ensure_ascii=False, indent=4)
        with open(f"_posts/{today}-{safe_title}.md", "w", encoding="utf-8") as f:
            blocks = get_blocks(page_id)
            markdown_content = ''.join([block_to_md(b) for b in blocks])
            f.write(markdown_content)
        print(f"✅ {safe_title} 페이지 내용 저장 완료!")
    else:
        print(f"❌ {safe_title} 페이지 로드 실패: {res.status_code}")

