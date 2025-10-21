import requests
from examModel import *
from createHTML import *

# 获取试卷的整体信息，为了获取questionIds 下面三个试卷id和cookie需填入
common_exercises_id = '3577988128'
gd_exercises_id = '3577981609'
cookie = "_ga=GA1.2.1735601216.1746068960; _ga_Z92YWZPKSM=GS2.2.s1747208213$o1$g0$t1747208214$j0$l0$h0; _ga_HKHM0G5171=GS2.2.s1747200599$o94$g1$t1747208884$j0$l0$h0; sid=148033; persistent=bS0BhTaGkgzOJPBsuOq+BbUFnY+01ThSQoCv7XR7D9nY6IOkuQf8krxSTag8dl6Bd9ExRJERGC9vUSabiRAzyg==; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%22110158411%22%2C%22first_id%22%3A%221992e73acf83c0-0ebe3e81ee71138-1b525636-1930176-1992e73acf91f16%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%2C%22%24latest_referrer%22%3A%22%22%7D%2C%22%24device_id%22%3A%22196899f3d0c8d0-06c92089d51e1c-1b525636-1930176-196899f3d0d18ba%22%2C%22identities%22%3A%22eyIkaWRlbnRpdHlfY29va2llX2lkIjoiMTk2ODlkMDIzOTVmNDctMDJlZWNmNzgwNzRkZTM4LTFiNTI1NjM2LTE5MzAxNzYtMTk2ODlkMDIzOTZlZjAiLCIkaWRlbnRpdHlfbG9naW5faWQiOiIxMTAxNTg0MTEifQ%3D%3D%22%2C%22history_login_id%22%3A%7B%22name%22%3A%22%24identity_login_id%22%2C%22value%22%3A%22110158411%22%7D%7D; Hm_lvt_e7351028cde0d0ccb9ccdbe5fe531683=1761058850; Hm_lpvt_e7351028cde0d0ccb9ccdbe5fe531683=1761058850; HMACCOUNT=1B98EC4164CC88B4; sess=XoWA940wGRR8CYb/8eSrk4NxNyjtnz9JWM1E5m8A2hgZivt+Vh00ulvgQLsE7M+QLxa/6+bQkgOSuLVvnVSaz/Mq0jcRAMtV0y6SkGq+V+o=; userid=110158411; acw_tc=0bdd34d217610588566088641e3d253a893501eb78f01743e6db098e624415"
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
    question_base_url = "https://tiku.fenbi.com/api/xingce/universal/auth/questions"
    #最后直接加exerciseid
    question_url_paramter_string = '?type=0&app=web&kav=100&av=100&hav=100&version=3.0.0.0&id='
    question_url = question_base_url + question_url_paramter_string + exercises_id
    response = requests.get(question_url, headers=headers)
    content = response.text
    return ExerciseQuestions(content)

def main():

    common_exercises = createExercises(common_exercises_id)

    gd_exercises = createExercises(gd_exercises_id)



    common_exercise_question = createQuestions(common_exercises_id)



    # 对比言语题
    yanyu_filter_list = list(common_exercises.yanyu_questionIds)
    for questionId in gd_exercises.yanyu_questionIds:
        if questionId in yanyu_filter_list:
            yanyu_filter_list.remove(questionId)
    yanyu_diff_questions = [common_exercise_question.questions[str(x)] for x in yanyu_filter_list]

    # 判断 去除定义
    panduan_filter_list = []
    for question_num in range(common_exercises.panduan_start_num, common_exercises.panduan_end_num):
        print(question_num)
        if question_num not in range(85, 96) and question_num not in range(105, 110):
            panduan_filter_list.append(common_exercises.questionIds[question_num])
    for questionId in gd_exercises.panduan_questionIds:
        if questionId in panduan_filter_list:
            panduan_filter_list.remove(questionId)
    panduan_filter_list = [common_exercise_question.questions[str(x)] for x in panduan_filter_list]

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

    # 数量
    shuliang_filter_list = list(common_exercises.shuliang_questionIds)
    for questionId in gd_exercises.shuliang_questionIds:
        if questionId in shuliang_filter_list:
            shuliang_filter_list.remove(questionId)
    shuliang_diff_questions = [common_exercise_question.questions[str(x)] for x in shuliang_filter_list]

    # 用html做出试卷，并转成pdf，最后输出到文件夹中
    createHTML(yanyu_diff_questions, ziliao_material_dic, ziliao_diff_question, shuliang_diff_questions, panduan_filter_list)



if __name__ == '__main__':
    main()