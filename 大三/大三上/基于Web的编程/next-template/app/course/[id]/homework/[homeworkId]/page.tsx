'use client'

import React, { useState, useEffect } from 'react'
import { Table, TableHeader, TableColumn, TableBody, TableRow, TableCell, Button, Card, CardHeader, CardBody, Chip, Avatar, Tooltip } from "@nextui-org/react"
import { useAsyncList } from "@react-stately/data"
import { updateCourse, getCourse, getUsers, getAllCourses, getAllHomeworks, getHomework, getUser, getHomeworksByCourseIds } from '../../../../../lib/indexedDB'
import { useParams } from 'next/navigation'
interface User {
  // 用户类型
  userType: string;
  // 用户ID
  userId: string;
  // 用户密码
  password: string;
  // 头像URL
  avatarUrl: string;
  // 用户昵称
  nickname: string;
  // 选课数组
  selectedCourses: string[];
  // 收藏课程数组
  favoriteCourses: string[];
  // 密码错误次数
  passwordErrorCount: number;
  // 用户状态
  status: string;
  // 学习历史记录
  learningHistory: string[];
  // 描述
  description: string;
  // 内容
  content: string;
}

interface Course {
  // 课程ID
  courseId: string;
  // 课程图片 URL
  courseImageUrl: string;
  // 选课人数
  numberOfEnrolledStudents: number;
  // 课程类别
  courseCategory: string;
  // 课程名字
  courseName: string;
  // 发布日期
  publishDate: string;
  // 点赞数
  numberOfLikes: number;
  // 讨论区（用户ID和讨论内容）
  discussionArea: { userId: string; content: string }[];
  // 是否设置讨论区
  hasDiscussionArea: boolean;
  // 是否设置笔记区
  hasNoteArea: boolean;
  // 选课名单（用户ID组）
  enrollmentList: string[];
  // 授课教师ID
  teacherId: string;
  // 课程资源id
  resourceId: string[];
  // 课程所属大学
  university: string;
  // 授课教师
  instructor: string;
  // 课程简介
  description: string;
  // 课程内容
  content: string;
  // 是否放在首页
  isHomepage: boolean;
}
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

// // 模拟数据生成函数
// const generateMockData = async () => {
//   const users:User[] =await getUsers()
//   const homeworks:Homework[] = await getAllHomeworks()

//   const course = await getCourse(id)

//   return { users, homework, course }
// }

// // IndexedDB交互的占位符
// const fetchData = async () => {
//   // 在实际应用中，这将从IndexedDB中获取数据
//   return generateMockData()
// }

export default function HomeworkSubmissions() {
  const [data, setData] = useState<{ users: User[], homework: Homework, course: Course }>()
  // 获取课程和作业ID
  const { id, homeworkId } = useParams()
  const [list, setList] = useState<{ userId: string; content: string }[]>([]);
  useEffect(() => {
    const fetchData = async () => {
      const course = await getCourse(id)
      if (!course) throw new Error('课程不存在')

      const homework = await getHomework(homeworkId)
      if (!homework) throw new Error('作业不存在')

      const lists = homework.submittedHomework;
      setList(lists);
      const users = await Promise.all(
        course.enrollmentList.map(async (userId: string) => {
          const user = await getUser(userId)
          if (!user) throw new Error(`用户 ${userId} 不存在`)
          return user
        })
      )

      return { users, homework, course }
    }
    fetchData().then(setData)
  }, [])

  // const list = useAsyncList({
  //   getHomework(homeworkId)

  //   // async load({ signal }) {
  //   //   await new Promise(resolve => setTimeout(resolve, 500)) // 模拟网络延迟
  //   //   return {
  //   //     items: data?.users ?? [],
  //   //   }
  //   // },
  // })

  if (!data) {
    return <div className="flex justify-center items-center h-screen">加载中...</div>
  }

  return (
    <div className="container mx-auto p-6 w-4/5">
      <Card className="mb-6">
        <CardHeader className="flex justify-between items-center">
          <h1 className="text-2xl font-bold">{data.homework.homeworkName} 作业提交</h1>
          <Chip color="primary">{data.course.courseName}</Chip>
        </CardHeader>
        <CardBody>
          <p><strong>截止日期：</strong> {new Date(data.homework.dueTime).toLocaleDateString()}</p>
          <p><strong>描述：</strong> {data.homework.description}</p>
          <p><strong>提交进度：</strong> {data.homework.submittedHomework.length} / {data.homework.studentList.length}</p>
        </CardBody>
      </Card>

      <Table
        aria-label="作业提交表格"
        className="mt-4"
      >
        <TableHeader>
          <TableColumn>学生</TableColumn>
          <TableColumn>状态</TableColumn>
          <TableColumn>操作</TableColumn>
        </TableHeader>
        <TableBody>
          {list.map((item: { userId: string; content: string }) => (
            <TableRow key={item.userId}>
              <TableCell>
                <div className="flex items-center gap-3">
                  {/* <Avatar src={user.avatarUrl} size="sm" /> */}
                  <div>
                    {/* <p className="font-semibold">{user.nickname}</p> */}
                    <p className="text-small text-default-500">{item.userId}</p>
                  </div>
                </div>
              </TableCell>
              <TableCell>
                <Chip color={data.homework.completedList.includes(item.userId) ? "success" : "warning"} variant="flat">
                  {data.homework.completedList.includes(item.userId) ? "已提交" : "未提交"}
                </Chip>
              </TableCell>
              <TableCell>
                <Tooltip content={data.homework.completedList.includes(item.userId) ? "查看提交" : "尚未提交"}>
                  <Button
                    size="sm"
                    color={data.homework.completedList.includes(item.userId) ? "primary" : "default"}
                    isDisabled={!data.homework.completedList.includes(item.userId)}
                  >
                    查看提交
                  </Button>
                </Tooltip>
              </TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </div>
  )
}