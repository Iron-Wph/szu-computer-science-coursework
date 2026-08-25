// /user/auth.tsx

"use client";

import React, { useState, useEffect } from "react";
import {
  Button,
  Input,
  Checkbox,
  Link,
  Divider,
  Card,
  CardBody,
  Avatar,
  Textarea,
} from "@nextui-org/react";
import { useRouter } from "next/navigation";
import { toast, Toaster } from "react-hot-toast";
import { registerUser, loginUser } from '../../lib/indexedDB'

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
  discussionArea: { userId: string; content: string }[];
  hasDiscussionArea: boolean;
  hasNoteArea: boolean;
  enrollmentList: string[];
  teacherId: string;
  resourceId: string[];
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

const generateTestUsers = (): User[] => [
  {
    userType: "student",
    userId: "student-1",
    password: "<demo-password>",
    avatarUrl: "https://s1.locimg.com/2024/12/25/5b9f98ef71be1.jpg",
    nickname: "Alice",
    selectedCourses: ["course-123"],
    favoriteCourses: ["course-456"],
    passwordErrorCount: 0,
    status: "active",
    learningHistory: ["course-123"],
  },
  {
    userType: "student",
    userId: "student-2",
    password: "<demo-password>",
    avatarUrl: "https://s1.locimg.com/2024/12/25/b772c8e171319.jpg",
    nickname: "Bob",
    selectedCourses: ["course-123", "course-456"],
    favoriteCourses: [],
    passwordErrorCount: 1,
    status: "active",
    learningHistory: ["course-456"],
  },
];

const generateTestCourses = (): Course[] => [
  {
    courseId: "course-123",
    courseImageUrl: "https://s1.locimg.com/2024/12/25/4f43ce87187ad.jpg",
    numberOfEnrolledStudents: 150,
    courseCategory: "Computer Science",
    courseName: "Introduction to Programming",
    publishDate: "2024-01-15",
    numberOfLikes: 250,
    discussionArea: [
      { userId: "student-1", content: "Great course!" },
      { userId: "student-2", content: "Looking forward to the next module." },
    ],
    hasDiscussionArea: true,
    hasNoteArea: true,
    enrollmentList: ["student-1", "student-2"],
    teacherId: "teacher-1",
    resourceId: ["resource-1", "resource-2"],
  },
  {
    courseId: "course-456",
    courseImageUrl: "https://s1.locimg.com/2024/12/25/52800bfba1d1a.jpg",
    numberOfEnrolledStudents: 200,
    courseCategory: "Mathematics",
    courseName: "Calculus I",
    publishDate: "2024-02-20",
    numberOfLikes: 300,
    discussionArea: [],
    hasDiscussionArea: false,
    hasNoteArea: true,
    enrollmentList: ["student-2"],
    teacherId: "teacher-2",
    resourceId: ["resource-3"],
  },
];

// -----------------------------------
// Authentication Page Component
// -----------------------------------

export default function AuthPage() {
  const router = useRouter();
  const [activeTab, setActiveTab] = useState<"login" | "register">("login");

  // Toggle between login and register tabs
  const toggleTab = () => {
    setActiveTab(activeTab === "login" ? "register" : "login");
  };

  // Initialize test data on component mount
  useEffect(() => {
    const initializeTestData = async () => {
      // Initialize Users
      const users = await getDataFromIndexedDB("users", "all");
      if (!users) {
        const testUsers = generateTestUsers();
        await setDataToIndexedDB("users", "all", testUsers);
      }

      // Initialize Courses
      const courses = await getDataFromIndexedDB("courses", "all");
      if (!courses) {
        const testCourses = generateTestCourses();
        await setDataToIndexedDB("courses", "all", testCourses);
      }

      // You can initialize other data structures similarly
    };

    initializeTestData();
  }, []);

  return (
    <div className="flex h-screen w-full flex-col items-center justify-center bg-gray-100">
      <Card className="w-full max-w-md p-6 shadow-lg rounded-lg">
        <CardBody>
          <div className="flex flex-col items-center pb-6">
            <p className="text-2xl text-gray-800 font-semibold">
              {activeTab === "login" ? "欢迎回来" : "深圳大学Uooc平台"}
            </p>
            <p className="text-sm text-gray-600">
              {activeTab === "login"
                ? "登录您的账户以继续"
                : "欢迎你的加入！"}
            </p>
          </div>

          {activeTab === "login" ? <LoginForm /> : <RegisterForm />}

          <div className="flex items-center gap-4 my-4">
            <Divider className="flex-1" />
            <p className="shrink-0 text-xs text-gray-500">或者</p>
            <Divider className="flex-1" />
          </div>

          <p className="text-center text-sm">
            {activeTab === "login" ? "还没有账户？" : "已经有账户？"}{" "}
            <Link onClick={toggleTab} className="text-blue-500 cursor-pointer">
              {activeTab === "login" ? "注册" : "登录"}
            </Link>
          </p>
        </CardBody>
      </Card>
    </div>
  );
}

// -----------------------------------
// Register Form Component
// -----------------------------------

// -----------------------------------
// Register Form Component
// -----------------------------------

function RegisterForm() {
  const router = useRouter();
  const [formData, setFormData] = useState({
    studentId: "",
    password: "",
    confirmPassword: "",
  });
  const [isVisible, setIsVisible] = useState(false);

  // Handle input changes
  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  // Toggle password visibility
  const toggleVisibility = () => {
    setIsVisible(!isVisible);
  };

  // Handle form submission
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    // Input validation
    const { studentId, password, confirmPassword } = formData;
    if (!/^\d{10}$/.test(studentId)) {
      toast.error("学号必须是10位数字！");
      return;
    }
    if (password.length < 6) {
      toast.error("密码长度至少为6位！");
      return;
    }
    if (password !== confirmPassword) {
      toast.error("密码和确认密码不一致！");
      return;
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

    // Simulate password hashing with salt (for demonstration purposes only)
    const hashedPassword = await hashPassword(password);
    const isRegistrationOpen = localStorage.getItem("isRegistrationOpen");
    if (isRegistrationOpen === "true") {
      const result = await registerUser('student', studentId, hashedPassword);
      if (result.success) {
        toast.success("注册成功！请返回登陆页面");
      } else {
        toast.error(result.message);
      }
    } else {
      toast.error("当前不开放注册");
    }
  };

  return (
    <form className="flex flex-col gap-4" onSubmit={handleSubmit}>
      <Input
        isRequired
        label="学号"
        name="studentId"
        placeholder="请输入您的学号（10位数字）"
        type="text"
        variant="bordered"
        value={formData.studentId}
        onChange={handleInputChange}
      />
      <Input
        isRequired
        label="密码"
        name="password"
        placeholder="请输入您的密码（至少6位）"
        type={isVisible ? "text" : "password"}
        variant="bordered"
        value={formData.password}
        onChange={handleInputChange}
        endContent={
          <Button
            auto
            size="xs"
            flat
            color="primary"
            onClick={toggleVisibility}
          >
            {isVisible ? "隐藏" : "显示"}
          </Button>
        }
      />
      <Input
        isRequired
        label="确认密码"
        name="confirmPassword"
        placeholder="确认您的密码"
        type={isVisible ? "text" : "password"}
        variant="bordered"
        value={formData.confirmPassword}
        onChange={handleInputChange}
        endContent={
          <Button
            auto
            size="xs"
            flat
            color="primary"
            onClick={toggleVisibility}
          >
            {isVisible ? "隐藏" : "显示"}
          </Button>
        }
      />
      <Checkbox isRequired className="py-2 text-sm">
        我同意&nbsp;
        <Link href="#" color="primary" size="sm">
          服务条款
        </Link>
        &nbsp; 和&nbsp;
        <Link href="#" color="primary" size="sm">
          隐私政策
        </Link>
      </Checkbox>
      <Button color="primary" type="submit">
        注册
      </Button>
    </form>
  );
}
  // -----------------------------------
  // Login Form Component
  // -----------------------------------

  function LoginForm() {
    const router = useRouter();
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
    const [isVisible, setIsVisible] = useState(false);
    const [remember, setRemember] = useState(false);

    // Toggle password visibility
    const toggleVisibility = () => {
      setIsVisible(!isVisible);
    };

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

    // Handle form submission
    const handleLogin = async (e: React.FormEvent) => {
      e.preventDefault();

      // Input validation
      if (!username || !password) {
        toast.error("请填写用户名和密码！");
        return;
      }

      // Simulate password hashing with salt (for demonstration purposes only)
      const hashedPassword = await hashPassword(password);

      const result = await loginUser(username, hashedPassword);
      if (result.success) {
        toast.success("登录成功！3秒后自动跳转至主页...");
        localStorage.setItem("username", username);
        localStorage.setItem("avatarUrl", result.avatarUrl || "");
        localStorage.setItem("role", result.userType || "");
        localStorage.setItem("userId", result.userId || "");
        window.location.href = "/";
      } else {
        toast.error(result.message);
      }
    };

    return (
      <form className="flex flex-col gap-4" onSubmit={handleLogin}>
        <Input
          isRequired
          label="用户名"
          name="username"
          placeholder="请输入您的用户名"
          type="text"
          variant="bordered"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
        />
        <Input
          isRequired
          label="密码"
          name="password"
          placeholder="请输入您的密码"
          type={isVisible ? "text" : "password"}
          variant="bordered"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          endContent={
            <Button
              auto
              size="xs"
              flat
              color="primary"
              onClick={toggleVisibility}
            >
              {isVisible ? "隐藏" : "显示"}
            </Button>
          }
        />
        <div className="flex items-center justify-between">
          <Checkbox
            isSelected={remember}
            onChange={(e) => setRemember(e.target.checked)}
            size="sm"
          >
            记住账户与密码
          </Checkbox>
          <Link href="#" color="primary" size="sm">
            忘记密码？
          </Link>
        </div>
        <Button color="primary" type="submit">
          登录
        </Button>
      </form>
    );
  }