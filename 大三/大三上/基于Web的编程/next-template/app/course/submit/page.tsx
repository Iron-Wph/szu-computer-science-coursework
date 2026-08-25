'use client'

import React, { useState, useEffect } from 'react'
import {
  Card,
  CardBody,
  CardHeader,
  Input,
  Button,
  Textarea,
  Switch,
  Select,
  SelectItem,
  useDisclosure,
  Modal,
  ModalBody,
  ModalContent,
  ModalFooter,
  ModalHeader,
} from "@nextui-org/react"
import ImageUploader from '@/components/ImageUploader'
import MyEditor from "@/components/MyEditor"
import { updateCourse,getCourse } from '../../../lib/indexedDB'
import toast from 'react-hot-toast'
import { motion } from 'framer-motion'
// import router from 'next/router'

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

const saveCourse = async (course: Course) => {
  await updateCourse(course)
  toast.success("课程提交成功！")
  window.location.href = "/course"
}

const getCourseInfo = async (courseId: string) => {
  const course = await getCourse(courseId)
  return course
}

// Course submission component
export default function CourseSubmission() {
  const { isOpen, onOpen, onClose } = useDisclosure();
  const [aiSuggestion, setAiSuggestion] = useState("");

  const [course, setCourse] = useState({
    courseId: "",
    courseImageUrl: '',
    numberOfEnrolledStudents: 0,
    courseCategory: '',
    courseName: '',
    publishDate: new Date().toISOString().split('T')[0],
    numberOfLikes: 0,
    discussionArea: [],
    hasDiscussionArea: false,
    hasNoteArea: false,
    enrollmentList: [],
    teacherId: '',
    resourceId: [],
    university: '',
    instructor: '',
    description: '',
    content: '',
    isHomepage: false
  })

  const handleInputChange = (e) => {
    const { name, value } = e.target
    setCourse(prev => ({ ...prev, [name]: value }))
  }

  const handleSwitchChange = (name) => {
    setCourse(prev => ({ ...prev, [name]: !prev[name] }))
  }

  const handleImageUpload = async (e) => {
    const file = e.target.files[0];
    if (!file) return;
  
    const formData = new FormData();
    formData.append('image', file);
  
    try {
      const response = await fetch('http://127.0.0.1:5008/upload_image', {
        method: 'POST',
        body: formData,
      });
  
      const data = await response.json();
  
      if (data.errno === 0) {
        setCourse(prev => ({ ...prev, courseImageUrl: data.data.url }));
        toast.success("图片上传成功！");
      } else {
        toast.error(`图片上传失败: ${data.message}`);
      }
    } catch (error) {
      console.error('图片上传错误:', error);
      toast.error('图片上传失败，请重试。');
    }
  };

  const handleContentChange = (content) => {
    setCourse(prev => ({ ...prev, content }))
  }

  const handleSubmit = async () => {
    console.log(course)
    try {
      await saveCourse(course)
      toast.success('课程提交成功！')
    } catch (error) {
      console.error('提交课程时出错:', error)
      toast.error('提交课程失败。请重试。')
    }
  }

  const handlePreview = async () => {
    try {
      toast.loading("获取AI建议中...")
      // 构建课程数据对象
      const courseData = {
        courseName: course.courseName,
        description: course.description,
        content: course.content,
      };
        // 调用 Flask 后端接口获取 AI 建议
      const response = await fetch('http://127.0.0.1:5008/get_ai_suggestion', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(courseData),
      });
  
      const data = await response.json();
      if (response.ok) {
        // 成功获取 AI 建议
        toast.dismiss()
        setAiSuggestion(data.suggestion);
        onOpen(); // 打开模态框展示建议
      } else {
        toast.dismiss()
        // 处理错误
        console.error('获取AI建议时出错:', data.error);
        toast.success('预览失败，请重试。');
      }
    } catch (error) {
      console.error('请求失败:', error);
      toast.success('预览失败，请重试。');
    }
  };
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
    >
      <Card className="max-w-4xl mx-auto my-8">
        <CardHeader className="flex gap-3">
          <h1 className="text-2xl font-bold">课程提交</h1>
        </CardHeader>
        <CardBody>
          <div className="space-y-6">
            <Input
              label="课程ID"
              name="courseId"
              value={course.courseId}
              onChange={handleInputChange}
            />
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                课程图片
              </label>
              <input
                type="file"
                accept="image/*"
                onChange={handleImageUpload}
                className="block w-full text-sm text-gray-500
                  file:mr-4 file:py-2 file:px-4
                  file:rounded-full file:border-0
                  file:text-sm file:font-semibold
                  file:bg-blue-50 file:text-blue-700
                  hover:file:bg-blue-100"
              />
            </div>
            {course.courseImageUrl && (
              <img
                src={course.courseImageUrl}
                alt="Course"
                className="w-full h-48 object-cover rounded-lg"
              />
            )}
            <Select
              label="课程类别"
              name="courseCategory"
              selectedKeys={[course.courseCategory]}
              onChange={handleInputChange}
            >
              <SelectItem key="Computer Science" value="Computer Science">
                计算机科学
              </SelectItem>
              <SelectItem key="Mathematics" value="Mathematics">
                数学
              </SelectItem>
              <SelectItem key="Physics" value="Physics">
                物理
              </SelectItem>
            </Select>
            <Input
              label="课程名称"
              name="courseName"
              value={course.courseName}
              onChange={handleInputChange}
            />
            <div className="flex justify-between">
              <Switch
                isSelected={course.hasDiscussionArea}
                onValueChange={() => handleSwitchChange("hasDiscussionArea")}
              >
                设置讨论区
              </Switch>
              <Switch
                isSelected={course.hasNoteArea}
                onValueChange={() => handleSwitchChange("hasNoteArea")}
              >
                设置笔记区
              </Switch>
            </div>
            <Input
              label="教师ID"
              name="teacherId"
              value={course.teacherId}
              onChange={handleInputChange}
            />
            <Input
              label="大学"
              name="university"
              value={course.university}
              onChange={handleInputChange}
            />
            <Input
              label="讲师"
              name="instructor"
              value={course.instructor}
              onChange={handleInputChange}
            />
            <Textarea
              label="课程描述"
              name="description"
              value={course.description}
              onChange={handleInputChange}
            />
            <MyEditor initialValue={'请输入课程内容'} onChange={handleContentChange}/>
            <div className="flex gap-4">
              <Button color="primary" onPress={handleSubmit}>
                提交课程
              </Button>
              <Button color="secondary" onPress={handlePreview}>
                预览
              </Button>
            </div>
          </div>
        </CardBody>
      </Card>

      <Modal isOpen={isOpen} onClose={onClose}>
        <ModalContent>
          <ModalHeader>AI 建议</ModalHeader>
          <ModalBody>
            <p>{aiSuggestion}</p>
          </ModalBody>
          <ModalFooter>
            <Button color="primary" onPress={onClose}>
              关闭
            </Button>
          </ModalFooter>
        </ModalContent>
      </Modal>
    </motion.div>
    
  )
}

