'use client'

import { useState, ChangeEvent } from 'react'
import { Button, Input } from "@nextui-org/react"

interface ImageUploaderProps {
    onImageUpload: (url: string) => void
}

export default function ImageUploader({ onImageUpload }: ImageUploaderProps) {
    const [selectedFile, setSelectedFile] = useState<File | null>(null)
    const [isUploading, setIsUploading] = useState<boolean>(false)

    const handleFileChange = (event: ChangeEvent<HTMLInputElement>) => {
        if (event.target.files && event.target.files[0]) {
            setSelectedFile(event.target.files[0])
        }
    }

    const handleSubmit = async () => {
        if (!selectedFile) {
            toast.success('请选择一个图片文件')
            return
        }
        setIsUploading(true)
        const formData = new FormData()
        formData.append('image', selectedFile)
        try {
            const response = await fetch('http://127.0.0.1:5008/upload_image', {
                method: 'POST',
                body: formData,
            })

            const result = await response.json()

            if (result.errno === 0) {
                onImageUpload(result.data.url)
            } else {
                toast.success(`上传失败: ${result.message}`)
            }
        } catch (error) {
            console.error('错误:', error)
            toast.success('上传图片时发生错误')
        } finally {
            setIsUploading(false)
        }
    }

    return (
        <div className="space-y-4 mt-4">
            <Input
                type="file"
                accept="image/*"
                onChange={handleFileChange}
                className='mt-8'
            />
            <Button 
                color="primary" 
                onPress={handleSubmit}
                disabled={!selectedFile || isUploading}
            >
                {isUploading ? '上传中...' : '上传图片'}
            </Button>
        </div>
    )
}