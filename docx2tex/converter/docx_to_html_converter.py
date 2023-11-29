# docx_to_html_converter.py
import re
import os

from docx import Document
from pydocx import PyDocX
from bs4 import BeautifulSoup


def convert_docx(docx_file):
    html_content = PyDocX.to_html(docx_file)
    soup = BeautifulSoup(html_content, 'html.parser')
    html_content = soup.prettify()
    return html_content


def extract_images_from_docx(docx_file, output_folder):
    doc = Document(docx_file)

    # 创建输出文件夹（如果不存在）
    os.makedirs(output_folder, exist_ok=True)

    image_count = 0

    for rel in doc.part.rels.values():
        if "image" in rel.reltype:
            image_count += 1
            image_data = rel.target_part.blob
            # 生成文件名，例如 image_1.png, image_2.png, ...
            image_filename = os.path.join(output_folder, f"image_{image_count}.png")
            with open(image_filename, "wb") as img_file:
                img_file.write(image_data)

    return None


def replace_img_tags(html_content):
    content = BeautifulSoup(html_content, 'html.parser')

    # 找到所有的 <img> 标签
    img_tags = content.find_all('img')

    # 逐个替换 <img> 标签
    for img_count, img_tag in enumerate(img_tags, start=1):
        replacement = content.new_tag('span')
        replacement.string = r'\begin{figure}' + '\n' + r'\centering' + '\n' + \
            f'\\includegraphics[keepaspectratio]{{\\figure\\image_{img_count}.png}}' + \
            '\n' + r'\end{figure}'
        img_tag.replace_with(replacement)

    html_content = str(content)
    return html_content


def replace_span_tags(html_content):
    pattern1 = re.compile(r'<span style="color:(.*?)">(.*?)</span>', re.DOTALL)
    pattern2 = re.compile(r'<span.*?>(.*?)</span>', re.DOTALL)
    html_content = pattern1.sub(r'\\textcolor{\1}{\2}', html_content)
    html_content = pattern2.sub(r'\1', html_content)
    return html_content


def replace_hyperlink_tags(html_content):
    pattern1 = re.compile(r'<sup.*?>|</sup>')
    pattern2 = re.compile(r'<a href="#footnote(.*?)".*?>(.*?)</a>', re.DOTALL)
    pattern3 = re.compile(r'<a.*?>(.*?)</a>', re.DOTALL)
    html_content = pattern1.sub(r'', html_content)
    html_content = pattern2.sub(r'\\footnote{\2}', html_content)
    html_content = pattern3.sub(r'\1', html_content)
    return html_content


def replace_html_tags(html_content):
    pattern1 = re.compile(r'<html>|</html>|<body>|</body>')
    pattern2 = re.compile(r'<style>.*?</style>', re.DOTALL)
    pattern3 = re.compile(r'<meta .*?>', re.DOTALL)
    html_content = pattern1.sub(r'', html_content)
    html_content = pattern2.sub(r'', html_content)
    html_content = pattern3.sub(r'', html_content)
    return html_content


def convert_table(html_content):
    '''格式化列表环境'''
    pattern1 = re.compile(r'<table(.*?)>(\n\s*)<tr>', re.DOTALL)
    pattern2 = re.compile(r'<thead>(.*?)</tr>', re.DOTALL)
    pattern3 = re.compile(r'</thead>(\n\s*)<tr>')
    pattern4 = re.compile(r'</table>')

    html_content = pattern1.sub(r'<table\1>\2<thead>\n<tr>', html_content)
    html_content = pattern2.sub(r'<thead>\1</tr>\n</thead>\n', html_content)
    html_content = pattern3.sub(r'</thead>\1<tbody>\n<tr>', html_content)
    html_content = pattern4.sub(r'</tbody>\n</table>', html_content)

    def convert_td_to_th(html_content):
        # 使用 BeautifulSoup 解析 HTML
        soup = BeautifulSoup(html_content, 'html.parser')

        # 遍历所有的 <table> 标签
        for table_tag in soup.find_all('table'):
            # 将 <td> 替换为 <th>
            for td_tag in table_tag.find_all('td'):
                th_tag = soup.new_tag('th')
                th_tag.string = td_tag.get_text(strip=True)
                td_tag.replace_with(th_tag)

        # 将修改后的 HTML 转为字符串并返回
        return str(soup)
    
    html_content = convert_td_to_th(html_content)
    return html_content


def convert_docx_to_html(docx_file):
    html_content = convert_docx(docx_file)
    html_content = convert_table(html_content)
    html_content = replace_img_tags(html_content)
    html_content = replace_span_tags(html_content)
    html_content = replace_hyperlink_tags(html_content)
    html_content = replace_html_tags(html_content)
    return html_content
