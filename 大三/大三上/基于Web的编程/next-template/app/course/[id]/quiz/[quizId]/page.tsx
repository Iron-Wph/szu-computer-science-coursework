'use client'

import { useState, useEffect } from 'react'
import { Card, CardBody, CardHeader, Checkbox, Button, Divider } from "@nextui-org/react"
import { toast, Toaster } from 'react-hot-toast'
interface Question {
    // 题目ID
    questionId: string;
    // 题目描述
    description: string;
    // 题目答案
    answer: string;
    // 题目类型
    type: string;
    // 题目解析
    analysis: string;
}


// 模拟的数据库接口
const mockDatabaseInterface = {
  getQuestions: async () => {
    // 这里应该是从 IndexedDB 获取数据的逻辑
    // 现在我们返回模拟数据
    return [
      {
        id: 1,
        type: 'single',
        question: '下列哪个不是 JavaScript 的数据类型？',
        options: ['String', 'Number', 'Boolean', 'Character'],
        correctAnswer: 'Character',
        explanation: 'JavaScript 没有 Character 数据类型。JavaScript 的基本数据类型包括 String、Number、Boolean、Undefined、Null、Symbol 和 BigInt。'
      },
      {
        id: 2,
        type: 'multiple',
        question: '以下哪些是 React 的核心概念？',
        options: ['组件', '虚拟 DOM', 'JSX', '双向数据绑定'],
        correctAnswer: ['组件', '虚拟 DOM', 'JSX'],
        explanation: 'React 的核心概念包括组件、虚拟 DOM 和 JSX。双向数据绑定不是 React 的核心概念，它更常见于 Angular 等框架。'
      }
    ]
  },
  submitAnswers: async (answers) => {
    // 这里应该是向 IndexedDB 提交答案的逻辑
    console.log('Submitted answers:', answers)
    return { success: true }
  }
}

export default function QuizPage() {
  const [questions, setQuestions] = useState([])
  const [answers, setAnswers] = useState({})
  const [showExplanations, setShowExplanations] = useState(false)

  useEffect(() => {
    const fetchQuestions = async () => {
      const fetchedQuestions = await mockDatabaseInterface.getQuestions()
      setQuestions(fetchedQuestions)
    }
    fetchQuestions()
  }, [])

  const handleAnswerChange = (questionId, option, isChecked) => {
    setAnswers(prev => {
      const questionAnswers = prev[questionId] || []
      if (isChecked) {
        return {
          ...prev,
          [questionId]: [...questionAnswers, option]
        }
      } else {
        return {
          ...prev,
          [questionId]: questionAnswers.filter(answer => answer !== option)
        }
      }
    })
  }

  const handleSubmit = async () => {
    const result = await mockDatabaseInterface.submitAnswers(answers)
    if (result.success) {
      toast.success('答案提交成功！')
      setShowExplanations(true)
    } else {
      toast.error('提交失败，请重试。')
    }
  }

  return (
    <div className="container mx-auto p-4 w-4/5">
      <h1 className="text-2xl font-bold mb-4">答题界面</h1>
      {questions.map((question) => (
        <Card key={question.id} className="mb-4">
          <CardHeader>
            <h2 className="text-lg font-semibold">{question.question}</h2>
          </CardHeader>
          <CardBody>
            <div className="flex flex-col gap-2">
              {question.options.map((option, index) => (
                <Checkbox
                  key={index}
                  isSelected={answers[question.id]?.includes(option)}
                  onValueChange={(isSelected) => handleAnswerChange(question.id, option, isSelected)}
                >
                  {option}
                </Checkbox>
              ))}
            </div>
            {showExplanations && (
              <div className="mt-4">
                <Divider />
                <p className="text-sm text-gray-600 mt-2">
                  <span className="font-semibold">解析：</span> {question.explanation}
                </p>
              </div>
            )}
          </CardBody>
        </Card>
      ))}
      <Button color="primary" onClick={handleSubmit}>
        提交答案
      </Button>
      <Toaster position="bottom-center" />
    </div>
  )
}
