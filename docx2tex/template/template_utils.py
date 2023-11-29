# template_utils.py

import os

def read_template(template_folder, template_name):
    """读取模板文件内容"""
    template_file = os.path.join(template_folder, f'{template_name}.cls')
    try:
        with open(template_file, 'r', encoding='utf-8') as file:
            template_content = file.read()
            return template_content
    except FileNotFoundError:
        print(f"错误: 未找到模板文件 '{template_name}.cls' .")
        return None
    except IOError as e:
        print(f"读取模板文件时出错：{e}")
        return None

def copy_template(template_folder, output_folder, template_name):
    """复制模板文件到输出文件夹"""
    template_content = read_template(template_folder, template_name)
    if template_content is not None:
        output_file = os.path.join(output_folder, f'{template_name}.cls')
        try:
            with open(output_file, 'w', encoding='utf-8') as file:
                file.write(template_content)
            print(f"模板文件 '{template_name}.cls' 复制到 '{output_folder}'.")
            return True
        except IOError as e:
            print(f"复制模板文件时出错: {e}")
            return False
    else:
        return False
