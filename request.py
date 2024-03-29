import requests
from examModel import *
from createHTML import *

# 获取试卷的整体信息，为了获取questionIds 下面三个试卷id和cookie需填入
common_exercises_id = '2551438388'
gd_exercises_id = '2551441705'
# 乡镇，用来获取科学推理差异题
gd_xiangzhen_exercises_id = '2551441321'
cookie = 'sid=148033; _ga=GA1.2.1604876671.1670060906; persistent=bS0BhTaGkgzOJPBsuOq+BbUFnY+01ThSQoCv7XR7D9nnafNeAOQJQuDwu3CK/qOkIPSm45M71OnWpoy58LiURQ==; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%22110158411%22%2C%22first_id%22%3A%22184d7603219da4-09b11ab4beb522-1a525635-2073600-184d760321aa49%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%2C%22%24latest_referrer%22%3A%22%22%7D%2C%22%24device_id%22%3A%22184d7603219da4-09b11ab4beb522-1a525635-2073600-184d760321aa49%22%2C%22identities%22%3A%22eyIkaWRlbnRpdHlfY29va2llX2lkIjoiMTg2ZjM4Y2M3ZTYyZjctMGYzOTg5ZGUyNWM5MTM4LTFmNTI1NjM0LTE5MzAxNzYtMTg2ZjM4Y2M3ZTcxYzg5IiwiJGlkZW50aXR5X2xvZ2luX2lkIjoiMTEwMTU4NDExIn0%3D%22%2C%22history_login_id%22%3A%7B%22name%22%3A%22%24identity_login_id%22%2C%22value%22%3A%22110158411%22%7D%7D; userid=110158411; _ga_HKHM0G5171=GS1.2.1706097785.53.0.1706097785.0.0.0; sess=XoWA940wGRR8CYb/8eSrk4NxNyjtnz9JWM1E5m8A2hgZivt+Vh00ulvgQLsE7M+QCSqaeukgSoNSUsNS3+q1wYpTdqqFI2waW1G9o2QLrIQ=; acw_tc=0bdd303617064117869625904e0f52ba7445dd20abfb142604df7ba97ec5cd'
headers = {'Accept-Language': 'zh-CN', 'Cookie': cookie}

def createExercises(exercise_id):
    fenbi_exercises_base_url = "https://tiku.fenbi.com/api/xingce/exercises/"
    exercise_url_paramter_string = "?app=web&kav=100&av=100&hav=100&version=3.0.0.0"
    fenbi_exercises_url = fenbi_exercises_base_url + exercise_id + exercise_url_paramter_string
    response = requests.get(fenbi_exercises_url, headers=headers)
    common_exercises_content = response.text
    return Exercise(common_exercises_content)

def createQuestions(exercises_id):
    # 获取通用试卷的题目
    question_base_url = "https://tiku.fenbi.com/api/xingce/universal/auth/questions?"
    #最后直接加exerciseid
    question_url_paramter_string = 'type=0&app=web&kav=100&av=100&hav=100&version=3.0.0.0&id='
    question_url = question_base_url + question_url_paramter_string + exercises_id
    response = requests.get(question_url, headers=headers)
    content = response.text
    return ExerciseQuestions(content)

def main():

    common_exercises = createExercises(common_exercises_id)

    gd_exercises = createExercises(gd_exercises_id)

    gd_xiangzhen_exercises = createExercises(gd_xiangzhen_exercises_id)

    common_exercise_question = createQuestions(common_exercises_id)

    gd_xiangzhen_exercise_question = createQuestions(gd_xiangzhen_exercises_id)

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

    # 数量
    shuliang_filter_list = list(common_exercises.shuliang_questionIds)
    for questionId in gd_exercises.shuliang_questionIds:
        if questionId in shuliang_filter_list:
            shuliang_filter_list.remove(questionId)
    shuliang_diff_questions = [common_exercise_question.questions[str(x)] for x in shuliang_filter_list]
    print(shuliang_diff_questions)

    # 用html做出试卷，并转成pdf，最后输出到文件夹中
    createHTML(yanyu_diff_questions, ziliao_material_dic, ziliao_diff_question, ketui_diff_questions, shuliang_diff_questions)



if __name__ == '__main__':
    main()