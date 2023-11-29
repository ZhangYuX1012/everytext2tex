# html_to_tex_converter_md.py

import re
import html
from bs4 import BeautifulSoup


def convert_textbf_to_tex(html_content):
    """将HTML中的<strong>标签转换为LaTeX的textbf命令"""
    pattern = re.compile(r'<strong>(.*?)</strong>')
    tex_content = pattern.sub(r'\\textbf{\1}', html_content)
    return tex_content


def convert_delete_to_tex(html_content):
    """将HTML中的删除线标签转换为LaTeX的sout命令"""
    pattern = re.compile(r'~~([^~].*?[^~])~~')
    tex_content = pattern.sub(r'\\sout{\1}', html_content)
    return tex_content


def convert_textit_to_tex(html_content):
    """将HTML中的<em>标签转换为LaTeX的textit命令"""
    pattern = re.compile(r'<em>(.*?)</em>')
    tex_content = pattern.sub(r'\\textit{\1}', html_content)
    return tex_content


def convert_quote_to_tex(html_content):
    """将HTML中的<blockquote>标签转换为LaTeX的quote环境"""
    pattern = re.compile(r'<blockquote>(.*?)</blockquote>', re.DOTALL)
    tex_content = pattern.sub(
        r'\\begin{quote}\n\1\\end{quote}\n', html_content)
    return tex_content


def convert_fontcolor_to_tex(html_content):
    """将HTML中的<font>标签中的颜色属性转换为LaTeX的textcolor命令"""
    pattern1 = re.compile(r'<font style="color: (.*?);">(.*?)</span>')
    pattern2 = re.compile(r'<font color="(.*?)">(.*?)</font>')
    tex_content = pattern1.sub(r'\\textcolor{\1}{\2}', html_content)
    tex_content = pattern2.sub(r'\\textcolor{\1}{\2}', tex_content)
    return tex_content


def convert_fontsize_to_tex(html_content):
    """将HTML中的<font>标签中的大小属性转换为LaTeX的字体大小命令"""
    pattern1 = re.compile(r'<font size="(\d+)">(.*?)</font>', re.DOTALL)
    pattern2 = re.compile(r'<font size="(\d+)">(.*?)<font>', re.DOTALL)
    size_mapping = {
        '0': '\\tiny',
        '1': '\\footnotesize',
        '2': '\\small',
        '3': '',
        '4': '\\large',
        '5': '\\Large',
        '6': '\\Large',
        '7': '\\LARGE',
        '8': '\\LARGE',
        '9': '\\huge',
        '10': '\\Huge',
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
    pattern = re.compile(r'(.*?)<center>(.*?)</center>(.*?)')
    tex_content = pattern.sub(
        r'\\begin{centering}\n\1 \2 \3\n\\end{centering}', html_content)
    return tex_content


def convert_orderedlist_to_tex(html_content):
    """将HTML中的有序列表标签转换为LaTeX的enumerate环境"""
    pattern = re.compile(r'<ol>(.*?)</ol>', re.DOTALL)
    tex_content = pattern.sub(
        r'\\begin{enumerate}\n\1\n\\end{enumerate}', html_content)
    return tex_content


def convert_list_to_tex(html_content):
    """将HTML中的无序列表标签转换为LaTeX的itemize环境"""
    pattern = re.compile(r'<ul>(.*?)</ul>', re.DOTALL)
    tex_content = pattern.sub(
        r'\\begin{itemize}\n\1\n\\end{itemize}', html_content)
    return tex_content


def convert_pictures_to_tex(html_content):
    """将HTML中的图片标签转换为LaTeX的figure环境"""
    pattern = re.compile(
        r'<img src="(.*?)"\s*alt="(.*?)"\s*(.*?)/>', re.DOTALL)
    picture = r'\\begin{figure}\n\\centering\n\\includegraphics[keepaspectratio]{\1}\n\\caption{\2}\n\\end{figure}'
    tex_content = pattern.sub(rf'{picture}', html_content)
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
        r'\\begin{table}[!htbp]\n%\\caption{}\n\\centering\n<table>', html_content)
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
        tabular = rf'\\begin{{tabular}}{{*{th_count}{{c}}}}\n\\toprule\n{content}'
        tex_content = pattern.sub(tabular, html_content, count=1)
    return tex_content


def convert_table_head(html_content):
    """将HTML中的<th>标签转换为LaTeX的表头命令"""
    pattern1 = re.compile(r'<th.*?>(.*?)</th>\n\s*(?!</tr>)')
    pattern2 = re.compile(r'<th.*?>(.*?)</th>\n\s*</tr>')
    tex_content = pattern1.sub(r'\1 & ', html_content)
    tex_content = pattern2.sub(r'\1 \\\\ \n', tex_content)
    return tex_content


def convert_table_content(html_content):
    """将HTML中的<td>标签转换为LaTeX的表格内容命令"""
    pattern1 = re.compile(r'<td.*?>(.*?)</td>\n\s*(?!</tr>)')
    pattern2 = re.compile(r'<td.*?>(.*?)</td>\n\s*</tr>')
    tex_content = pattern1.sub(r'\1 & ', html_content)
    tex_content = pattern2.sub(r'\1 \\\\ \n', tex_content)
    return tex_content


def convert_midrule(html_content):
    """将HTML中的<tbody>标签转换为LaTeX的midrule命令"""
    pattern = re.compile(r'<tbody>')
    tex_content = pattern.sub(r'\n\\midrule\n', html_content)
    return tex_content


def convert_bottomrule(html_content):
    """将HTML中的</tbody>标签转换为LaTeX的bottomrule命令"""
    pattern = re.compile(r'</tbody>')
    tex_content = pattern.sub(r'\n\\bottomrule\n', html_content)
    return tex_content


def convert_table_end(html_content):
    """将HTML中的</table>标签转换为LaTeX的tabular和table命令"""
    pattern = re.compile(r'</table>')
    tex_content = pattern.sub(r'\n\\end{tabular}\n\\end{table}', html_content)
    return tex_content


def convert_table_to_tex(html_content):
    """将HTML中的表格相关标签转换为LaTeX"""
    tex_content = convert_table_top(html_content)
    tex_content = convert_table_toprule(tex_content)
    tex_content = convert_midrule(tex_content)
    tex_content = convert_bottomrule(tex_content)
    tex_content = convert_table_head(tex_content)
    tex_content = convert_table_content(tex_content)
    tex_content = convert_table_end(tex_content)
    return tex_content


def convert_html_tags_to_tex(html_content):
    """将HTML内容转换为LaTeX"""
    tex_content = re.sub(
        r'<li>', r'    \\item ', html_content)
    tex_content = re.sub(
        r'</li>|<p>|</p>', '', tex_content)
    tex_content = re.sub(
        r'</ul>|</ol>|<div>|</div>|<br />|<th>|</tr>|<tr>', '', tex_content)
    tex_content = re.sub(r'<ol start="\d+">', '', tex_content)
    tex_content = re.sub(r'<thead>|</thead>|<table.*?>', '', tex_content)
    tex_content = re.sub(r'([^\\])\\\s*\n', r'\1\\\\\n', tex_content)
    tex_content = re.sub(r'<em>|</em>', '*', tex_content)
    return tex_content


def convert_html_to_tex(html_content):
    tex_content = convert_quote_to_tex(html_content)
    tex_content = convert_textbf_to_tex(tex_content)
    tex_content = convert_textit_to_tex(tex_content)
    tex_content = convert_delete_to_tex(tex_content)
    tex_content = convert_centering_to_tex(tex_content)
    tex_content = convert_fontsize_to_tex(tex_content)
    tex_content = convert_fontcolor_to_tex(tex_content)
    tex_content = convert_lists_to_tex(tex_content)
    tex_content = convert_table_to_tex(tex_content)
    tex_content = convert_pictures_to_tex(tex_content)
    tex_content = convert_html_tags_to_tex(tex_content)
    tex_content = html.unescape(tex_content)
    return tex_content
