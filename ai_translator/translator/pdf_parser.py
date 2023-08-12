import pdfplumber
from typing import Optional
from book import Book, Page, Content, ContentType, TableContent
from translator.exceptions import PageOutOfRangeException
from utils import LOG

class PDFParser:
    def __init__(self):
        pass

    def parse_pdf(self, pdf_file_path: str, pages: Optional[int] = None) -> Book:
        # 创建一个 Book 对象，用于存储解析后的 PDF 内容
        book = Book(pdf_file_path)

        # 使用 pdfplumber 打开 PDF 文件
        with pdfplumber.open(pdf_file_path) as pdf:
            # 检查页数是否超出范围
            if pages is not None and pages > len(pdf.pages):
                raise PageOutOfRangeException(len(pdf.pages), pages)

            # 确定要解析的页数范围
            if pages is None:
                pages_to_parse = pdf.pages
            else:
                pages_to_parse = pdf.pages[:pages]

            # 遍历要解析的每一页
            for pdf_page in pages_to_parse:
                # 创建一个 Page 对象，用于存储单个页面的内容
                page = Page()

                # 存储原始文本内容
                raw_text = pdf_page.extract_text()

                # 提取表格数据
                tables = pdf_page.extract_tables()

                # 从原始文本中删除每个单元格的内容
                for table_data in tables:
                    for row in table_data:
                        for cell in row:
                            raw_text = raw_text.replace(cell, "", 1)

                # 提取图片
                images = pdf_page.images
                for image in images:
                    # 先把它保存在本地，并定义唯一的名称，然后写入时根据名称找到图片写入
                    print(image)
                    img_content = Content(content_type=ContentType.IMAGE, original=image)
                    page.add_content(img_content)

                # 处理文本
                if raw_text:
                    # 移除空行和前导/尾随空格
                    raw_text_lines = raw_text.splitlines()
                    cleaned_raw_text_lines = [line.strip() for line in raw_text_lines if line.strip()]
                    cleaned_raw_text = "\n".join(cleaned_raw_text_lines)

                    # 创建 Content 对象并添加到页面
                    text_content = Content(content_type=ContentType.TEXT, original=cleaned_raw_text)
                    page.add_content(text_content)
                    LOG.debug(f"[raw_text]\n {cleaned_raw_text}")

                # 处理表格
                if tables:
                    # 创建 TableContent 对象并添加到页面
                    table = TableContent(tables)
                    page.add_content(table)
                    LOG.debug(f"[table]\n{table}")

                # 将页面添加到 Book 对象中
                book.add_page(page)

        # 返回解析后的 Book 对象
        return book
