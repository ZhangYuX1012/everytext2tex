# html_to_tex_converter_docx.py

import re
import html
from bs4 import BeautifulSoup


def convert_section_to_tex(html_content):
    """将html中的标题转换为LaTeX的section"""
    pattern = re.compile(r'<h2>(.*?)</h2>', re.DOTALL)
    tex_content = pattern.sub(r'\n\n<backslash>section{\1}\n\n', html_content)
    return tex_content


def convert_part_to_tex(html_content):
    """将html中的标题转换为LaTeX的part"""
    pattern = re.compile(r'<h1>(.*?)</h1>', re.DOTALL)
    tex_content = pattern.sub(r'\n\n<backslash>part{\1}\n\n', html_content)
    return tex_content


def convert_subsection_to_tex(html_content):
    """将html中的标题转换为LaTeX的subsection"""
    pattern = re.compile(r'<h3>(.*?)</h3>', re.DOTALL)
    tex_content = pattern.sub(
        r'\n\n<backslash>subsection{\1}\n\n', html_content)
    return tex_content


def convert_subsubsection_to_tex(html_content):
    """将html中的标题转换为LaTeX的subsubsection"""
    pattern = re.compile(r'<h4>(.*?)</h4>', re.DOTALL)
    tex_content = pattern.sub(
        r'\n\n<backslash>subsubsection{\1}\n\n', html_content)
    return tex_content


def convert_textbf_to_tex(html_content):
    """将HTML中的<strong>标签转换为LaTeX的textbf命令"""
    pattern = re.compile(r'<strong>(.*?)</strong>', re.DOTALL)
    tex_content = pattern.sub(r'<backslash>textbf{\1}', html_content)
    return tex_content


def convert_textit_to_tex(html_content):
    """将HTML中的<em>标签转换为LaTeX的textit命令"""
    pattern = re.compile(r'<em>(.*?)</em>', re.DOTALL)
    tex_content = pattern.sub(r'<backslash>textit{\1}', html_content)
    return tex_content


def convert_quote_to_tex(html_content):
    """将HTML中的<blockquote>标签转换为LaTeX的quote环境"""
    pattern = re.compile(r'<blockquote>(.*?)</blockquote>', re.DOTALL)
    tex_content = pattern.sub(
        r'<backslash>begin{quote}\n\1<backslash>end{quote}\n', html_content)
    return tex_content


def convert_fontcolor_to_tex(html_content):
    """将HTML中的<font>标签中的颜色属性转换为LaTeX的textcolor命令"""
    pattern1 = re.compile(
        r'<font style="color: (.*?);">(.*?)</span>', re.DOTALL)
    pattern2 = re.compile(r'<font color="(.*?)">(.*?)</font>', re.DOTALL)
    tex_content = pattern1.sub(r'<backslash>textcolor{\1}{\2}', html_content)
    tex_content = pattern2.sub(r'<backslash>textcolor{\1}{\2}', tex_content)
    return tex_content


def convert_fontsize_to_tex(html_content):
    """将HTML中的<font>标签中的大小属性转换为LaTeX的字体大小命令"""
    pattern1 = re.compile(r'<font size="(\d+)">(.*?)</font>', re.DOTALL)
    pattern2 = re.compile(r'<font size="(\d+)">(.*?)<font>', re.DOTALL)
    size_mapping = {
        '0': '<backslash>tiny',
        '1': '<backslash>footnotesize',
        '2': '<backslash>small',
        '3': '',
        '4': '<backslash>large',
        '5': '<backslash>Large',
        '6': '<backslash>Large',
        '7': '<backslash>LARGE',
        '8': '<backslash>LARGE',
        '9': '<backslash>huge',
        '10': '<backslash>Huge',
    }

    def convert_size(match):
        size = match.group(1)
        content = match.group(2)
        size_command = size_mapping.get(size, '')
        return f'{size_command}{{{content}}}'

    tex_content = pattern1.sub(convert_size, html_content)
    tex_content = pattern2.sub(convert_size, tex_content)
    return tex_content


def convert_centering_to_tex(html_content):
    """将HTML中的<center>标签转换为LaTeX的centering环境"""
    pattern = re.compile(r'(.*?)<center>(.*?)</center>(.*?)', re.DOTALL)
    tex_content = pattern.sub(
        r'<backslash>begin{centering}\n\1 \2 \3\n<backslash>end{centering}', html_content)
    return tex_content


def convert_orderedlist_to_tex(html_content):
    """将HTML中的有序列表标签转换为LaTeX的enumerate环境"""
    pattern = re.compile(r'<ol.*?>(.*?)</ol>', re.DOTALL)
    tex_content = pattern.sub(
        r'<backslash>begin{enumerate}\n\1\n<backslash>end{enumerate}', html_content)
    return tex_content


def convert_list_to_tex(html_content):
    """将HTML中的无序列表标签转换为LaTeX的itemize环境"""
    pattern = re.compile(r'<ul>(.*?)</ul>', re.DOTALL)
    tex_content = pattern.sub(
        r'<backslash>begin{itemize}\n\1\n<backslash>end{itemize}', html_content)
    return tex_content


def convert_lists_to_tex(html_content):
    """将HTML中的有序列表和无序列表标签转换为LaTeX格式"""
    tex_content = convert_orderedlist_to_tex(html_content)
    tex_content = convert_list_to_tex(tex_content)
    return tex_content


def convert_table_top(html_content):
    """将HTML中的<table>标签转换为LaTeX的table环境"""
    pattern = re.compile(r'<table.*?>')
    tex_content = pattern.sub(
        r'<backslash>begin{table}[!htbp]\n%<backslash>caption{}\n<backslash>centering\n<table>', html_content)
    return tex_content


def convert_table_toprule(html_content):
    """将HTML中的<thead>标签转换为LaTeX的toprule命令"""
    tex_content = html_content  # 初始化 tex_content
    pattern = re.compile(r'<table>\s*(.*?)\s*</thead>', re.DOTALL)
    matches = pattern.findall(html_content)
    for match in matches:
        content = match
        soup = BeautifulSoup(content, 'html.parser')
        thead_th_tags = soup.select('thead th')
        th_count = sum(str(th).count('</th>') for th in thead_th_tags)
        tabular = rf'<backslash>begin{{tabular}}{{*{th_count}{{c}}}}\n<backslash>toprule\n{content}'
        tex_content = pattern.sub(tabular, html_content, count=1)
    return tex_content


def convert_table_head(html_content):
    """将HTML中的<th>标签转换为LaTeX的表头命令"""
    pattern1 = re.compile(r'<th.*?>(.*?)</th>\n\s*(?!</tr>)')
    pattern2 = re.compile(r'<th.*?>(.*?)</th>\n\s*</tr>')
    tex_content = pattern1.sub(r'\1 & ', html_content)
    tex_content = pattern2.sub(r'\1 <backslash><backslash> \n', tex_content)
    return tex_content


def convert_midrule(html_content):
    """将HTML中的<tbody>标签转换为LaTeX的midrule命令"""
    pattern = re.compile(r'<tbody>')
    tex_content = pattern.sub(r'\n<backslash>midrule\n', html_content)
    return tex_content


def convert_bottomrule(html_content):
    """将HTML中的</tbody>标签转换为LaTeX的bottomrule命令"""
    pattern = re.compile(r'</tbody>')
    tex_content = pattern.sub(r'\n<backslash>bottomrule\n', html_content)
    return tex_content


def convert_table_end(html_content):
    """将HTML中的</table>标签转换为LaTeX的tabular和table命令"""
    pattern = re.compile(r'</table>')
    tex_content = pattern.sub(
        r'\n<backslash>end{tabular}\n<backslash>end{table}', html_content)
    return tex_content


def convert_table_to_tex(html_content):
    """将HTML中的表格相关标签转换为LaTeX"""
    tex_content = convert_table_top(html_content)
    tex_content = convert_table_toprule(tex_content)
    tex_content = convert_midrule(tex_content)
    tex_content = convert_bottomrule(tex_content)
    tex_content = convert_table_head(tex_content)
    tex_content = convert_table_end(tex_content)
    return tex_content


def convert_html_tags_to_tex(html_content):
    """将HTML内容转换为LaTeX"""
    tex_content = re.sub(
        r'<li>', r'    <backslash>item ', html_content)
    tex_content = re.sub(
        r'</li>|<p>|</p>', '', tex_content)
    tex_content = re.sub(
        r'</thead>|<thead>|<table.*?>|<br/>|<span>|</span>|</head>|<head>|</ul>|</ol>|<div>|</div>|<br />|<th>|</tr>|<tr>|<hr/>', '', tex_content)
    tex_content = re.sub(r'<ol.*?>', '', tex_content)
    tex_content = re.sub(r'<thead>', '', tex_content)
    tex_content = re.sub(r'([^<backslash>])<backslash>\s*\n',
                         r'\1<backslash><backslash>\n', tex_content)
    tex_content = re.sub(r'<em>|</em>', '*', tex_content)
    return tex_content


def return_backslash(html_content):
    """还原反斜杠"""
    pattern = re.compile(r'<backslash>')
    tex_content = pattern.sub(r'\\', html_content)
    return tex_content


def remove_multiple_blank_lines(html_content):
    # 使用正则表达式匹配两个及以上的空行，并替换为空行
    tex_content = re.sub(r'\n\s*\n\s*\n*', '\n', html_content)
    return tex_content


def convert_html_to_tex(html_content):
    tex_content = convert_quote_to_tex(html_content)
    tex_content = convert_part_to_tex(tex_content)
    tex_content = convert_section_to_tex(tex_content)
    tex_content = convert_subsection_to_tex(tex_content)
    tex_content = convert_subsubsection_to_tex(tex_content)
    tex_content = convert_textbf_to_tex(tex_content)
    tex_content = convert_textit_to_tex(tex_content)
    tex_content = convert_centering_to_tex(tex_content)
    tex_content = convert_fontsize_to_tex(tex_content)
    tex_content = convert_fontcolor_to_tex(tex_content)
    tex_content = convert_lists_to_tex(tex_content)
    tex_content = convert_table_to_tex(tex_content)
    tex_content = convert_html_tags_to_tex(tex_content)
    tex_content = return_backslash(tex_content)
    tex_content = html.unescape(tex_content)
    tex_content = remove_multiple_blank_lines(tex_content)
    return tex_content
