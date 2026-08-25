"use client";

import React, { useEffect, useState } from "react";
import { useParams, useRouter } from "next/navigation";
import {
  Tabs,
  Tab,
  Button,
  Card,
  CardBody,
  Accordion,
  AccordionItem,
  Link,
  Image,
  Avatar,
  Textarea,
  Dropdown,
  DropdownTrigger,
  DropdownMenu,
  DropdownItem,
  Spinner,
  useDisclosure,
  Input,
  Modal,
  ModalBody,
  ModalContent,
  ModalFooter,
  ModalHeader,
} from "@nextui-org/react";
import {
  BookOpen,
  Bell,
  Newspaper,
  CheckSquare,
  MessageSquare,
  Calendar,
  Users,
  ThumbsUp,
  MoreVertical,
  Flag,
} from "lucide-react";
import {
  getCourseById,
  registerCourse,
  getCourse,
  publishHomework,
  isFavourite,
  addFavouriteCourse,
  addNote,
  addComment,
  removeFavouriteCourse,
  deleteCourse,
  unenrollFromCourse,
  isEnrolled,
  getAnnouncementsByCourseId,
  getResourcesByCourseId,
  addAnnouncement,
  getHomeworksByCourseId,
  enrollInCourse,
  getUser,
  deleteComment,
} from "../../../lib/indexedDB";
import MyEditor from "@/components/MyEditor";
import toast from "react-hot-toast";

// -----------------------------------
// Data Structures
// -----------------------------------

interface Course {
  courseId: string;
  courseImageUrl: string;
  numberOfEnrolledStudents: number;
  courseCategory: string;
  courseName: string;
  publishDate: string;
  numberOfLikes: number;
  discussionArea: { userId: string; content: string; time: string }[];
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

interface User {
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
}

interface Announcement {
  announcementId: string;
  courseId: string;
  announcementTime: string;
  announcementTitle: string;
  announcementContent: string;
}

interface Homework {
  homeworkId: string;
  homeworkName: string;
  courseId: string;
  startTime: string;
  dueTime: string;
  description: string;
  studentList: string[];
  completedList: string[];
  isDue: boolean;
}

interface Resource {
  resourceId: string;
  description: string;
  content: string;
  imageUrl: string;
  courseId: string;
}

interface Exam {
  examId: string;
  questionIds: string[];
  creatorId: string;
  creatorType: string;
}

// -----------------------------------
// IndexedDB Interaction Interfaces
// -----------------------------------

// Placeholder functions for IndexedDB interactions.
// These should be implemented to interact with IndexedDB appropriately.

const getDataFromIndexedDB = async (storeName: string, key: string) => {
  // TODO: Implement data retrieval from IndexedDB
  return null;
};

const setDataToIndexedDB = async (storeName: string, key: string, data: any) => {
  // TODO: Implement data storage to IndexedDB
};

// -----------------------------------
// Test Data Generation
// -----------------------------------

const generateTestCourse = (): Course => ({
  courseId: "course-123",
  courseImageUrl: "https://s1.locimg.com/2024/12/25/4f43ce87187ad.jpg",
  numberOfEnrolledStudents: 150,
  courseCategory: "Computer Science",
  courseName: "Introduction to Programming",
  publishDate: "2024-01-15",
  numberOfLikes: 250,
  discussionArea: [
    { userId: "user-1", content: "Great course!", time: "2024-04-20T10:00:00Z" },
    { userId: "user-2", content: "Looking forward to the next module.", time: "2024-04-21T12:30:00Z" },
  ],
  hasDiscussionArea: true,
  hasNoteArea: true,
  enrollmentList: ["user-1", "user-2", "user-3"],
  teacherId: "teacher-1",
  resourceId: ["resource-1", "resource-2"],
  university: "北京大学",
  instructor: "张三",
  description: "这是一门关于编程的课程，涵盖了编程的基本概念和实践 用。",
  content: "课程内容包括编程基础、数据结构、算法设计等。",
});

const generateTestTeacher = (): User => ({
  userType: "teacher",
  userId: "teacher-1",
  password: "<demo-password>",
  avatarUrl: "https://s1.locimg.com/2024/12/25/5b9f98ef71be1.jpg",
  nickname: "Dr. Smith",
  selectedCourses: ["course-123"],
  favoriteCourses: [],
  passwordErrorCount: 0,
  status: "active",
  learningHistory: [],
});

const generateTestResources = (): Resource[] => [
  {
    resourceId: "resource-1",
    description: "Lecture Slides for Week 1",
    content: "Content of Lecture Slides Week 1",
    imageUrl: "https://s1.locimg.com/2024/12/25/4f43ce87187ad.jpg",
    courseId: "course-123",
  },
  {
    resourceId: "resource-2",
    description: "Programming Assignment 1",
    content: "Details of Programming Assignment 1",
    imageUrl: "https://s1.locimg.com/2024/12/25/4f43ce87187ad.jpg",
    courseId: "course-123",
  },
];

// -----------------------------------
// HomeworkModal Component
// -----------------------------------

export function HomeworkModal() {
  const { isOpen, onOpen, onOpenChange } = useDisclosure();
  const [homeworkTitle, setHomeworkTitle] = useState("");
  const [homeworkContent, setHomeworkContent] = useState("");
  const [dueTime, setDueTime] = useState("");
  const { id } = useParams(); // Get course ID from URL

  const handleHomeWorkPublish = async () => {
    if (!id) {
      toast.error("课程ID无效！");
      return;
    }

    const course = await getCourse(id);
    if (!course) {
      toast.error("课程不存在！");
      return;
    }

    try {
      await publishHomework(course.courseName, homeworkTitle, new Date().toISOString(), dueTime, homeworkContent);
      toast.success("作业发布成功！");
      window.location.reload();
    } catch (error) {
      console.error("发布作业失败:", error);
      toast.error("发布作业失败，请重试。");
    }
  };

  return (
    <>
      <Button color="default" onPress={onOpen}>
        发布作业
      </Button>
      <Modal isOpen={isOpen} placement="top-center" onOpenChange={onOpenChange}>
        <ModalContent>
          {(onClose) => (
            <>
              <ModalHeader className="flex flex-col gap-1">发布作业</ModalHeader>
              <ModalBody>
                <Input
                  label="作业标题"
                  placeholder="请输入作业的标题"
                  variant="bordered"
                  value={homeworkTitle}
                  onChange={(e) => setHomeworkTitle(e.target.value)}
                />
                <Textarea
                  label="作业内容"
                  placeholder="请输入本次作业的内容"
                  value={homeworkContent}
                  onChange={(e) => setHomeworkContent(e.target.value)}
                />
                <Input
                  label="截止时间"
                  type="datetime-local"
                  value={dueTime}
                  onChange={(e) => setDueTime(e.target.value)}
                />
              </ModalBody>
              <ModalFooter>
                <Button color="danger" variant="flat" onPress={onClose}>
                  关闭
                </Button>
                <Button color="primary" onPress={handleHomeWorkPublish}>
                  发布
                </Button>
              </ModalFooter>
            </>
          )}
        </ModalContent>
      </Modal>
    </>
  );
}

// -----------------------------------
// CourseDetailPage Component
// -----------------------------------

export default function CourseDetailPage() {
  const { id } = useParams(); // Get course ID from URL
  const router = useRouter();
  const [course, setCourse] = useState<Course | null>(null);
  const [teacher, setTeacher] = useState<User | null>(null);
  const [resources, setResources] = useState<Resource[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);
  const { isOpen, onOpen, onOpenChange } = useDisclosure();
  const [announcementTitle, setAnnouncementTitle] = useState("");
  const [announcementContent, setAnnouncementContent] = useState("");
  const [announcements, setAnnouncements] = useState<Announcement[]>([]);
  const [homeworks, setHomeworks] = useState<Homework[]>([]);
  const [isEnroll, setIsEnrolled] = useState(false);
  const [isFavouriteState, setIsFavouriteState] = useState(false);
  const [newComment, setNewComment] = useState("");
  const [newNote, setNewNote] = useState("");
  const [userAvatars, setUserAvatars] = useState<{ [key: string]: string }>({});

  useEffect(() => {
    const fetchData = async () => {
      try {
        if (!id) {
          setError("课程ID无效。");
          setLoading(false);
          return;
        }

        // Fetch course data
        const storedCourse = await getCourseById(id);
        if (storedCourse) {
          setCourse(storedCourse);
        } else {
          const testCourse = generateTestCourse();
          setCourse(testCourse);
          // await setDataToIndexedDB("courses", id, testCourse);
        }

        // Fetch teacher data
        const teacherId = storedCourse ? storedCourse.teacherId : "teacher-1";
        const storedTeacher = await getUser(teacherId);
        if (storedTeacher) {
          setTeacher(storedTeacher);
        } else {
          const testTeacher = generateTestTeacher();
          setTeacher(testTeacher);
          // await setDataToIndexedDB("users", "teacher-1", testTeacher);
        }

        // Fetch announcements
        const storedAnnouncements = await getAnnouncementsByCourseId(id);
        if (storedAnnouncements) {
          setAnnouncements(storedAnnouncements);
        }

        // Fetch resources
        const storedResources = await getResourcesByCourseId(id);
        if (storedResources) {
          setResources(storedResources);
        } else {
          const testResources = generateTestResources();
          setResources(testResources);
          // await setDataToIndexedDB("resources", id, testResources);
        }

        // Fetch homeworks
        const storedHomeworks = await getHomeworksByCourseId(id);
        if (storedHomeworks) {
          setHomeworks(storedHomeworks);
        }

        // Check enrollment
        const username = localStorage.getItem("username");
        if (username && await isEnrolled(username, id)) {
          setIsEnrolled(true);
        }

        // Check if favorite
        if (username) {
          const user = await getUser(username);
          if (user) {
            setIsFavouriteState(user.favoriteCourses.includes(id));
          }
        }

        // Fetch user avatars for comments
        if (storedCourse && storedCourse.discussionArea.length > 0) {
          const avatars: { [key: string]: string } = {};
          for (const comment of storedCourse.discussionArea) {
            if (!avatars[comment.userId]) {
              const user = await getUser(comment.userId);
              avatars[comment.userId] = user ? user.avatarUrl : "";
            }
          }
          setUserAvatars(avatars);
        }

        setLoading(false);
      } catch (err) {
        console.error("Failed to load course data:", err);
        setError("Failed to load course data.");
        setLoading(false);
      }
    };

    fetchData();
  }, [id]);

  // Handle Note Submission
  const handleNoteSubmit = async () => {
    if (newNote.trim() === "") {
      toast.error("笔记不能为空!");
      return;
    }
    const userId = localStorage.getItem("userId") || "";
    if (!userId) {
      toast.error("请先登录!");
      return;
    }
    try {
      await addNote({
        userId: userId,
        content: newNote,
        time: new Date().toISOString(),
        courseId: id || "",
      });
      toast.success("笔记提交成功！");
      setNewNote("");
      window.location.reload();
    } catch (error) {
      console.error("提交笔记失败:", error);
      toast.error("提交笔记失败，请重试。");
    }
  };

  // Handle Comment Submission
  const handleCommentSubmit = async () => {
    if (newComment.trim() === "") {
      toast.error("评论不能为空!");
      return;
    }
    const username = localStorage.getItem("username");
    if (!username) {
      toast.error("请先登录!");
      return;
    }
    try {
      const comment = {
        userId: username,
        content: newComment,
        time: new Date().toISOString(),
      };
      await addComment(comment, id || "");
      toast.success("评论成功！");
      setNewComment("");
      window.location.reload();
    } catch (error) {
      console.error("发表评论失败:", error);
      toast.error("发表评论失败，请重试。");
    }
  };

  const handleDeleteComment = async (userId: string,courseId: string) => {
    await deleteComment(userId,courseId);
    toast.success("删除评论成功！");
    window.location.reload();
  };

  // Handle Homework Click
  const handleHomeworkClick = (homeworkId: string) => {
    if (id && homeworkId) {
      router.push(`/course/${id}/homework/${homeworkId}`);
    } else {
      console.error("课程 ID 或作业 ID 无效");
    }
  };

  // Handle Course Deletion
  const handleDelete = async () => {
    if (!id) {
      toast.error("课程ID无效！");
      return;
    }
    try {
      await deleteCourse(id);
      toast.success("删除课程成功！");
      router.push("/courses"); // Redirect to courses list or another appropriate page
    } catch (error) {
      console.error("删除课程失败:", error);
      toast.error("删除课程失败，请重试。");
    }
  };

  // Handle Favourite
  const handleFavourite = async () => {
    const username = localStorage.getItem("username");
    if (!username) {
      toast.error("请先登录!");
      return;
    }
    try {
      await addFavouriteCourse(username, id || "");
      setIsFavouriteState(true);
      toast.success("收藏课程成功！");
    } catch (error) {
      console.error("收藏课程失败:", error);
      toast.error("收藏课程失败，请重试。");
    }
  };

  // Handle Unfavourite
  const handleUnfavourite = async () => {
    const username = localStorage.getItem("username");
    if (!username) {
      toast.error("请先登录!");
      return;
    }
    try {
      await removeFavouriteCourse(username, id || "");
      setIsFavouriteState(false);
      toast.success("取消收藏成功！");
    } catch (error) {
      console.error("取消收藏失败:", error);
      toast.error("取消收藏失败，请重试。");
    }
  };

  // Handle Publish Announcement
  const handlePublish = async () => {
    if (!id) {
      toast.error("课程ID无效！");
      return;
    }
    try {
      const announcement = {
        announcementId: "announcement" + new Date().getTime(),
        courseId: id,
        announcementTitle: announcementTitle,
        announcementContent: announcementContent,
        announcementTime: new Date().toISOString(),
      };
      await addAnnouncement(announcement);
      toast.success("公告发布成功！");
      setAnnouncementTitle("");
      setAnnouncementContent("");
      onOpenChange(false);
      window.location.reload();
    } catch (error) {
      console.error("发布公告失败:", error);
      toast.error("发布公告失败，请重试。");
    }
  };

  // Handle Unenroll from Course
  const handleUnselectCourse = async () => {
    const username = localStorage.getItem("username");
    if (!username) {
      toast.error("请先登录!");
      return;
    }
    try {
      const res = await unenrollFromCourse(username, id || "");
      if (res.success) {
        toast.success("退选成功!");
        setIsEnrolled(false);
      } else {
        toast.error(res.message);
      }
    } catch (error) {
      console.error("退选课程失败:", error);
      toast.error("退选课程失败，请重试。");
    }
  };

  // Handle Enroll in Course
  const handleSelectCourse = async () => {
    const username = localStorage.getItem("username");
    if (!username) {
      toast.error("请先登录!");
      return;
    }
    try {
      const res = await enrollInCourse(username, id || "");
      if (res.success) {
        toast.success("选课成功!");
        setIsEnrolled(true);
      } else {
        toast.error(res.message);
      }
    } catch (error) {
      console.error("选课失败:", error);
      toast.error("选课失败，请重试。");
    }
  };

  // Handle Avatar Fetching (if additional user data is needed)
  // This can be expanded based on requirements

  if (loading) {
    return (
      <div className="flex justify-center items-center h-screen">
        <Spinner size="lg" />
      </div>
    );
  }

  if (error || !course || !teacher) {
    return (
      <div className="text-red-500 text-center mt-10">
        {error || "Course not found."}
      </div>
    );
  }

  return (
    <div className="max-w-6xl mx-auto px-4 py-8">
      {/* Header Section */}
      <div className="flex flex-col md:flex-row justify-between items-start md:items-center py-4">
        <h1 className="text-3xl font-bold mb-4 md:mb-0">{course.courseName}</h1>
        <div className="flex flex-col md:flex-row items-start md:items-center gap-4">
          <div className="text-sm text-gray-600">
            <span>选课阶段</span>
            <div>
              {course.publishDate} ~ {/* Replace with actual enrollment end date if available */}
              2024-12-31
            </div>
            <div className="text-gray-400">选课进行中</div>
          </div>
          {localStorage.getItem("role") === "student" ? (
            !isEnroll ? (
              <Button
                color="primary"
                className="bg-[#4CAF50] text-white"
                onClick={handleSelectCourse}
                disabled={false} // Replace with actual state if needed
              >
                选择课程
              </Button>
            ) : (
              <Button
                color="danger"
                className="text-white"
                onClick={handleUnselectCourse}
                disabled={false} // Replace with actual state if needed
              >
                退选课程
              </Button>
            )
          ) : (
            <></>
          )}
          {localStorage.getItem("role") === "teacher" &&
            localStorage.getItem("userId") === course.teacherId && (
              <Button
                color="danger"
                className="bg-[#4CAF50] text-white"
                onClick={handleDelete}
                disabled={false} // Replace with actual state if needed
              >
                删除课程
              </Button>
            )}
          {localStorage.getItem("role") === "student" && (
            !isFavouriteState ? (
              <Button
                color="primary"
                className="text-white"
                onClick={handleFavourite}
                disabled={false} // Replace with actual state if needed
              >
                收藏课程
              </Button>
            ) : (
              <Button
                color="danger"
                className="text-white"
                onClick={handleUnfavourite}
                disabled={false} // Replace with actual state if needed
              >
                取消收藏
              </Button>
            )
          )}
        </div>
      </div>

      {/* Course Image */}
      <div className="mb-8">
        <Image
          src={course.courseImageUrl}
          alt={course.courseName}
          className="w-full h-full object-cover rounded-lg shadow-md transition-transform duration-500"
        />
      </div>

      {/* Tabs Section */}
      <Tabs
        aria-label="Course sections"
        color="primary"
        variant="underline"
        classNames={{
          tabList: "gap-6 w-full",
          cursor: "w-full",
        }}
      >
        {/* Course Information Tab */}
        <Tab
          key="course-info"
          title={
            <div className="flex items-center gap-2">
              <BookOpen className="w-4 h-4" />
              <span>课程信息</span>
            </div>
          }
        >
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-8 mt-8">
            {/* Left Section: Course Details */}
            <div className="lg:col-span-2">
              <Card className="p-6 shadow-lg">
                <h2 className="text-2xl font-semibold mb-4">课程描述</h2>
                <p className="text-gray-700 mb-6">{course.description}</p>

                <h2 className="text-2xl font-semibold mb-4">课程详情</h2>
                <ul className="list-disc list-inside text-gray-700 space-y-2">
                  <li>
                    <strong>类别:</strong> {course.courseCategory}
                  </li>
                  <li>
                    <strong>发布日期:</strong> {course.publishDate}
                  </li>
                  <li>
                    <strong>点赞数:</strong> {course.numberOfLikes}
                  </li>
                  <li>
                    <strong>选课人数:</strong> {course.numberOfEnrolledStudents}
                  </li>
                </ul>
              </Card>
            </div>

            {/* Right Section: Teacher Info */}
            <div className="lg:col-span-1">
              <Card className="p-4 shadow-lg">
                <h2 className="text-xl font-semibold mb-4">授课教师</h2>
                <div className="flex items-center space-x-4">
                  <Avatar src={teacher.avatarUrl} alt={teacher.nickname} size="lg" />
                  <div>
                    <p className="font-bold">{teacher.nickname}</p>
                    {/* Replace with actual teacher email if available */}
                    <p className="text-gray-600">Email: teacher@example.com</p>
                  </div>
                </div>

                <h2 className="text-xl font-semibold mt-6 mb-4">开课院系</h2>
                <p className="text-gray-700">{course.courseCategory}</p>
              </Card>
            </div>
          </div>
        </Tab>

        {/* Announcements Tab */}
        <Tab
          key="announcements"
          title={
            <div className="flex items-center gap-2">
              <Bell className="w-4 h-4" />
              <span>通知公告</span>
            </div>
          }
        >
          <div className="mt-2">
            <>
              {localStorage.getItem("role") === "teacher" && (
                <Button color="default" onPress={onOpen}>
                  发布公告
                </Button>
              )}
              <Modal isOpen={isOpen} placement="top-center" onOpenChange={onOpenChange}>
                <ModalContent>
                  {(onClose) => (
                    <>
                      <ModalHeader className="flex flex-col gap-1">
                        发布公告
                      </ModalHeader>
                      <ModalBody>
                        <Input
                          label="公告标题"
                          placeholder="请输入公告的标题"
                          variant="bordered"
                          value={announcementTitle}
                          onChange={(e) => setAnnouncementTitle(e.target.value)}
                        />
                        <Textarea
                          label="公告内容"
                          placeholder="请输入本次公告的内容"
                          value={announcementContent}
                          onChange={(e) => setAnnouncementContent(e.target.value)}
                        />
                      </ModalBody>
                      <ModalFooter>
                        <Button color="danger" variant="flat" onPress={onClose}>
                          关闭
                        </Button>
                        <Button color="primary" onPress={handlePublish}>
                          发布
                        </Button>
                      </ModalFooter>
                    </>
                  )}
                </ModalContent>
              </Modal>
            </>
            <Card className="p-4 shadow-lg">
              <Accordion>
                {announcements && announcements.length > 0 ? (
                  announcements.map((announcement) => (
                    <AccordionItem
                      key={announcement.announcementId}
                      aria-label={announcement.announcementTitle}
                      title={announcement.announcementTitle}
                      subtitle={new Date(announcement.announcementTime).toLocaleString()}
                    >
                      {announcement.announcementContent}
                    </AccordionItem>
                  ))
                ) : (
                  <p className="text-gray-500">暂无公告。</p>
                )}
              </Accordion>
            </Card>
          </div>
        </Tab>

        {/* Resources Tab */}
        <Tab
          key="resources"
          title={
            <div className="flex items-center gap-2">
              <Newspaper className="w-4 h-4" />
              <span>课程资源</span>
            </div>
          }
        >
          <Link href={`/course/${id}/submit`}>
            <Button variant="flat" color="primary" className="w-full">
              发布资源
            </Button>
          </Link>
          <div className="mt-8 grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {resources && resources.length > 0 ? (
              resources.map((resource) => (
                <Card
                  key={resource.resourceId}
                  className="bg-white shadow-md transition-transform duration-300 hover:scale-105"
                >
                  <CardBody>
                    <Image
                      src={resource.imageUrl} // Placeholder image
                      alt={resource.description}
                      className="w-full h-32 object-cover rounded-md mb-4"
                    />
                    <h3 className="text-lg font-semibold">{resource.description}</h3>

                    <Link href={`/course/${id}/${resource.resourceId}`}>
                      <Button
                        variant="light"
                        color="primary"
                        className="mt-4 w-full"
                        onClick={() => toast.success(`访问资源 ${resource.resourceId}`)}
                      >
                        查看资源
                      </Button>
                    </Link>
                  </CardBody>
                </Card>
              ))
            ) : (
              <p className="text-gray-500">暂无资源。</p>
            )}
          </div>
        </Tab>

        {/* Todo Items Tab */}
        <Tab
          key="todo-items"
          title={
            <div className="flex items-center gap-2">
              <CheckSquare className="w-4 h-4" />
              <span>待完成事项</span>
            </div>
          }
        >
          <div className="mt-8">
            <Card className="p-4 shadow-lg">
              <h2 className="text-xl font-semibold mb-4">待完成事项</h2>
              {localStorage.getItem("role") === "teacher" && <HomeworkModal />}
              {/* Replace with actual todo items */}
              {homeworks && homeworks.length > 0 ? (
                <Accordion>
                  {homeworks.map((homework) => (
                    <AccordionItem
                      key={homework.homeworkId}
                      aria-label={homework.homeworkName}
                      title={homework.homeworkName}
                      subtitle={`截止时间：${new Date(homework.dueTime).toLocaleString()}`}
                      onClick={() => {
                        if (localStorage.getItem("role") === "student") {
                          router.push(`/course/${id}/homework/${homework.homeworkId}/submit`);
                        } else {
                          router.push(`/course/${id}/homework/${homework.homeworkId}`);
                        }
                      }}
                    >
                      {homework.description}
                    </AccordionItem>
                  ))}
                </Accordion>
              ) : (
                <p className="text-gray-500">暂无待完成事项。</p>
              )}
            </Card>
          </div>
        </Tab>

        {/* Comments Tab */}
        {course.hasDiscussionArea && (
          <Tab
            key="comments"
            title={
              <div className="flex items-center gap-2">
                <MessageSquare className="w-4 h-4" />
                <span>评论区</span>
              </div>
            }
          >
            <div className="mt-8">
              <Card className="p-4 shadow-lg">
                <h2 className="text-xl font-semibold mb-4">评论 ({course.discussionArea.length})</h2>
                {/* Comment Submission */}
                <Textarea
                  placeholder="发表评论..."
                  className="mb-4"
                  value={newComment}
                  onChange={(e) => setNewComment(e.target.value)}
                />
                <Button color="primary" onClick={handleCommentSubmit}>
                  发表评论
                </Button>

                {/* Display Comments */}
                <div className="mt-6 space-y-4">
                  {course.discussionArea && course.discussionArea.length > 0 ? (
                    course.discussionArea.map((comment, index) => (
                      <Card key={index} className="p-4">
                        <div className="flex items-start space-x-4">
                          <Avatar
                            src={userAvatars[comment.userId] || ""}
                            alt={`User ${comment.userId}`}
                          />
                          <div className="flex-grow">
                            <div className="flex justify-between items-center">
                              <h3 className="font-semibold">User {comment.userId}</h3>
                              <p className="text-gray-500 text-sm">
                                {new Date(comment.time).toLocaleString()}
                              </p>
                              <Dropdown>
                                <DropdownTrigger>
                                  <Button isIconOnly variant="light" size="sm">
                                    <MoreVertical size={16} />
                                  </Button>
                                </DropdownTrigger>
                                <DropdownMenu aria-label="Comment actions">
                                  <DropdownItem key="report" startContent={<Flag size={16} />}>
                                    举报
                                  </DropdownItem>
                                  <DropdownItem onClick={() => handleDeleteComment(comment.userId)} key="report" startContent={<Flag size={16} />}>
                                    删除
                                  </DropdownItem>
                                </DropdownMenu>
                              </Dropdown>
                            </div>
                            <p className="mt-2">{comment.content}</p>
                            <div className="mt-2 flex items-center space-x-4">
                              <Button
                                variant="light"
                                size="sm"
                                startContent={<ThumbsUp size={16} />}
                                disabled
                              >
                                点赞
                              </Button>
                              <Button variant="light" size="sm" disabled>
                                回复
                              </Button>
                            </div>
                          </div>
                        </div>
                      </Card>
                    ))
                  ) : (
                    <p className="text-gray-500">暂无评论。</p>
                  )}
                </div>
              </Card>
            </div>
          </Tab>
        )}

        {/* Note Area Tab */}
        {course.hasNoteArea && (
          <Tab
            key="note"
            title={
              <div className="flex items-center gap-2">
                <MessageSquare className="w-4 h-4" />
                <span>笔记区域</span>
              </div>
            }
          >
            <div className="mt-8">
              <Card className="p-4 shadow-lg">
                <h2 className="text-xl font-semibold mb-4">我的笔记</h2>
                <MyEditor
                  initialValue={newNote}
                  onChange={(value) => setNewNote(value)}
                />
                {/* 提交按钮 */}
                <Button color="primary" onClick={handleNoteSubmit} className="mt-4">
                  提交笔记
                </Button>
              </Card>
            </div>
          </Tab>
        )}
      </Tabs>
    </div>
  );
}