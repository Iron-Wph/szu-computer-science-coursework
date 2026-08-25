'use client'

import React, { useState, useEffect } from 'react'
import {
  Navbar,
  NavbarBrand,
  NavbarContent,
  NavbarItem,
  Link,
  Button,
  Input,
  Dropdown,
  DropdownTrigger,
  DropdownMenu,
  DropdownItem,
  Spinner,
  Image,
  Card,
  CardBody
} from "@nextui-org/react"
import { Splide, SplideSlide } from '@splidejs/react-splide'
import '@splidejs/react-splide/css'
import { registerCourse, getHomepageCourses,publishHomework, getLatestCourses, getRecommendedCourses, getPopularCourses,setRegistration ,registerUser} from '../lib/indexedDB'
import router from 'next/router'


// 定义课程接口
interface Course {
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
  resourceId: string[];
  university: string;
  instructor: string;
  description: string;
  content: string;
} 

// 生成模拟课程数据
async function getCoursesFromDB(): Promise<Course[]> {
  const categories = ['编程', '设计', '商业', '市场营销', '科学', 'Computer Science'];
  const universities = ['北京大学', '清华大学', '复旦大学', '上海交通大学', '浙江大学'];
  const imageUrls = [
    'https://s1.locimg.com/2024/12/25/4f43ce87187ad.jpg',
    'https://s1.locimg.com/2024/12/25/5b9f98ef71be1.jpg',
    'https://s1.locimg.com/2024/12/25/52800bfba1d1a.jpg',
    'https://s1.locimg.com/2024/12/25/b772c8e171319.jpg',
    'https://s1.locimg.com/2024/12/25/3a93130ee2b09.jpg'
  ];

  for (let i = 0; i < 20; i++) {
    await registerCourse(
      `课程 ${i + 1}`,
      categories[Math.floor(Math.random() * categories.length)],
      `teacher-${Math.floor(Math.random() * 10) + 1}`,
      true,
      true,
      new Date(Date.now() - Math.random() * 10000000000).toISOString(),
      imageUrls[i % 5],
      universities[Math.floor(Math.random() * universities.length)],
      `讲师 ${i + 1}`,
      `课程简介 ${i + 1}`,
      `课程内容 ${i + 1}`
    );

    
    // 发布作业
    await publishHomework(
      `课程 ${i + 1}`,
      `作业 ${i + 1}`,
      '2023-12-01',
      '2023-12-31',
      `作业简介 ${i + 1}`
    );

  }
  const courses: Course[] = await getLatestCourses();
  return courses;
}

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

// 生成模拟用户
async function getUsersFromDB(){
  for(let i = 0; i < 20; i++){
    await registerUser(
      `student`,
      `user-${i + 1}`,
      await hashPassword(`password-${i + 1}`)
    );
  }

  await registerUser(
    `teacher`,
    `teacher-1`,
    await hashPassword(`123456`),
  );
  await registerUser(
    `teacher`,
    `teacher-2`,
    await hashPassword(`123456`),
  );
  await registerUser(
    `teacher`,
    `admin-s`,
    await hashPassword(`123456`),
  );
}


export default function Home() {

  const [latestCourses, setLatestCourses] = useState<Course[]>([]);
  const [recommendedCourses, setRecommendedCourses] = useState<Course[]>([]);
  const [popularCourses, setPopularCourses] = useState<Course[]>([]);
  const [filteredCoursesLatest, setFilteredCoursesLatest] = useState<Course[]>([]);
  const [filteredCoursesRecommended, setFilteredCoursesRecommended] = useState<Course[]>([]);
  const [filteredCoursesPopular, setFilteredCoursesPopular] = useState<Course[]>([]);
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedCategory, setSelectedCategory] = useState('全部');
  const [isLoading, setIsLoading] = useState(true);
  const [homepageCourses, setHomepageCourses] = useState<Course[]>([]);

  // 获取首页课程
  useEffect(() => {
    getHomepageCourses().then((data) => {
      setHomepageCourses(data);
    });
  }, []);

  // 获取最新课程
  useEffect(() => {
    // // note: 初始化
    // getCoursesFromDB();
    // getUsersFromDB();
    // setRegistration(true); 

    getLatestCourses().then((data) => {
      setLatestCourses(data);
      setIsLoading(false);
    });
  }, []);

  // 获取推荐课程
  useEffect(() => {
    getRecommendedCourses().then((data) => {
      setRecommendedCourses(data);
      setIsLoading(false);
    });
  }, []);

  // 获取热门课程
  useEffect(() => {
    getPopularCourses().then((data) => {
      setPopularCourses(data);
      setIsLoading(false);
    });
  }, []);

  // 过滤最新课程
  useEffect(() => {
    let filtered = latestCourses;
    if (searchTerm) {
      filtered = filtered.filter(latestCourse =>
        latestCourse.courseName.toLowerCase().includes(searchTerm.toLowerCase()) ||
        latestCourse.courseCategory.toLowerCase().includes(searchTerm.toLowerCase())
      );
    }
    if (selectedCategory !== '全部') {
      filtered = filtered.filter(latsetcourse => latsetcourse.courseCategory === selectedCategory);
    }
    setFilteredCoursesLatest(filtered);
  }, [latestCourses, searchTerm, selectedCategory]);

  // 过滤推荐课程
  useEffect(() => {
    let filtered = recommendedCourses;
    if (searchTerm) {
      filtered = filtered.filter(recommendedCourse =>
        recommendedCourse.courseName.toLowerCase().includes(searchTerm.toLowerCase()) ||
        recommendedCourse.courseCategory.toLowerCase().includes(searchTerm.toLowerCase())
      );
    }
    if (selectedCategory !== '全部') {
      filtered = filtered.filter(recommendedCourse => recommendedCourse.courseCategory === selectedCategory);
    }
    setFilteredCoursesRecommended(filtered);
  }, [recommendedCourses, searchTerm, selectedCategory]);

  // 过滤热门课程
  useEffect(() => {
    let filtered = popularCourses;
    if (searchTerm) {
      filtered = filtered.filter(popularCourse =>
        popularCourse.courseName.toLowerCase().includes(searchTerm.toLowerCase()) ||
        popularCourse.courseCategory.toLowerCase().includes(searchTerm.toLowerCase())
      );
    }
    if (selectedCategory !== '全部') {
      filtered = filtered.filter(popularCourse => popularCourse.courseCategory === selectedCategory);
    }
    setFilteredCoursesPopular(filtered);
  }, [popularCourses, searchTerm, selectedCategory]);

  // 提取所有课程的类别
  const categories = ['全部', ...new Set([...latestCourses, ...recommendedCourses, ...popularCourses].map(course => course.courseCategory))];

  if (isLoading) {
    return (
      <div className="flex justify-center items-center h-screen">
        <Spinner size="lg" color="primary" />
        <span className="ml-2 text-lg">加载中...</span>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-100">
      <main className="container mx-auto px-4 py-8">
        <section className="mb-8">
          <h1 className="text-4xl font-bold mb-4">欢迎来到我们的课程平台</h1>
          <p className="text-xl text-gray-600">在这里，知识触手可及。</p>
        </section>

        {/* 主轮播图 */}
        <section className="mb-8">
          <Splide
            options={{
              type: 'loop',
              perPage: 1,
              autoplay: true,
              interval: 5000,
              arrows: true,
              pagination: true,
              height: '400px',
            }}
          >
            {homepageCourses.map((course, index) => (
              <SplideSlide key={index} className="h-full">
                <div className="relative w-full h-full">
                    <img
                      src={course.courseImageUrl}
                      alt={course.courseName}
                      className="absolute inset-0 w-full h-full object-cover"
                  />
                  <div className="absolute inset-0 bg-black bg-opacity-50 flex flex-col justify-end p-6">
                    <Link className="text-3xl font-bold text-white mb-2" href={`/course/${course.courseId}`}>{course.courseName}</Link>
                    <Link className="text-xl text-white mb-1" href={`/course/${course.courseId}`}>{course.university}</Link>
                    <Link className="text-lg text-white mb-4" href={`/course/${course.courseId}`}>讲师: {course.instructor}</Link>
                  </div>
                </div>
              </SplideSlide>
            ))}
          </Splide>
        </section>

        <section className="mb-8">
          <div className="flex justify-between items-center mb-4">
            <Input
              placeholder="搜索课程..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="max-w-xs"
            />
            <Dropdown>
              <DropdownTrigger>
                <Button variant="bordered">
                  {selectedCategory || '选择类别'}
                </Button>
              </DropdownTrigger>
              <DropdownMenu
                aria-label="类别选择"
                selectionMode="single"
                selectedKeys={new Set([selectedCategory])}
                onSelectionChange={(keys) => setSelectedCategory(Array.from(keys)[0] as string)}
              >
                {categories.map((category) => (
                  <DropdownItem key={category}>{category}</DropdownItem>
                ))}
              </DropdownMenu>
            </Dropdown>
          </div>

          {/* 最新课程 */}
          <div className="mb-8">
            <h3 className="mb-4 text-xl font-semibold">最新课程</h3>
            <Splide
              options={{
                type: 'loop',   perPage: 4,  gap: '1rem', pagination: false,
                arrows: true,   autoplay: true,  interval: 3000,
                breakpoints: {
                  1024: { perPage: 3 },
                  768: { perPage: 2 },
                  640: { perPage: 1 }
                }
              }}
            >
              {filteredCoursesLatest.slice(0, 8).map((course) => (
                <SplideSlide key={course.courseId}>
                  <Card className="h-full">
                    <CardBody className="p-0">
                      <Image
                        src={course.courseImageUrl}
                        alt={course.courseName}
                        className="h-40 w-full object-cover"
                      />
                      <div className="p-3">
                        <Link href={`/course/${course.courseId}`}  className="mb-1 line-clamp-2 text-sm font-semibold">
                          {course.courseName}
                        </Link>
                        <p className="text-xs text-default-500">
                          {course.university} / {course.instructor}
                        </p>
                      </div>
                    </CardBody>
                  </Card>
                </SplideSlide>
              ))}
            </Splide>
          </div>

          {/* 推荐课程 */}
          <div className="mb-8">
            <h3 className="mb-4 text-xl font-semibold">推荐课程</h3>
            <Splide
              options={{
                type: 'loop',
                perPage: 4,
                gap: '1rem',
                pagination: false,
                arrows: true,
                autoplay: true,
                interval: 3000,
                breakpoints: {
                  1024: { perPage: 3 },
                  768: { perPage: 2 },
                  640: { perPage: 1 }
                }
              }}
            >
              {homepageCourses.slice(0, 8).map((course) => (
                <SplideSlide key={course.courseId}>
                  <Card className="h-full">
                    <CardBody className="p-0">
                      <Image
                        src={course.courseImageUrl}
                        alt={course.courseName}
                        className="h-40 w-full object-cover"
                      />
                      <div className="p-3">
                        <Link href={`/course/${course.courseId}`} className="mb-1 line-clamp-2 text-sm font-semibold">
                          {course.courseName}
                        </Link>
                        <p className="text-xs text-default-500">
                          {course.university} / {course.instructor}
                        </p>
                      </div>
                    </CardBody>
                  </Card>
                </SplideSlide>
              ))}
            </Splide>
          </div>

          {/* 热门课程 */}
          <div className="mb-8">
            <h3 className="mb-4 text-xl font-semibold">热门课程</h3>
            <Splide
              options={{
                type: 'loop',
                perPage: 4,
                gap: '1rem',
                pagination: false,
                arrows: true,
                autoplay: true,
                interval: 3000,
                breakpoints: {
                  1024: { perPage: 3 },
                  768: { perPage: 2 },
                  640: { perPage: 1 }
                }
              }}
            >
              {filteredCoursesPopular.slice(0, 8).map((course) => (
                <SplideSlide key={course.courseId}>
                  <Card className="h-full">
                    <CardBody className="p-0">
                      <Image
                        src={course.courseImageUrl}
                        alt={course.courseName}
                        className="h-40 w-full object-cover"
                      />
                      <div className="p-3">
                        <Link href={`/course/${course.courseId}`}  className="mb-1 line-clamp-2 text-sm font-semibold">
                          {course.courseName}
                        </Link>
                        <p className="text-xs text-default-500">
                          {course.university} / {course.instructor}
                        </p>
                      </div>
                    </CardBody>
                  </Card>
                </SplideSlide>
              ))}
            </Splide>
          </div>
        </section>
      </main>

      <footer className="bg-gray-100 text-black py-8">
        <div className="container mx-auto px-4">
          <div className="flex flex-wrap justify-between">
            <div className="w-full md:w-1/3 mb-6 md:mb-0">
              <h3 className="text-xl font-bold mb-2">课程平台</h3>
              <p>为全球学者赋能</p>
            </div>
            <div className="w-full md:w-1/3 mb-6 md:mb-0">
              <h4 className="text-lg font-semibold mb-2">快速链接</h4>
              <ul>
                <li><a href="#" className="hover:text-gray-300">关于我们</a></li>
                <li><a href="#" className="hover:text-gray-300">联系我们</a></li>
                <li><a href="#" className="hover:text-gray-300">隐私政策</a></li>
              </ul>
            </div>
            <div className="w-full md:w-1/3">
              <h4 className="text-lg font-semibold mb-2">关注我们</h4>
              <p>在社交媒体上关注我们，获取最新更新！</p>
            </div>
          </div>
        </div>
      </footer>
    </div>
  )
}

