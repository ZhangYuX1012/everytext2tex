# markdown_to_html_converter.py

import re
import markdown2


def replace_backslash(markdown_content):
    """保留md结构中的反斜杠"""
    pattern = re.compile(r'\\')
    markdown_content = pattern.sub(r'<backslash>',markdown_content)
    return markdown_content

def remain_underline_markdown(markdown_content):
    """保留Markdown中的下划线"""
    pattern = re.compile(r'_')
    markdown_content = pattern.sub(r'\\_', markdown_content)
    return markdown_content

def remain_shape_markdown(markdown_content):
    """保留Markdown中的井号"""
    pattern = re.compile(r'#')
    markdown_content = pattern.sub(r'\\#', markdown_content)
    return markdown_content

def remain_lstlisting(markdown_content):
    """保留Markdown中的代码块"""
    pattern = re.compile(r'\n```(.*?)\n(.*?)```', re.S)

    def convert_code_block(match):
        """将代码块转换为LaTeX代码块"""
        lang = match.group(1)
        code_block_content = match.group(2)
        tex_code_block = rf'<backslash>begin{{lstlisting}}[{lang}]' + \
            '\n' + code_block_content + '\n' + r'<backslash>end{lstlisting}' + '\n'
        return tex_code_block

    markdown_content = pattern.sub(convert_code_block, markdown_content)
    return markdown_content

def remain_markdown_content(markdown_content):
    """保留Markdown中的特殊语法"""
    markdown_content = remain_lstlisting(markdown_content)
    markdown_content = remain_underline_markdown(markdown_content)
    markdown_content = remain_shape_markdown(markdown_content)
    return markdown_content

def convert_section(markdown_content):
    """将Markdown中的标题转换为LaTeX的section"""
    pattern = re.compile(r'##\s+([^#]*?)\n')
    markdown_content = pattern.sub(r'\n\n<backslash>section{\1}\n\n', markdown_content)
    return markdown_content

def convert_part(markdown_content):
    """将Markdown中的标题转换为LaTeX的part"""
    pattern = re.compile(r'#\s+([^#]*?)\n')
    markdown_content = pattern.sub(r'\n\n<backslash>part{\1}\n\n', markdown_content)
    return markdown_content

def convert_subsection(markdown_content):
    """将Markdown中的标题转换为LaTeX的subsection"""
    pattern = re.compile(r'###\s+([^#]*?)\n')
    markdown_content = pattern.sub(r'\n\n<backslash>subsection{\1}\n\n', markdown_content)
    return markdown_content

def convert_subsubsection(markdown_content):
    """将Markdown中的标题转换为LaTeX的subsubsection"""
    pattern = re.compile(r'####\s+([^#]*?)\n')
    markdown_content = pattern.sub(r'\n\n<backslash>subsubsection{\1}\n\n', markdown_content)
    return markdown_content

def convert_lists(markdown_content):
    """将Markdown中的列表转换为LaTeX格式"""
    pattern = re.compile(r'\n((1\.)|(\-\s)|(\*\s))')
    markdown_content = pattern.sub(r'\n\n\1', markdown_content)
    return markdown_content

def convert_titles(markdown_content):
    """将Markdown中的所有标题转换为LaTeX格式"""
    markdown_content = convert_subsubsection(markdown_content)
    markdown_content = convert_subsection(markdown_content)
    markdown_content = convert_section(markdown_content)
    markdown_content = convert_part(markdown_content)
    return markdown_content

def convert_md_to_html(markdown_content):
    """将Markdown内容转换为HTML"""
    markdown_content = replace_backslash(markdown_content)
    markdown_content = convert_titles(markdown_content)
    markdown_content = convert_lists(markdown_content)
    markdown_content = remain_markdown_content(markdown_content)

    # 启用部分拓展
    extras = ["tables",  "def-list", "fenced-code-blocks"]

    # 将 Markdown 转换为 HTML
    html_content = markdown2.markdown(markdown_content, extras=extras)

    return html_content
