from examModel import *
import re
# 用html
html_str_start = '''<!DOCTYPE html>
<html lang="zh">
<head>
    <meta charset="UTF-8">
    <style>
        .container {
            display: flex;
            flex-direction: row;
        }
        
        .quarterColumn {
            width: 25%;
        }
        .halfColumn {
            width: 50%
        }
        body {  
            font-family: Arial, sans-serif;  
            font-size: 14px;  
        }  
        p {  
            line-height: 190%;  
            margin-bottom: 0px;
            margin-top: 0px;
        } 
        div {
            margin-bottom: 5px; 
            margin-top: 2px;
        }
    </style>
</head>
<body>
'''
html_str_end = '''
</body>
</html>
'''
def createHTML(yanyu_questions, ziliao_material_dic, ziliao_questions, shuliang_questions, panduan_questions):
    content = ""
    for question in yanyu_questions:
        content += question.content
        content += optionString(question.options)
    content += '<p></p>'

    for index,material in ziliao_material_dic.items():
        content += material['content']
        filtered_list = list(filter(lambda x: index in x.materialIndexes , ziliao_questions)) 
        for question in filtered_list:
            content += question.content
            content += optionString(question.options)
    content += '<p></p>'

    for question in panduan_questions:
        content += question.content
        content += optionString(question.options)
    content += '<p></p>'

    for question in shuliang_questions:
        content += question.content
        content += optionString(question.options)

    html_path = 'diff_question.html'
    find_and_write(html_path, content)

    

def find_and_write(filepath, content):
    file = open(filepath, 'r+')
    file.truncate(0)
    file.write(html_str_start)
    file.write(content)
    file.write(html_str_end)
    file.close

def conver(match):
    if "https://" in match.group(1):
        return match.group()
    else:
        return match.group().replace(match.group(1), "https:" + match.group(1)) 

def optionString(options):
    for i in range(len(options)):
        if "<img" in options[i]:
            pattern = r"<img[\s\S]+?src=\"(//\S+)\""    
            result = re.sub(pattern, conver, options[i])
            options[i] = result


    if all(len(x)<=10 for x in options):
        return '''
    <div class="container">
        <div class="quarterColumn">A.{}</div>
        <div class="quarterColumn">B.{}</div>
        <div class="quarterColumn">C.{}</div>
        <div class="quarterColumn">D.{}</div>
    </div>
'''.format(options[0], options[1], options[2], options[3])
    elif all(len(x) <= 20 for x in options):
        return '''
    <div class="container">
        <div class="halfColumn">A.{}</div>
        <div class="halfColumn">B.{}</div>
    </div>
    <div class="container">
        <div class="halfColumn">C.{}</div>
        <div class="halfColumn">D.{}</div>
    </div>
'''.format(options[0], options[1], options[2], options[3])
    else:
        return '''
    <div>
    <p>A.{}</p>
    <p>B.{}</p>
    <p>C.{}</p>
    <p>D.{}</p>
    </div>
'''.format(options[0], options[1], options[2], options[3])
