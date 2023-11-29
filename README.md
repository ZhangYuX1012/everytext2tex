# everytext2tex
A Simple Tool for Markdown and DocX to Latex Conversion

## 依赖环境
- 使用 ***md2tex*** 前需要安装*markdown2*库
- 使用 ***docx2tex*** 前需要安装*pydocx*和*python-docx*库
  
### 注： 
如果使用docx2tex时报错 ***AttributeError: module 'collections' has no attribute 'Hashable'***

则需要找到源码文件***memorize.py***，将其中的***import collections***改成***import collections.abc***

并将***if not isinstance(args, collections.Hashable):*** 改成 ***if not isinstance(args, collections.abc.Hashable):***

## 使用方法
打开python文件将md2tex或者docx2tex中的相关路径改成你自己设置的路径
- **md2tex：** 使用前要准备好*md文件路径，模板路径* 
- **docx2tex：** 使用前要准备好*docx文件路径，模板路径*

*elegant_templates*文件夹里附带了几个常用的LaTeX模板，如果你想添加属于自己的模板和相应的宏包设置，直接在*template*中的*beginning*和*package*文件中更改相应的字典即可

## 可以转换的格式
- **md2tex：** 见example 
- **docx2tex:** 列表、表格、图片、文本内容、加粗、斜体等

***注意：*** 
1. 在进行md转至tex时，markdown源文件的格式要遵守md2tex中的example格式，否则可能会出现格式错误
2. docx转tex之前最好确保图片格式均为png，否则转至tex之后会出现图片格式错误
3. docx转tex之前最后使用mathtype将所有公式转成latex格式，否则可能会出现无法识别或把公式识别成图片

***todo:*** 
1. 自动化docx公式转化成latex格式
2. 完善docx中更多格式的转化

