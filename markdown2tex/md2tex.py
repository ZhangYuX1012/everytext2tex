# md2tex.py

import os

from template.template_utils import copy_template
from converter.markdown_to_html_converter import convert_md_to_html
from converter.html_to_tex_converter_md import convert_html_to_tex
from template.package import package_list
from template.beginning import beginning

def read_file(file_path):
    """读取文件内容"""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    except FileNotFoundError:
        print(f"错误：文件 '{file_path}' 未找到。")
        return None
    except IOError as e:
        print(f"读取 '{file_path}' 时出错：{e}")
        return None


def write_file(file_path, content):
    """写入文件内容"""
    try:
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(content)
        print(f"写入成功。文件已写入 '{file_path}'。")
    except IOError as e:
        print(f"写入 '{file_path}' 时出错：{e}")


def process_markdown_file(output_file, template_folder, output_folder, template_name=None):
    """处理Markdown文件"""
    if template_name is None:
        template_name = input("请输入模板名称（不输入模板名称即不调用模板）：")

    # 复制选择的模板
    template_copied = copy_template(
        template_folder, output_folder, template_name)
    if not template_copied:
        print("错误：无法复制模板。程序退出。")
        return

    # 获取Markdown文件路径
    input_file = input("请输入Markdown文件路径：")

    markdown_content = read_file(input_file)
    if markdown_content is None:
        return

    html_content = convert_md_to_html(markdown_content)
    tex_content = convert_html_to_tex(html_content)

    full_tex_content = generate_tex_template_content(template_name, tex_content)

    write_file(output_file, full_tex_content)


def generate_tex_template_content(template_name, tex_content):
    """生成完整的TeX模板"""
    setting_tex_code = beginning.setting_content[template_name]
    beginning_tex_code = beginning.beginning_content[template_name]
    package_tex_code = package_list.package_content['base'] + package_list.package_content[template_name]
    end_tex_code = '\n\\end{document}'

    return setting_tex_code + package_tex_code + beginning_tex_code + '\n' + tex_content + '\n' + end_tex_code


if __name__ == "__main__":
    default_output_folder = "\\path" # 换成你自己的输出路径
    default_template_folder = "\\path" # 换成你自己的模板路径

    # 创建输出文件夹
    if not os.path.exists(default_output_folder):
        os.makedirs(default_output_folder)

    output_tex_file = os.path.join(default_output_folder, "output.tex") #换成你想要的输出名称
    process_markdown_file(
        output_tex_file, default_template_folder, default_output_folder)
