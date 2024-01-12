from examModel import *
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
            font-size: 16px;  
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
def createHTML(yanyu_questions, ziliao_material_dic, ziliao_question):
    content = ""
    for question in yanyu_questions:
        content += question.content
        content += optionString(question.options)
    content += '<p></p>'
    for index,material in ziliao_material_dic.items():
        print(material)
        content += material['content']
        filtered_list = list(filter(lambda x: index in x.materialIndexes , ziliao_question)) 
        for question in filtered_list:
            content += question.content
            content += optionString(question.options)
    html_path = '/Users/chenqian/Desktop/陈谦/python/request_fenbi_exam_diff/diff_question.html'
    find_and_write(html_path, content)

    

def find_and_write(filepath, content):
    file = open(filepath, 'r+')
    file.truncate(0)
    file.write(html_str_start)
    file.write(content)
    file.write(html_str_end)
    file.close

def optionString(options):
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
