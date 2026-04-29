import api from '@/utils/request'

export const questionApi = {
  // 获取题目列表
  getQuestions(params) {
    return api.get('/api/questions/', { params })
  },

  // 获取随机题目
  getRandomQuestions(params) {
    return api.get('/api/questions/random/', { params })
  },

  // 获取题目详情
  getQuestion(id) {
    return api.get(`/api/questions/${id}/`)
  },

  // 获取题目分类
  getCategories() {
    return api.get('/api/questions/categories/')
  },

  // 获取错题本
  getWrongQuestions() {
    return api.get('/api/questions/wrong/')
  },

  // 添加错题
  addWrongQuestion(data) {
    return api.post('/api/questions/wrong/add/', data)
  },

  // 标记错题为已掌握
  markCorrect(id) {
    return api.post(`/api/questions/wrong/${id}/mark_correct/`)
  },

  // 获取作业列表
  getAssignments() {
    return api.get('/api/questions/assignments/')
  },

  // 提交作业
  submitAssignment(id, data) {
    return api.post(`/api/questions/assignments/${id}/submit/`, data)
  }
}

export const activityApi = {
  // 获取活动列表
  getActivities(params) {
    return api.get('/api/activities/', { params })
  },

  // 获取活动详情
  getActivity(id) {
    return api.get(`/api/activities/${id}/`)
  },

  // 创建活动
  createActivity(data) {
    return api.post('/api/activities/', data)
  },

  // 参与活动
  participate(id, data) {
    return api.post(`/api/activities/${id}/participate/`, data)
  }
}

export const statsApi = {
  // 获取首页统计
  getDashboard() {
    return api.get('/api/stats/dashboard/')
  },

  // 获取学员分布
  getStudentDistribution(params) {
    return api.get('/api/stats/student_distribution/', { params })
  },

  // 获取用户分布
  getUserDistribution() {
    return api.get('/api/stats/user_distribution/')
  },

  // 获取就业城市分布
  getEmploymentCities() {
    return api.get('/api/stats/employment_cities/')
  },

  // 获取最高薪资
  getTopSalaries() {
    return api.get('/api/stats/top_salaries/')
  },

  // 获取优秀学员
  getExcellentStudents() {
    return api.get('/api/stats/excellent-students/')
  },

  // 获取面试题
  getInterviewQuestions() {
    return api.get('/api/stats/interview-questions/')
  }
}

export const evaluationApi = {
  // 获取评价列表
  getEvaluations() {
    return api.get('/api/evaluations/')
  },

  // 创建评价
  createEvaluation(data) {
    return api.post('/api/evaluations/', data)
  },

  // 获取学员进度
  getStudentProgress() {
    return api.get('/api/evaluations/progress/')
  },

  // 获取我的学员
  getMyStudents() {
    return api.get('/api/evaluations/progress/my_students/')
  }
}
