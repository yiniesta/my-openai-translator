from typing import Optional
from model import Model
from translator.pdf_parser import PDFParser
from translator.writer import Writer
from utils import LOG


class PDFTranslator:
    def __init__(self, model: Model):
        self.model = model
        self.pdf_parser = PDFParser()
        self.writer = Writer()

    def translate_pdf(self, pdf_file_path: str, file_format: str = 'PDF', target_language: str = '中文',
                      output_file_path: str = None, pages: Optional[int] = None):
        # 解析PDF文件并构建Book对象
        self.book = self.pdf_parser.parse_pdf(pdf_file_path, pages)

        # 遍历每一页的内容进行翻译
        for page_idx, page in enumerate(self.book.pages):
            for content_idx, content in enumerate(page.contents):
                # 生成翻译提示语句
                prompt = self.model.translate_prompt(content, target_language)
                LOG.debug(prompt)

                # 如果提示为空，则继续下一个内容的翻译
                if not prompt:
                    continue

                # 发送翻译请求并获取结果
                translation, status = self.model.make_request(prompt)
                LOG.info(translation)

                # 直接在Book对象中更新内容的翻译结果
                self.book.pages[page_idx].contents[content_idx].set_translation(translation, status)

        # 将翻译后的Book保存为输出文件
        self.writer.save_translated_book(self.book, output_file_path, file_format)
