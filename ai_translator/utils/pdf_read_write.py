import PyPDF2

# 打开原始PDF文件
with open("D:\\github\\openai-translator\\tests\\The_Old_Man_of_the_Sea.pdf", "rb") as file:
    # 创建一个PDF Reader对象
    pdf_reader = PyPDF2.PdfReader(file)

    # 创建一个新的PDF Writer对象
    pdf_writer = PyPDF2.PdfWriter()

    # 遍历前5页
    for page_num in range(5):
        # 获取当前页
        page = pdf_reader.pages[page_num]

        # 将当前页添加到新的PDF Writer对象中
        pdf_writer.add_page(page)

    # 创建一个新的PDF文件
    with open("D:\\github\\openai-translator\\tests\\first_5_page.pdf", "wb") as output_file:
        # 将新的PDF内容写入文件
        pdf_writer.write(output_file)
