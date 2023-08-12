from ..model import GLMModel, OpenAIModel
from ..utils import ArgumentParser, ConfigLoader, LOG
from ..book import Book, Page, Content, ContentType, TableContent

if __name__ == "__main__":
    # 创建 OpenAIModel 实例
    model = OpenAIModel(model="gpt-3.5-turbo", api_key="your_openai_api_key")

    # 原始文本内容
    original = 'This dataset contains two test samples provided by ChatGPT, an AI language model by OpenAI. These samples include a markdown table and an English text passage, which can be used to test an English-to-Chinese translation software supporting both text and table formats.'

    # 创建内容对象
    text_content = Content(content_type=ContentType.TEXT, original=original)

    # 使用模型进行翻译提示生成
    target_language = '日文'
    prompt = model.translate_prompt(text_content, target_language)

    # 打印翻译提示
    LOG.info('提示语为：' + prompt)

    # 发送翻译请求并获取结果
    translation, status = model.make_request(prompt)

    # 打印翻译结果
    LOG.info('翻译后为：' + translation)
