import requests
from examModel import *
from createHTML import *

# 获取试卷的整体信息，为了获取questionIds 下面三个自己填入
common_exercises_id = '2516477029'
gd_exercises_id = '2516562768'
cookie = ''

# 后跟exercisesid
fenbi_exercises_base_url = "https://tiku.fenbi.com/api/xingce/exercises/"
exercise_url_paramter_string = "?app=web&kav=100&av=100&hav=100&version=3.0.0.0"
headers = {'Accept-Language': 'zh-CN', 'Cookie': cookie}

fenbi_exercises_url = fenbi_exercises_base_url + common_exercises_id + exercise_url_paramter_string
response = requests.get(fenbi_exercises_url, headers=headers)
common_exercises_content = response.text
common_exercises = Exercise(common_exercises_content)

fenbi_exercises_url = fenbi_exercises_base_url + gd_exercises_id + exercise_url_paramter_string
response = requests.get(fenbi_exercises_url, headers=headers)
gd_exercises_content = response.text
gd_exercises = Exercise(gd_exercises_content)
# print("questionids")
# print(common_exercises.yanyu_questionIds)
# print(gd_exercises.yanyu_questionIds)


# 获取通用试卷的题目
question_base_url = "https://tiku.fenbi.com/api/xingce/universal/auth/questions?"
#最后直接加exerciseid
question_url_paramter_string = 'type=0&app=web&kav=100&av=100&hav=100&version=3.0.0.0&id='
question_url = question_base_url + question_url_paramter_string + common_exercises_id
response = requests.get(question_url, headers=headers)
common_question_content = response.text
common_exercise_question = ExerciseQuestions(common_question_content)
# print("----materials----");
# print(common_exercise_question.materials)
# print("----questions----");
# print(common_exercise_question.questions)

# 对比言语题
yanyu_fliter_list = list(common_exercises.yanyu_questionIds)
# print(yanyu_fliter_list)
for questionid in gd_exercises.yanyu_questionIds:
    if questionid in yanyu_fliter_list:
        yanyu_fliter_list.remove(questionid)
yanyu_diff_questions = [common_exercise_question.questions[str(x)] for x in yanyu_fliter_list]
# print(yanyu_diff_questions)

# 资料获取到差异题，然后获取相同的materialindex。先输出material再输出相应的题目
ziliao_fliter_list = list(common_exercises.ziliao_questionIds)
for questionid in gd_exercises.ziliao_questionIds:
    if questionid in ziliao_fliter_list:
        ziliao_fliter_list.remove(questionid)
ziliao_diff_question = [common_exercise_question.questions[str(x)] for x in ziliao_fliter_list]
ziliao_material_index_set = set()
for question in ziliao_diff_question:
    ziliao_material_index_set.update(question.materialIndexes)
ziliao_material_dic = {}
for index in ziliao_material_index_set:
    ziliao_material_dic[index] = common_exercise_question.materials[index]

# 用html做出试卷，并转成pdf，最后输出到文件夹中
createHTML(yanyu_diff_questions, ziliao_material_dic, ziliao_diff_question)
