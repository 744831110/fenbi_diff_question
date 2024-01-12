import requests
from examModel import *
from createHTML import *

# 获取试卷的整体信息，为了获取questionIds 下面三个试卷id和cookie需填入
common_exercises_id = ''
gd_exercises_id = ''
# 乡镇，用来获取科学推理差异题
gd_xiangzhen_exercises_id = ''
cookie = ''
headers = {'Accept-Language': 'zh-CN', 'Cookie': cookie}

def createExercises(exercise_id):
    fenbi_exercises_base_url = "https://tiku.fenbi.com/api/xingce/exercises/"
    exercise_url_paramter_string = "?app=web&kav=100&av=100&hav=100&version=3.0.0.0"
    fenbi_exercises_url = fenbi_exercises_base_url + exercise_id + exercise_url_paramter_string
    response = requests.get(fenbi_exercises_url, headers=headers)
    common_exercises_content = response.text
    return Exercise(common_exercises_content)

common_exercises = createExercises(common_exercises_id)

gd_exercises = createExercises(gd_exercises_id)

gd_xiangzhen_exercises = createExercises(gd_xiangzhen_exercises_id)


# 获取通用试卷的题目
question_base_url = "https://tiku.fenbi.com/api/xingce/universal/auth/questions?"
#最后直接加exerciseid
question_url_paramter_string = 'type=0&app=web&kav=100&av=100&hav=100&version=3.0.0.0&id='
question_url = question_base_url + question_url_paramter_string + common_exercises_id
response = requests.get(question_url, headers=headers)
common_question_content = response.text
common_exercise_question = ExerciseQuestions(common_question_content)

question_url = question_base_url + question_url_paramter_string + gd_xiangzhen_exercises_id
response = requests.get(question_url, headers=headers)
gd_xiangzhen_question_content = response.text
gd_xiangzhen_exercise_question = ExerciseQuestions(gd_xiangzhen_question_content)

# 对比言语题
yanyu_filter_list = list(common_exercises.yanyu_questionIds)
for questionId in gd_exercises.yanyu_questionIds:
    if questionId in yanyu_filter_list:
        yanyu_filter_list.remove(questionId)
yanyu_diff_questions = [common_exercise_question.questions[str(x)] for x in yanyu_filter_list]

# 资料获取到差异题，然后获取相同的materialindex。先输出material再输出相应的题目
ziliao_filter_list = list(common_exercises.ziliao_questionIds)
for questionId in gd_exercises.ziliao_questionIds:
    if questionId in ziliao_filter_list:
        ziliao_filter_list.remove(questionId)
ziliao_diff_question = [common_exercise_question.questions[str(x)] for x in ziliao_filter_list]
ziliao_material_index_set = set()
for question in ziliao_diff_question:
    ziliao_material_index_set.update(question.materialIndexes)
ziliao_material_dic = {}
for index in ziliao_material_index_set:
    ziliao_material_dic[index] = common_exercise_question.materials[index]

# 科学推理
ketui_diff_questions = []
if len(gd_xiangzhen_exercises_id) > 0:
    ketui_filter_list = list(gd_xiangzhen_exercises.ketui_questionIds)
    for questionId in gd_exercises.ketui_questionIds:
        if questionId in ketui_filter_list:
            ketui_filter_list.remove(questionId)
    ketui_diff_questions = [gd_xiangzhen_exercise_question.questions[str(x)] for x in ketui_filter_list]

# 用html做出试卷，并转成pdf，最后输出到文件夹中
createHTML(yanyu_diff_questions, ziliao_material_dic, ziliao_diff_question, ketui_diff_questions)
