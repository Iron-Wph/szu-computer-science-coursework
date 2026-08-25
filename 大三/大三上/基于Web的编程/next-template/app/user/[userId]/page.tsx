'use client'

import { useEffect, useState } from 'react'
import { Card, CardBody, Avatar, Button, Tabs, Tab, Input, Textarea, button, Link, Accordion, AccordionItem } from "@nextui-org/react"
import Image from "next/image"
import { motion } from "framer-motion"
import { getUser, getCourses, updateUser, getAnnouncementsByCourseIds, getHomeworksByCourseIds } from '../../../lib/indexedDB'
import ImageUploader from '@/components/ImageUploader'
import { HomeworkModal } from '@/app/course/[id]/page'
import { CheckSquare } from 'lucide-react'
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

export interface Course {
  courseId: string;
  courseImageUrl: string;
  numberOfEnrolledStudents: number;
  courseCategory: string;
  courseName: string;
  publishDate: string;
  numberOfLikes: number;
  discussionArea: { userId: string; content: string }[];
  hasDiscussionArea: boolean;
  hasNoteArea: boolean;
  enrollmentList: string[];
  teacherId: string;
  resourceId: string[],
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

export interface User {
  userType: string;
  userId: string;
  password: string;
  avatarUrl: string;
  nickname: string;
  selectedCourses: string[];
  favoriteCourses: string[];
  passwordErrorCount: number;
  status: string;
  learningHistory: string[];
  // 描述
  description: string;
  // 内容
  content: string;
  // 笔记
  note: { content: string; time: string,courseId:string}[];
}
// 定义公告接口
interface Announcement {
  announcementId: string;
  courseId: string;
  announcementTime: string;
  announcementTitle: string;
  announcementContent: string;
}

// 模拟与IndexedDB交互的函数
const fetchUserData = async (userId: string): Promise<User> => {
  // 这里应该是从IndexedDB获取数据的逻辑
  // 现在我们只返回模拟数据
  const user = await getUser(userId);
  if (!user) {
    return {
      userType: "student",
      userId: userId,
      password: "<demo-password>",
      avatarUrl: "https://s1.locimg.com/2024/12/25/4f43ce87187ad.jpg",
      nickname: "学生小明",
      selectedCourses: ["course1", "course2", "course3"],
      favoriteCourses: ["course4", "course5"],
      passwordErrorCount: 0,
      status: "active",
      learningHistory: ["history1", "history2"],
      description: "这是一个描述",
      content: "这是一个内容",
      note: []
    }
  }
  return user;
}
const fetchAnnouncements = async (courseIds: string[]): Promise<Announcement[]> => {
  // 这里应该是从IndexedDB获取数据的逻辑
  // 现在我们只返回模拟数据
  const announcements = await getAnnouncementsByCourseIds(courseIds);
  return announcements;
}

// 获取作业
const fetchHomeworks = async (courseIds: string[]): Promise<Homework[]> => {
  const homeworks = await getHomeworksByCourseIds(courseIds);
  return homeworks;
}

const fetchCourses = async (courseIds: string[]): Promise<Course[]> => {
  // 这里应该是从IndexedDB获取数据的逻辑
  // 现在我们只返回模拟数据
  const courses = await getCourses(courseIds);
  if (courses.length === 0) {
    return courseIds.map((id, index) => ({
      courseId: id,
      courseImageUrl: `https://s1.locimg.com/2024/12/25/${index + 1}b9f98ef71be1.jpg`,
      numberOfEnrolledStudents: Math.floor(Math.random() * 100) + 1,
      courseCategory: ["计算机科学", "数学", "物理"][index % 3],
      courseName: `课程 ${id}`,
      publishDate: new Date().toISOString().split('T')[0],
      numberOfLikes: Math.floor(Math.random() * 50),
      discussionArea: [],
      hasDiscussionArea: true,
      hasNoteArea: true,
      enrollmentList: [],
      teacherId: `teacher${index + 1}`,
      resourceId: [],
      university: "清华大学",
      instructor: "张三",
      description: "这是一个描述",
      content: "这是一个内容",
      isHomepage: false
    }))
  }
  return courses;
}

export default function UserProfile() {
  const [user, setUser] = useState<User | null>(null)
  const [courses, setCourses] = useState<Course[]>([])
  const [isEditing, setIsEditing] = useState(false)
  const [editedUser, setEditedUser] = useState<Partial<User>>({})
  const [favoriteCourses, setFavoriteCourses] = useState<Course[]>([])
  const [learningHistory, setLearningHistory] = useState<Course[]>([])
  const [announcements, setAnnouncements] = useState<Announcement[]>([])
  const [homeworks, setHomeworks] = useState<Homework[]>([])
  const [note, setNote] = useState<{ content: string; time: string,courseId:string}[]>([])
  useEffect(() => {
    const loadData = async () => {
      const userData = await fetchUserData(localStorage.getItem("username") || "")
      setUser(userData)
      const coursesData = await fetchCourses(userData.selectedCourses)
      setCourses(coursesData)
      const favoriteCoursesData = await fetchCourses(userData.favoriteCourses)
      setFavoriteCourses(favoriteCoursesData)
      const learningHistoryData = await fetchCourses(userData.learningHistory)
      setLearningHistory(learningHistoryData)
      const announcementsData = await fetchAnnouncements(userData.selectedCourses)
      setAnnouncements(announcementsData)
      const homeworksData = await fetchHomeworks(userData.selectedCourses)
      setHomeworks(homeworksData)
    }
    loadData()
  }, [])

  const handleEdit = () => {
    setIsEditing(true)
    setEditedUser({
      nickname: user?.nickname,
      avatarUrl: user?.avatarUrl,
      description: user?.description
    })
  }

  const handleSave = () => {
    if (user && editedUser) {
      setUser({ ...user, ...editedUser })
      setIsEditing(false)
      // 这里应该有保存到IndexedDB的逻辑
      updateUser({ ...user, ...editedUser })
      window.location.reload();
    }
  }

  const handleCancel = () => {
    setIsEditing(false)
    setEditedUser({})
  }

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    const { name, value } = e.target
    setEditedUser(prev => ({ ...prev, [name]: value }))
  }
  const handleImageUpload = (url) => {
    setUser(prev => ({ ...prev, avatarUrl: url }))
    setEditedUser(prev => ({ ...prev, avatarUrl: url }))
    console.log(url)
  }

  if (!user) {
    return <div>加载中...</div>
  }


  return (
    <div className="min-h-screen bg-gray-100 p-8">
      <div className="max-w-7xl mx-auto">
      <div className="flex flex-col md:flex-row gap-8">
          {/* 侧边栏 */}
          <motion.div
            initial={{ opacity: 0, x: -50 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.5 }}
            className="w-full md:w-1/4"
          >
            <Card className="p-6">
              <CardBody className="flex flex-col items-center">
                <Avatar
                  src={user.avatarUrl}
                  className="w-32 h-32 text-large"
                />
                {isEditing ? (
                  <ImageUploader onImageUpload={handleImageUpload} />
                ) : (
                  <></>
                )}
                {isEditing ? (
                  <Input
                    name="nickname"
                    value={editedUser.nickname || ''}
                    onChange={handleInputChange}
                    className="mt-4"
                  />
                ) : (
                  <h2 className="mt-4 text-2xl font-bold">{user.nickname}</h2>
                )}
                <h3 className="mt-2 text-gray-600">类型: {user.userType}</h3>
                {isEditing ? (
                  <Textarea
                    name="description"
                    value={editedUser.description || ''}
                    onChange={handleInputChange}
                    className="mt-4"
                    placeholder="请输入描述"
                  />
                ) : (
                  <p className="mt-2 text-gray-600">{user.description}</p>
                )}
                {isEditing ? (
                  <div className="mt-4 flex gap-2">
                    <Button color="primary" onClick={handleSave}>保存</Button>
                    <Button color="secondary" onClick={handleCancel}>取消</Button>
                  </div>
                ) : (
                  <Button color="primary" onClick={handleEdit} className="mt-4">编辑资料</Button>
                )}
              </CardBody>
            </Card>
          </motion.div>

          {/* 主要内容 */}
          <motion.div
            initial={{ opacity: 0, y: 50 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5 }}
            className="flex-1"
          >
            <Tabs aria-label="用户信息" color="primary">
            <Tab key="courses" title="相关课程">
                <div className="mt-4 space-y-4">
                  {courses.length > 0 && courses.map((course) => (
                    <motion.div
                      key={course.courseId}
                      initial={{ opacity: 0, y: 20 }}
                      animate={{ opacity: 1, y: 0 }}
                      transition={{ duration: 0.3 }}
                    >
                      <Card className="w-full h-[160px]">
                        <CardBody className="p-0 overflow-hidden">
                          <div className="relative w-full h-full">
                            <Image
                              src={course.courseImageUrl}
                              alt={course.courseName}
                              layout="fill"
                              objectFit="cover"
                            />
                            <div className="absolute inset-0 bg-gradient-to-t from-black/90 via-black/50 to-transparent" />
                            <div className="absolute inset-0 p-6 flex flex-col justify-between">
                              <div>
                                <Link  href={`/course/${course.courseId}`} className="text-2xl font-bold text-white mb-2">{course.courseName}</Link>
                                <p className="text-base text-gray-300">{course.courseCategory}</p>
                              </div>
                              <div className="space-y-3">
                                <div className="space-y-2">
                                  <p className="text-base text-gray-300">教师ID: {course.teacherId}</p>
                                  <p className="text-base text-gray-300">发布日期: {course.publishDate}</p>
                                </div>
                                <div className="flex justify-between">
                                  <p className="text-base text-white">已选 {course.numberOfEnrolledStudents}</p>
                                  <p className="text-base text-white">点赞 {course.numberOfLikes}</p>
                                </div>
                              </div>
                            </div>
                          </div>
                        </CardBody>
                      </Card>
                    </motion.div>
                  ))}
                </div>
              </Tab>
              {user.userType === "student" &&(
                <Tab key="favorites" title="收藏课程">
                  <div className="mt-4">
                    {favoriteCourses.length > 0 && favoriteCourses.map((course) => (
                      <motion.div
                        key={course.courseId}
                        initial={{ opacity: 0, y: 20 }}
                        animate={{ opacity: 1, y: 0 }}
                        transition={{ duration: 0.3 }}
                      >
                        <Card className="w-full h-[160px]">
                          <CardBody className="p-0 overflow-hidden">
                            <div className="relative w-full h-full">
                              <Image
                                src={course.courseImageUrl}
                                alt={course.courseName}
                                layout="fill"
                                objectFit="cover"
                              />
                              <div className="absolute inset-0 bg-gradient-to-t from-black/90 via-black/50 to-transparent" />
                              <div className="absolute inset-0 p-6 flex flex-col justify-between">
                                <div>
                                  <h3 className="text-2xl font-bold text-white mb-2">{course.courseName}</h3>
                                  <p className="text-base text-gray-300">{course.courseCategory}</p>
                                </div>
                                <div className="space-y-3">
                                  <div className="space-y-2">
                                    <p className="text-base text-gray-300">教师ID: {course.teacherId}</p>
                                    <p className="text-base text-gray-300">发布日期: {course.publishDate}</p>
                                  </div>
                                  <div className="flex justify-between">
                                    <p className="text-base text-white">已选 {course.numberOfEnrolledStudents}</p>
                                    <p className="text-base text-white">点赞 {course.numberOfLikes}</p>
                                  </div>
                                </div>
                              </div>
                            </div>
                          </CardBody>
                        </Card>
                      </motion.div>
                    ))}
                  </div>
                </Tab>
                
                  )
              }
              {user.userType === "student" && (
                <Tab key="history" title="学习历史">
                  <div className="mt-4">
                    {learningHistory.length > 0 && learningHistory.map((course) => (
                      <motion.div
                        key={course.courseId}
                        initial={{ opacity: 0, y: 20 }}
                        animate={{ opacity: 1, y: 0 }}
                        transition={{ duration: 0.3 }}
                      >
                        <Card className="w-full h-[160px]">
                          <CardBody className="p-0 overflow-hidden">
                            <div className="relative w-full h-full">
                              <Image
                                src={course.courseImageUrl}
                                alt={course.courseName}
                                layout="fill"
                                objectFit="cover"
                              />
                              <div className="absolute inset-0 bg-gradient-to-t from-black/90 via-black/50 to-transparent" />
                              <div className="absolute inset-0 p-6 flex flex-col justify-between">
                                <div>
                                  <Link  href={`/course/${course.courseId}`} className="text-2xl font-bold text-white mb-2">{course.courseName}</Link>
                                  <p className="text-base text-gray-300">{course.courseCategory}</p>
                                </div>
                                <div className="space-y-3">
                                  <div className="space-y-2">
                                    <p className="text-base text-gray-300">教师ID: {course.teacherId}</p>
                                    <p className="text-base text-gray-300">发布日期: {course.publishDate}</p>
                                  </div>
                                  <div className="flex justify-between">
                                    <p className="text-base text-white">已选 {course.numberOfEnrolledStudents}</p>
                                    <p className="text-base text-white">点赞 {course.numberOfLikes}</p>
                                  </div>
                                </div>
                              </div>
                            </div>
                          </CardBody>
                        </Card>
                      </motion.div>
                    ))}
                  </div>
                </Tab>
              )
              }
              // 个人待办
              <Tab
          key="todo-items"
          title={
            <div className="flex items-center gap-2">
              <span>待完成事项</span>
            </div>
          }
        >
          <div className="mt-8">
            {/* Placeholder for Todo Items */}
            <Card className="p-4 shadow-lg">
              <h2 className="text-xl font-semibold mb-4">待完成事项</h2>
              {localStorage.getItem("role") === "teacher" && (
                <HomeworkModal/>
              )}
              {/* Replace with actual todo items */}
              <Accordion>
                {homeworks && homeworks.map((homework) => (
                  <AccordionItem
                    key={homework.homeworkId}
                    aria-label={homework.homeworkName}
                    title={homework.homeworkName}
                    subtitle={`截止时间：${homework.dueTime}`}
                    onClick={() => {
                      if (localStorage.getItem("role") === "student") {
                        window.location.href = `/course/${id}/homework/${homework.homeworkId}/submit`
                      }
                      else {
                        window.location.href = `/course/${id}/homework/${homework.homeworkId}`
                      }
                    }}
                  >
                    {homework.description}
                  </AccordionItem>
                ))}
              </Accordion>
            </Card>
          </div>
        </Tab>
              {/* 个人笔记 */}
              <Tab key="note" title="笔记">
                <div className="mt-4">
                  {user.note.length > 0 && user.note.map((note) => (
                    <div dangerouslySetInnerHTML={{ __html: note.content }} />
                  ))}
                </div>
              </Tab>
            </Tabs>

          </motion.div>
        </div>


        {user.userType === "teacher" ?
          <Link className="mt-4" href="/admin">
            进入学生
            管理界面
          </Link>
          :
          <></>
        }
      </div>
    </div>
  )
}

