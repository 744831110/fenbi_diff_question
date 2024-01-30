import json

class Exercise:
    def __init__(self, request_content):
        request_dic = json.loads(request_content)
        sheet = request_dic['sheet']
        chapters = sheet['chapters']
        question_num = 0
        contain_ketui = False
        for chapter in chapters:
            if chapter['name'] == '言语理解与表达':
                self.yanyu_start_num = question_num
                question_num += int(chapter['questionCount'])
                self.yanyu_end_num = question_num
            elif chapter['name'] == '资料分析':
                self.ziliao_start_num = question_num
                question_num += int(chapter['questionCount'])
                self.ziliao_end_num = question_num
            elif chapter['name'] == '科学推理':
                contain_ketui = True
                self.ketui_start_num = question_num
                question_num += int(chapter['questionCount'])
                self.ketui_end_num = question_num
            elif chapter['name'] == '数量关系':
                self.shuliang_start_num = question_num
                question_num += int(chapter['questionCount'])
                self.shuliang_end_num = question_num
            else:
                question_num += int(chapter['questionCount'])
        self.questionIds = sheet['questionIds']
        self.yanyu_questionIds = self.questionIds[self.yanyu_start_num: self.yanyu_end_num]
        self.ziliao_questionIds = self.questionIds[self.ziliao_start_num: self.ziliao_end_num]
        self.shuliang_questionIds = self.questionIds[self.shuliang_start_num: self.shuliang_end_num]
        self.ketui_questionIds = self.questionIds[self.ketui_start_num: self.ketui_end_num] if contain_ketui else []

class ExerciseQuestions:
    def __init__(self, request_content):
        request_dic = json.loads(request_content)
        self.materials = request_dic['materials']
        question_list = request_dic['questions']
        self.questions = {}
        for i in range(len(question_list)):
            question = Question(question_list[i], i+1)
            self.questions[question.id] = question

class Question:
    def __init__(self, dic, question_num):
        self.id = str(dic['id'])
        self.content = dic['content']
        # 只要单选题
        if dic['type'] == 1:
            self.options = dic['accessories'][0]['options']
            self.question_num = question_num
            self.content = self.content[:3] + str(question_num) + '.' + self.content[3:]
            if dic['materialIndexes']:
                self.materialIndexes = dic['materialIndexes']
            else:
                self.materialIndexes = None
    