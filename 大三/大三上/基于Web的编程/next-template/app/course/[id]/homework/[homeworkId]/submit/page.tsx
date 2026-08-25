'use client'

import React, { useState } from 'react'
import {
  Card,
  CardBody,
  CardHeader,
  Button,
} from "@nextui-org/react"
import MyEditor from "@/components/MyEditor"
import { useParams } from 'next/navigation'
import { updateHomework,submitHomework } from '../../../../../../lib/indexedDB'
import toast from 'react-hot-toast'

interface Homework {
  // 作业ID
  homeworkId: string;
  // 作业名字
  homeworkName: string;
  // 课程ID
  courseId: string;
  // 开始时间
  startTime: string;
  // 截止时间
  dueTime: string;
  // 作业描述
  description: string;
  // 学生名单（用户ID数组）
  studentList: string[];
  // 已完成名单（用户ID数组）
  completedList: string[];
  // 是否截止状态
  isDue: boolean;
  // 评分
  score: number[];
  // 提交的作业
  submittedHomework: { userId: string; content: string }[];
}

// // IndexedDB 工具函数
// const initDB = () => {
//   return new Promise((resolve, reject) => {
//     const request = indexedDB.open('HomeworkDB', 1)
//     request.onerror = () => reject("IndexedDB 初始化失败")
//     request.onsuccess = () => resolve(request.result)
//     request.onupgradeneeded = (event) => {
//       const db = event.target.result
//       db.createObjectStore('homework', { keyPath: 'homeworkId' })
//     }
//   })
// }

const submitHw = async (homework:{homeworkId: string, content: string, userId: string}) => {
  // await updateHomework(homework)
  await submitHomework(homework)
}

// 作业提交组件
export default function HomeworkSubmission() {
  const {id} = useParams();
  const {homeworkId} = useParams();
  const [homework, setHomework] = useState({
    homeworkId: homeworkId,
    content: '', // Only keeping content for homework submission
    userId: localStorage.getItem('userId') || ''
  })

  const handleContentChange = (content:string) => {
    setHomework(prev => ({ ...prev, content }))
  }

  const handleSubmit = async () => {
    if (!homework.content) {
      toast.success('作业内容不能为空！')
      return
    }
    try {
      await submitHw(homework)
      toast.success('作业提交成功！')
      window.location.href = `/course/${id}`
    } catch (error) {
      console.error('提交作业时出错:', error)
      toast.success('提交作业失败。请重试。')
    }
  }

  return (
    <Card className="max-w-4xl mx-auto my-8">
      <CardHeader className="flex gap-3">
        <h1 className="text-2xl font-bold">提交作业</h1>
      </CardHeader>
      <CardBody>
        <div className="space-y-6">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">作业内容</label>
            <MyEditor
              initialValue={homework.content}
              onChange={handleContentChange}
            />
          </div>
          <Button color="primary" onPress={handleSubmit}>
            提交作业
          </Button>
        </div>
      </CardBody>
    </Card>
  )
}