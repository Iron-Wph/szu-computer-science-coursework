'use client'

import { useEffect, useState } from 'react'
import { useParams } from 'next/navigation'
import { Image, Card, CardBody, CardHeader, Divider } from '@nextui-org/react'
import { getResourceById } from '../../../../lib/indexedDB'
// 定义资源接口，基于提供的数据结构
interface Resource {
  resourceId: string;
  description: string;
  content: string;
  imageUrl: string;
  courseId: string;
}

// 模拟从 IndexedDB 中获取数据的函数
const fetchResourceFromIndexedDB = async (id: string): Promise<Resource> => {
  // 模拟异步操作
  await new Promise(resolve => setTimeout(resolve, 1000))
  
  // 返回模拟数据
  return {
    resourceId: id,
    description: '这是一个示例资源描述。',
    content: `
      <h2>示例资源内容</h2>
      <p>这是资源的主要内容，可以包含各种 HTML 元素。</p>
      <ul>
        <li>要点 1</li>
        <li>要点 2</li>
        <li>要点 3</li>
      </ul>
    `,
    imageUrl:"https://s1.locimg.com/2024/12/25/3a93130ee2b09.jpg",
    courseId: "course-123"
  }
}

export default function ResourcePage() {
  const [resource, setResource] = useState<Resource>()
  const [scrollPosition, setScrollPosition] = useState(0)
  // 这个id是课程id
  const { id, resourceId } = useParams()

  useEffect(() => {
    const fetchResource = async () => {
      if (typeof id === 'string' && typeof resourceId === 'string') {
        const fetchedResource = await getResourceById(resourceId)
        setResource(fetchedResource)
      }
    }

    fetchResource()

    const handleScroll = () => {
      const position = window.scrollY
      setScrollPosition(position)
    }

    window.addEventListener('scroll', handleScroll)
    return () => window.removeEventListener('scroll', handleScroll)
  }, [id])

  if (!resource) {
    return <p className="text-center mt-8">加载中...</p>
  }

  return (
    <div className="relative min-h-screen bg-gray-100">
      <div
        className="fixed top-0 left-0 w-full h-screen z-0"
        style={{
          opacity: Math.max(0, 1 - scrollPosition / 500),
        }}
      >
        <Image
          src={resource.imageUrl}
          alt="资源头图"
          classNames={{
            wrapper: "w-full h-full",
            img: "object-cover",
          }}
        />
        <div className="absolute inset-y-0 left-0 w-1/4 bg-gradient-to-r from-black/80 to-transparent" />
        <div className="absolute inset-y-0 right-0 w-1/4 bg-gradient-to-l from-black/80 to-transparent" />
      </div>

      <div className="relative z-10">
        <div className="h-screen flex items-center justify-center">
          <h1 className="text-4xl font-bold text-white">{resource.resourceId}</h1>
        </div>
        <div className="w-full flex-col flex items-center">
          <Card className="w-3/5 max-w-none mx-auto mt-64 bg-white/90">
            <CardHeader className="flex-col items-start px-4 pt-4">
              <h2 className="text-2xl font-bold">描述</h2>
              <p>{resource.description}</p>
            </CardHeader>
            <Divider />
            <CardBody className="px-4 pt-4">
              <h2 className="text-2xl font-bold mb-4">内容</h2>
              <div dangerouslySetInnerHTML={{ __html: resource.content }} />
            </CardBody>
          </Card>
        </div>
      </div>
    </div>
  )
}