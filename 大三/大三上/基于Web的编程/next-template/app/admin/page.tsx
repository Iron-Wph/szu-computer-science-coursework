'use client'

import React, { useState, useEffect } from 'react'
import { Table, TableHeader, TableColumn, TableBody, TableRow, TableCell, User, Chip, Button, Input, Modal, ModalContent, ModalHeader, ModalBody, ModalFooter, Switch } from "@nextui-org/react"
import Image from 'next/image'
import { getUsers, updateUser,getRegistrationStatus, getCourse,getHomepageCourses, updateCourse,getAllCourses, setRegistration } from '../../lib/indexedDB'

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

// 用于测试的模拟数据
const mockUsers: User[] = [
  {
    userId: "1",
    userType: "student", // 用户类型: 学生
    password: "<demo-password>",
    avatarUrl: "https://s1.locimg.com/2024/12/25/4f43ce87187ad.jpg",
    nickname: "John Doe",
    selectedCourses: ["C1", "C2"],
    favoriteCourses: ["C3"],
    passwordErrorCount: 0,
    status: "active", // 用户状态: 激活
    learningHistory: ["H1", "H2"],
    description: "A diligent student", // 描述: 一个勤奋的学生
    content: "Detailed student information" // 内容: 详细的学生信息
  },
  {
    userId: "2",
    userType: "teacher", // 用户类型: 教师
    password: "<demo-password>",
    avatarUrl: "https://s1.locimg.com/2024/12/25/5b9f98ef71be1.jpg",
    nickname: "Prof. Smith",
    selectedCourses: [],
    favoriteCourses: [],
    passwordErrorCount: 0,
    status: "active", // 用户状态: 激活
    learningHistory: [],
    description: "Experienced professor", // 描述: 经验丰富的教授
    content: "Detailed teacher information" // 内容: 详细的教师信息
  }
]
interface Course {
  courseId: string;
  isHomepage: boolean;
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
  resourceId: string[];
  university: string;
  instructor: string;
  description: string;
  content: string;
} 

const mockCourses: Course[] = [
  {
    courseId: "C1",
    courseImageUrl: "https://s1.locimg.com/2024/12/25/52800bfba1d1a.jpg",
    numberOfEnrolledStudents: 50,
    courseCategory: "Computer Science", // 课程类别: 计算机科学
    courseName: "Introduction to Programming", // 课程名称: 编程入门
    publishDate: "2023-01-01",
    numberOfLikes: 100,
    discussionArea: [{ userId: "1", content: "Great course!" }],
    hasDiscussionArea: true,
    hasNoteArea: true,
    enrollmentList: ["1"],
    teacherId: "2",
    resourceId: ["R1"],
    university: "Tech University", // 大学: 科技大学
    instructor: "Prof. Smith", // 教师: Prof. Smith
    description: "A great course", // 描述: 一个伟大的课程
    content: "Detailed course information", // 内容: 详细的课程信息
    isHomepage: true,
  },
  {
    courseId: "C2",
    courseImageUrl: "https://s1.locimg.com/2024/12/25/b772c8e171319.jpg",
    numberOfEnrolledStudents: 30,
    courseCategory: "Mathematics", // 课程类别: 数学
    courseName: "Linear Algebra", // 课程名称: 线性代数
    publishDate: "2023-02-01",
    numberOfLikes: 80,
    discussionArea: [],
    hasDiscussionArea: false,
    hasNoteArea: true,
    enrollmentList: ["1"],
    teacherId: "2",
    resourceId: ["R2"],
    university: "Math College", // 大学: 数学学院
    instructor: "Dr. Johnson", // 教师: Dr. Johnson
    description: "A great course", // 描述: 一个伟大的课程
    content: "Detailed course information", // 内容: 详细的课程信息
    isHomepage: true,
  }
]

// 管理员设置接口
interface AdminSettings {
  homepageCourseIds: string[]; // 主页课程ID
  allowSelfRegistration: boolean; // 允许自助注册
}

// 模拟管理员设置
const mockAdminSettings: AdminSettings = {
  homepageCourseIds: ["C1", "C2"],
  allowSelfRegistration: true
}

// 用于 IndexedDB 的占位符
const indexedDBPlaceholder = {
  getUsers: async () => mockUsers,
  updateUser: async (user: User) => {
    console.log("用户已更新:", user)
    return true
  },
  getCourses: async () => mockCourses,
  getAdminSettings: async () => mockAdminSettings,
  updateAdminSettings: async (settings: AdminSettings) => {
    console.log("管理员设置已更新:", settings)
    return true
  }
}

export default function AdminInterface() {
  // const router = useRouter();
  const [users, setUsers] = useState<User[]>([])
  const [courses, setCourses] = useState<Course[]>([])
  const [editingUser, setEditingUser] = useState<User | null>(null)
  const [isEditModalOpen, setIsEditModalOpen] = useState(false)
  const [homepageCourses, setHomepageCourses] = useState<Course[]>([])
  const [registrationStatus, setRegistrationStatus] = useState(true);

  useEffect(() => {
    // 组件挂载时获取数据
    fetchData()
  }, [])

  const salt = 'your_fixed_salt_here'; // 定义固定盐
  async function hashPassword(password: string): Promise<string> {
    const encoder = new TextEncoder();
    const data = encoder.encode(password + salt); // 将密码和盐组合

    let hashBuffer = await window.crypto.subtle.digest('SHA-256', data); // 使用 SHA-256 哈希
    let hashArray = Array.from(new Uint8Array(hashBuffer)); // 转换为字节数组
    let hash = hashArray.map(b => b.toString(16).padStart(2, '0')).join(''); // 转换为十六进制字符串

    hashBuffer = await window.crypto.subtle.digest('SHA-256', encoder.encode(`${hash}`));
    hashArray = Array.from(new Uint8Array(hashBuffer)); // 转换为字节数组
    hash = hashArray.map(b => b.toString(16).padStart(2, '0')).join(''); // 转换为十六进制字符串
    return `${hash}`; // 返回哈希
  }
  
  const fetchData = async () => {
    const fetchedUsers = await getUsers()
    const fetchedCourses = await getAllCourses()
    const fetchedHomepageCourses = await getHomepageCourses()
    const fetchedRegistrationStatus = await getRegistrationStatus()
    setUsers(fetchedUsers)
    setCourses(fetchedCourses)
    setHomepageCourses(fetchedHomepageCourses)
    setRegistrationStatus(fetchedRegistrationStatus)
  }

  const handleEditUser = (user: User) => {
    setEditingUser(user)
    setIsEditModalOpen(true)
    fetchData() // 更新后刷新数据
  }

  const handleUpdateUser = async () => {
    if (editingUser) {
      updateUser(editingUser)
      setIsEditModalOpen(false)
      fetchData() // 更新后刷新数据
    }
  }

  const handleToggleUserStatus = async (user: User) => {
    const updatedUser = { ...user, status: user.status === 'active' ? 'frozen' : 'active' }
    updateUser(updatedUser)
    fetchData() // 更新后刷新数据
  }

  const handleUpdateCarousel = async (courseId: string) => {
    const course = courses.find(course => course.courseId === courseId);
    if (course) {
      const updatedCourse = { ...course, isHomepage: !course.isHomepage };
      await updateCourse(updatedCourse); // 确保所有属性都有值
      fetchData(); // 更新后刷新数据
    }
  }

  // 切换注册状态
  const handleToggleSelfRegistration = () => {
    console.log("registrationStatus", registrationStatus)
    localStorage.setItem("isRegistrationOpen", (!registrationStatus).toString());
    console.log("isRegistrationOpen", localStorage.getItem("isRegistrationOpen"))
  }

  return (
    <div className="container mx-auto p-4 w-4/5">
      <h1 className="text-2xl font-bold mb-4">管理员界面</h1>

      <div className="mb-8">
        <h2 className="text-xl font-semibold mb-2">全局设置</h2>
        <div className="flex items-center">
          <Switch

            // isSelected={localStorage.getItem("isRegistrationOpen") === "true"}

            checked={registrationStatus}
            onClick={()=>setRegistrationStatus(!registrationStatus)}
            onValueChange={handleToggleSelfRegistration}
          />
          <span className="ml-2">允许自助注册</span>
        </div>
      </div>

      <div className="mb-8">
        <h2 className="text-xl font-semibold mb-2">用户管理</h2>
        <Table aria-label="用户管理表格">
          <TableHeader>
            <TableColumn>用户</TableColumn>
            <TableColumn>类型</TableColumn>
            <TableColumn>状态</TableColumn>
            <TableColumn>操作</TableColumn>
          </TableHeader>
          <TableBody>
            {users.map((user) => (
              <TableRow key={user.userId}>
                <TableCell>
                  <User
                    name={user.nickname}
                    description={user.userId}
                    avatarProps={{ src: user.avatarUrl }}
                  />
                </TableCell>
                <TableCell>{user.userType}</TableCell>
                <TableCell>
                  <Chip color={user.status === 'active' ? 'success' : 'danger'}>
                    {user.status}
                  </Chip>
                </TableCell>
                <TableCell>
                  <Button size="sm" onClick={() => handleEditUser(user)}>编辑</Button>
                  <Button 
                    size="sm" 
                    color={user.status === 'active' ? 'danger' : 'success'}
                    onClick={() => handleToggleUserStatus(user)}
                    className="ml-2"
                  >
                    {user.status === 'active' ? '冻结' : '解冻'}
                  </Button>
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </div>

      <div>
        <h2 className="text-xl font-semibold mb-2">主页轮播图管理</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {courses.map((course) => (
            <div key={course.courseId} className="border p-4 rounded-lg">
              <Image
                src={course.courseImageUrl}
                alt={course.courseName}
                width={300}
                height={200}
                className="w-full h-40 object-cover mb-2 rounded"
              />
              <h3 className="font-semibold">{course.courseName}</h3>
              <p className="text-sm text-gray-600">{course.courseCategory}</p>
              <Button
                size="sm"
                color={homepageCourses.map(course => course.courseId).includes(course.courseId) ? 'primary' : 'default'}
                onClick={() => handleUpdateCarousel(course.courseId)}
                className="mt-2"
              >
                {homepageCourses.map(course => course.courseId).includes(course.courseId) ? '从轮播图中移除' : '添加到轮播图'}
              </Button>
            </div>
          ))}
        </div>
      </div>

      <Modal isOpen={isEditModalOpen} onClose={() => setIsEditModalOpen(false)}>
        <ModalContent>
          {(onClose) => (
            <>
              <ModalHeader>编辑用户</ModalHeader>
              <ModalBody>
                {editingUser && (
                  <>
                    <Input
                      label="昵称"
                      value={editingUser.nickname}
                      onChange={(e) => setEditingUser({ ...editingUser, nickname: e.target.value })}
                    />
                    <Input
                      label="密码"
                      type="password"
                      value={editingUser.password}
                      onChange={async (e) => {
                        const hash = await hashPassword(e.target.value);
                        setEditingUser({ ...editingUser, password: hash.toString() });
                      }}
                    />
                  </>
                )}
              </ModalBody>
              <ModalFooter>
                <Button color="danger" variant="light" onPress={onClose}>
                  取消
                </Button>
                <Button color="primary" onPress={handleUpdateUser}>
                  保存
                </Button>
              </ModalFooter>
            </>
          )}
        </ModalContent>
      </Modal>
    </div>
  )
}