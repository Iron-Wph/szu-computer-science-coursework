'use client'

import React, { useState, useEffect } from 'react'
import {
  Card,
  CardBody,
  CardHeader,
  Input,
  Button,
  Textarea,
  Modal,
  ModalBody,
  ModalContent,
  ModalFooter,
  ModalHeader,
  useDisclosure,
} from "@nextui-org/react"
import ImageUploader from '@/components/ImageUploader'
import { useParams } from 'next/navigation'
import MyEditor from "@/components/MyEditor"
import { updateResource } from '../../../../lib/indexedDB'
import toast from 'react-hot-toast'

interface Resource {
  // 资源ID
  resourceId: string;
  // 资源简介
  description: string;
  // 资源内容
  content: string;
  // 资源图片URL
  imageUrl: string;
  // 课程id
  courseId: string;
}

// IndexedDB 工具函数
const initDB = () => {
  return new Promise((resolve, reject) => {
    const request = indexedDB.open('ResourceDB', 1)
    request.onerror = () => reject("IndexedDB 初始化失败")
    request.onsuccess = () => resolve(request.result)
    request.onupgradeneeded = (event) => {
      const db = event.target.result
      db.createObjectStore('resources', { keyPath: 'resourceId' })
    }
  })
}

const saveResource = async (resource: Resource) => {
  await updateResource(resource)
}

// 资源提交组件
export default function ResourceSubmission() {
  const { isOpen, onOpen, onClose } = useDisclosure();
  const [aiSuggestion, setAiSuggestion] = useState("");

  const { id } = useParams()
  const [resource, setResource] = useState({
    resourceId: "",
    imageUrl: '',
    description: '',
    content: '',
    courseId: id
  })
  const handlePreview = async () => {
    try {
      // 构建课程数据对象
      toast.loading("获取AI建议中...")
      const courseData = {
        description: resource.description,
        content: resource.content,
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
        toast.dismiss()
        toast.success("获取AI建议成功！")
        setAiSuggestion(data.suggestion);
        onOpen(); // 打开模态框展示建议
      } else {
        // 处理错误
        toast.dismiss()
        console.error('获取AI建议时出错:', data.error);
        toast.success('预览失败，请重试。');
      }
    } catch (error) {
      console.error('请求失败:', error);
      toast.success('预览失败，请重试。');
    }
  };
  const handleInputChange = (e) => {
    const { name, value } = e.target
    setResource(prev => ({ ...prev, [name]: value }))
  }

  const handleImageUpload = async (url: string) => {
    console.log('上传的图片URL:', url)
    setResource(prev => ({ ...prev, imageUrl: url }))
  }

  const handleContentChange = (content) => {
    setResource(prev => ({ ...prev, content }))
  }

  const handleSubmit = async () => {
    console.log(resource)
    try {
      await saveResource(resource)
      toast.success('资源提交成功！')
      window.location.href = `/course/${id}`
    } catch (error) {
      console.error('提交资源时出错:', error)
      toast.success('提交资源失败。请重试。')
    }
  }

  return (
    <Card className="max-w-4xl mx-auto my-8">
      <CardHeader className="flex gap-3">
        <h1 className="text-2xl font-bold">资源提交</h1>
      </CardHeader>
      <CardBody>
        <div className="space-y-6">
          <Input
            label="资源ID"
            name="resourceId"
            value={resource.resourceId}
            onChange={handleInputChange}
          />
          <ImageUploader onImageUpload={handleImageUpload} />
          {resource.imageUrl && (
            <img src={resource.imageUrl} alt="Resource" className="w-full h-48 object-cover rounded-lg" />
          )}
          <Textarea
            label="资源简介"
            name="description"
            value={resource.description}
            onChange={handleInputChange}
          />
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">资源内容</label>
            <MyEditor
              initialValue={resource.content}
              onChange={handleContentChange}
            />
          </div>
          <Button color="primary" onPress={handleSubmit}>
            提交资源
          </Button>
          <Button className="mx-4" color="secondary" onPress={handlePreview}>
            预览
          </Button>
        </div>
      </CardBody>
      
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
    </Card>
  )
}