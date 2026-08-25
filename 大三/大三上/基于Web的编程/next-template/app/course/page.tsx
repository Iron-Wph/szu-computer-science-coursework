'use client'

import React, { useState, useEffect } from 'react'
import { Input, Checkbox, Chip, Card, CardBody, Image, Pagination, Link } from "@nextui-org/react"
import { Accordion, AccordionItem } from "@nextui-org/react"
import { Search, University } from 'lucide-react'
import { getAllCourses } from '../../lib/indexedDB'
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
}

interface Comment {
  userId: string;
  content: string;
  timestamp: string;
}

type FilterCategory = 'category' | 'university' | 'publishDate' | 'numberOfLikes' | 'numberOfEnrolledStudents';
type FilterOption = { category: FilterCategory; label: string; value: string }
type FilterCategoryOption = {
  title: string;
  category: FilterCategory;
  options: { label: string; value: string; }[];
};

export default function CourseListingPage() {
  const [courses, setCourses] = useState<Course[]>([]);
  const [filteredCourses, setFilteredCourses] = useState<Course[]>([]);
  const [selectedFilters, setSelectedFilters] = useState<FilterOption[]>([]);
  const [searchTerm, setSearchTerm] = useState('');
  const [currentPage, setCurrentPage] = useState(1);
  const [filterCategories, setFilterCategories] = useState<FilterCategoryOption[]>([]);
  const coursesPerPage = 4;
  const currentCourses = filteredCourses.slice(
    (currentPage - 1) * coursesPerPage,
    currentPage * coursesPerPage
  );
  const [comments, setComments] = useState<Comment[]>([]);
  const [newComment, setNewComment] = useState('');

  // 获取所有课程
  useEffect(() => {
    getAllCourses().then((data) => {
      setCourses(data);
      setFilteredCourses(data);
      updateFilterOptions(data);
    });
  }, []);

  const updateFilterOptions = (courses: Course[]) => {
    const categories = new Set(courses.map(course => course.courseCategory));
    const universities = new Set(courses.map(course => course.university));

    const filterCategories: FilterCategoryOption[] = [
      {
        title: '课程类别',
        category: 'category',
        options: Array.from(categories).map(category => ({
          label: category,
          value: category,
        })),
      },
      {
        title: '开课大学',
        category: 'university',
        options: Array.from(universities).map(university => ({
          label: university,
          value: university,
        })),
      },
      {
        title: '发布时间',
        category: 'publishDate',
        options: [
          { label: '升序', value: 'asc' },
          { label: '降序', value: 'desc' },
        ],
      },
      {
        title: '点赞人数',
        category: 'numberOfLikes',
        options: [
          { label: '升序', value: 'asc' },
          { label: '降序', value: 'desc' },
        ],
      },
      {
        title: '选课人数',
        category: 'numberOfEnrolledStudents',
        options: [
          { label: '升序', value: 'asc' },
          { label: '降序', value: 'desc' },
        ],
      },
    ];

    setFilterCategories(filterCategories);
  };

  const handleFilterChange = (filters: FilterOption[], search: string) => {
    setCurrentPage(1); // Reset to first page
    let filtered = courses.filter(course => {
      const matchesSearch = course.courseName.toLowerCase().includes(search.toLowerCase()) ||
                          course.teacherId.toLowerCase().includes(search.toLowerCase());
      const matchesFilters = filters.every(filter => {
        if (filter.category === 'category') {
          return course.courseCategory === filter.value;
        } else if (filter.category === 'university') {
          return course.university === filter.value;
        }
        return true;
      });
      return matchesSearch && matchesFilters;
    });

    filters.forEach(filter => {
      if (filter.category === 'publishDate') {
        filtered = filtered.sort((a, b) => filter.value === 'asc' ? new Date(a.publishDate).getTime() - new Date(b.publishDate).getTime() : new Date(b.publishDate).getTime() - new Date(a.publishDate).getTime());
      } else if (filter.category === 'numberOfLikes') {
        filtered = filtered.sort((a, b) => filter.value === 'asc' ? a.numberOfLikes - b.numberOfLikes : b.numberOfLikes - a.numberOfLikes);
      } else if (filter.category === 'numberOfEnrolledStudents') {
        filtered = filtered.sort((a, b) => filter.value === 'asc' ? a.numberOfEnrolledStudents - b.numberOfEnrolledStudents : b.numberOfEnrolledStudents - a.numberOfEnrolledStudents);
      }
    });

    setFilteredCourses(filtered);
  };

  const handleCommentSubmit = () => {
    if (newComment.trim() === '') return;
    const comment: Comment = {
      userId: 'currentUserId', // Replace with actual user ID
      content: newComment,
      timestamp: new Date().toISOString(),
    };
    setComments([...comments, comment]);
    setNewComment('');
  };

  return (
    <div className="flex min-h-screen w-4/5 mx-auto mt-14">
      {/* Filter Sidebar */}
      <div className="w-1/5 bg-white">
        <div className="p-4">
          <h2 className="text-xl font-semibold mb-4">筛选器</h2>
          <Input
            isClearable
            classNames={{
              base: "mb-6",
              input: "text-small",
            }}
            placeholder="搜索课程或教师"
            startContent={<Search size={18} className="text-default-400" />}
            value={searchTerm}
            onClear={() => {
              setSearchTerm('');
              handleFilterChange(selectedFilters, '');
            }}
            onValueChange={(value) => {
              setSearchTerm(value);
              handleFilterChange(selectedFilters, value);
            }}
          />
          <Accordion 
            className="p-0 gap-1"
            variant="light"
          >
            {filterCategories.map((category) => (
              <AccordionItem 
                key={category.title} 
                aria-label={category.title} 
                title={category.title}
                className="px-0"
              >
                <div className="flex flex-col gap-2 px-1">
                  {category.options.map(({ label, value }) => (
                    <Checkbox
                      key={value}
                      size="sm"
                      onChange={(e) => {
                        let newFilters: FilterOption[];
                        if (e.target.checked) {
                          newFilters = [...selectedFilters, { category: category.category, label, value }];
                        } else {
                          newFilters = selectedFilters.filter(filter => filter.value !== value);
                        }
                        setSelectedFilters(newFilters);
                        handleFilterChange(newFilters, searchTerm);
                      }}
                    >
                      {label}
                    </Checkbox>
                  ))}
                </div>
              </AccordionItem>
            ))}
          </Accordion>
          {(selectedFilters.length > 0 || searchTerm) && (
            <div className="mt-4">
              <h3 className="text-sm font-medium mb-2">已选择的筛选条件</h3>
              <div className="flex flex-wrap gap-2">
                {selectedFilters.map(({ category, label, value }) => (
                  <Chip
                    key={value}
                    size="sm"
                    onClose={() => {
                      const newFilters = selectedFilters.filter(filter => filter.value !== value);
                      setSelectedFilters(newFilters);
                      handleFilterChange(newFilters, searchTerm);
                    }}
                    variant="flat"
                    color={category === 'category' ? 'primary' : 'secondary'}
                  >
                    {label}
                  </Chip>
                ))}
                {searchTerm && (
                  <Chip 
                    size="sm"
                    variant="flat"
                    color="warning" 
                    onClose={() => {
                      setSearchTerm('');
                      handleFilterChange(selectedFilters, '');
                    }}
                  >
                    搜索: {searchTerm}
                  </Chip>
                )}
              </div>
            </div>
          )}
        </div>
      </div>

      {/* Course List */}
      <div className="w-4/5 min-h-screen">
        <div className="flex flex-col gap-4 p-4">
          {currentCourses.map((course) => (
            <Card 
              key={course.courseId} 
              className="w-full h-[160px]"
              isPressable
            >
              <CardBody className="p-0 overflow-hidden">
                <div className="relative w-full h-full">
                  <Image
                    removeWrapper
                    alt={course.courseName}
                    className="z-0 w-full h-full object-cover"
                    src={course.courseImageUrl}
                  />
                  <div className="absolute inset-0 bg-gradient-to-t from-black/90 via-black/50 to-transparent" />
                  <div className="absolute inset-0 p-6 flex flex-col justify-between">
                    <div>
                    <Link href={`/course/${course.courseId}`} className="text-2xl font-bold text-white mb-2">{course.courseName}</Link>
                      <p className="text-base text-gray-300">{course.courseCategory}</p>
                    </div>
                    <div className="space-y-3 flex justify-between">
                      <div className="space-y-2">
                        <p className="text-base text-gray-300">教师ID: {course.teacherId}</p>
                        <p className="text-base text-gray-300">发布日期: {course.publishDate}</p>
                      </div>
                      <div className="flex flex-col text-gray-400">
                        <p className="text-base">已选 {course.numberOfEnrolledStudents}</p>
                        <p className="text-base">点赞 {course.numberOfLikes}</p>
                      </div>
                    </div>
                    
                  </div>
                </div>
              </CardBody>
            </Card>
          ))}
        </div>
        <div className="flex justify-center pb-4">
          <Pagination
            total={Math.ceil(filteredCourses.length / coursesPerPage)}
            page={currentPage}
            onChange={setCurrentPage}
          />
        </div>
      </div>
    </div>
  );
}

