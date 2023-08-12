import pandas as pd
from enum import Enum, auto
from PIL import Image as PILImage
from loguru import logger


# 定义 ContentType 枚举类，表示内容的类型
class ContentType(Enum):
    TEXT = auto()
    TABLE = auto()
    IMAGE = auto()


# 定义 Content 基类，表示通用的内容对象
class Content:
    def __init__(self, content_type, original, translation=None):
        self.content_type = content_type
        self.original = original
        self.translation = translation
        self.status = False

    def set_translation(self, translation, status):
        # 检查翻译内容的类型是否符合预期
        if not self.check_translation_type(translation):
            raise ValueError(f"Invalid translation type. Expected {self.content_type}, but got {type(translation)}")
        self.translation = translation
        self.status = status

    def check_translation_type(self, translation):
        # 检查翻译内容的类型是否符合预期
        if self.content_type == ContentType.TEXT and isinstance(translation, str):
            return True
        elif self.content_type == ContentType.TABLE and isinstance(translation, list):
            return True
        elif self.content_type == ContentType.IMAGE and isinstance(translation, PILImage.Image):
            return True
        return False


# 定义 TableContent 类，继承自 Content 类，表示表格内容
class TableContent(Content):
    def __init__(self, data, translation=None):
        df = pd.DataFrame(data)

        # 验证提取到的表格数据与 DataFrame 对象的行数和列数是否匹配
        if len(data) != len(df) or len(data[0]) != len(df.columns):
            raise ValueError(
                "The number of rows and columns in the extracted table data and DataFrame object do not match.")

        super().__init__(ContentType.TABLE, df)

    @logger.catch
    def set_translation(self, translation, status):
        try:
            if not isinstance(translation, str):
                raise ValueError(f"Invalid translation type. Expected str, but got {type(translation)}")

            logger.debug(translation)
            # 将字符串转换为列表形式的表格数据
            table_data = [row.strip().split() for row in translation.strip().split('\n')]
            logger.debug(table_data)
            # 从表格数据创建 DataFrame 对象
            translated_df = pd.DataFrame(table_data[1:], columns=table_data[0])
            logger.debug(translated_df)
            self.translation = translated_df
            self.status = status
        except Exception as e:
            logger.error(f"An error occurred during table translation: {e}")
            self.translation = None
            self.status = False

    def __str__(self):
        # 返回原始表格数据的字符串表示形式
        return self.original.to_string(header=False, index=False)

    def iter_items(self, translated=False):
        target_df = self.translation if translated else self.original
        for row_idx, row in target_df.iterrows():
            for col_idx, item in enumerate(row):
                yield (row_idx, col_idx, item)

    def update_item(self, row_idx, col_idx, new_value, translated=False):
        target_df = self.translation if translated else self.original
        target_df.at[row_idx, col_idx] = new_value

    def get_original_as_str(self):
        # 返回原始表格数据的字符串表示形式
        return self.original.to_string(header=False, index=False)
