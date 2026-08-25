import { openDB, DBSchema } from 'idb';
import toast from 'react-hot-toast';


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
    // 笔记
    note: { content: string; time: string,courseId:string}[];
}

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
    discussionArea: { userId: string; content: string; time: string }[];
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

interface Question {
    // 题目ID
    questionId: string;
    // 题目描述
    description: string;
    // 题目答案
    answer: string;
    // 题目类型
    type: string;
    // 题目解析
    analysis: string;
}

interface Exam {
    // 试卷ID
    examId: string;
    // 题目ID数组
    questionIds: string[];
    // 创建人ID
    creatorId: string;
    // 创建人类型
    creatorType: string;
}

// 定义公告接口
interface Announcement {
    announcementId: string;
    courseId: string;
    announcementTime: string;
    announcementTitle: string;
    announcementContent: string;
}

interface MyDB extends DBSchema {
    users: {
        key: string;
        value: User;
        indexes: { 'by-userId': string };
    };
    courses: {
        key: string;
        value: Course;
        indexes: { 'by-courseId': string; 'by-numberOfLikes': number };
    };
    homeworks: {
        key: string;
        value: Homework;
        indexes: { 'by-homeworkId': string };
    };
    resources: {
        key: string;
        value: Resource;
        indexes: { 'by-resourceId': string };
    };
    questions: {
        key: string;
        value: Question;
        indexes: { 'by-questionId': string };
    };
    exams: {
        key: string;
        value: Exam;
        indexes: { 'by-examId': string };
    };
    registrationStatus: {
        key: string;
        value: { isOpen: boolean };
    };
    announcements: {
        key: string;
        value: Announcement;
        indexes: { 'by-courseId': string };
    };
}

// 定义数据库打开成功的回调函数
const onDBOpenSuccess = (db: IDBDatabase) => {
    console.log('数据库打开成功');
    // 其他成功逻辑
};

// 定义数据库打开失败的回调函数
const onDBOpenError = (error: any) => {
    console.error('数据库打开失败:', error);
    // 其他错误处理逻辑
};

const dbPromise = openDB<MyDB>('my-database', 1, {
    upgrade(db) {
        // 检查并创建 'users' 存储
        if (!db.objectStoreNames.contains('users')) {
            const store = db.createObjectStore('users', {
                keyPath: 'userId',
            });
            store.createIndex('by-userId', 'userId');
        }


        // 检查并创建 'courses' 存储
        if (!db.objectStoreNames.contains('courses')) {
            const courseStore = db.createObjectStore('courses', {
                keyPath: 'courseId',
            });
            courseStore.createIndex('by-courseId', 'courseId');
            courseStore.createIndex('by-numberOfLikes', 'numberOfLikes');
            courseStore.createIndex('isHomepage', 'isHomepage');
        }

        // 检查并创建 'homeworks' 存储
        if (!db.objectStoreNames.contains('homeworks')) {
            const homeworkStore = db.createObjectStore('homeworks', {
                keyPath: 'homeworkId',
            });
            homeworkStore.createIndex('by-homeworkId', 'homeworkId');
            homeworkStore.createIndex('by-courseId', 'courseId');
        }

        // 检查并创建 'resources' 存储
        if (!db.objectStoreNames.contains('resources')) {
            const resourceStore = db.createObjectStore('resources', {
                keyPath: 'resourceId',
            });
            resourceStore.createIndex('by-resourceId', 'resourceId');
            resourceStore.createIndex('by-courseId', 'courseId');
        }

        // 检查并创建 'questions' 存储
        if (!db.objectStoreNames.contains('questions')) {
            const questionStore = db.createObjectStore('questions', {
                keyPath: 'questionId',
            });
            questionStore.createIndex('by-questionId', 'questionId');
        }

        // 检查并创建 'exams' 存储
        if (!db.objectStoreNames.contains('exams')) {
            const examStore = db.createObjectStore('exams', {
                keyPath: 'examId',
            });
            examStore.createIndex('by-examId', 'examId');
        }

        // 新增 'registrationStatus' 存储
        if (!db.objectStoreNames.contains('registrationStatus')) {
            const registrationStore = db.createObjectStore('registrationStatus', {
                keyPath: 'key',
            });
            // 设置默认值为 true
            registrationStore.transaction.oncomplete = () => {
                const tx = db.transaction('registrationStatus', 'readwrite');
                const store = tx.objectStore('registrationStatus');
                store.put({ key: 'status', isOpen: true });
            };
        }

        // 检查并创建 'announcements' 存储
        if (!db.objectStoreNames.contains('announcements')) {
            const announcementStore = db.createObjectStore('announcements', {
                keyPath: 'announcementId',
            });
            announcementStore.createIndex('by-courseId', 'courseId');
        }
    },
}).catch(error => {
    console.error('数据库打开失败:', error);
    throw error; // 确保在失败时抛出错误
});

// 根据作业id获取作业
export const getHomeworkByHomeworkId = async (homeworkId: string): Promise<Homework | undefined> => {
    const db = await dbPromise;
    return db.get('homeworks', homeworkId);
};

export const addUser = async (user: User) => {
    const db = await dbPromise;
    await db.add('users', user);
};

export const getUser = async (userId: string): Promise<User | undefined> => {
    const db = await dbPromise;
    return db.get('users', userId);
};
// 获取所有用户
export const getUsers = async (): Promise<User[]> => {
    const db = await dbPromise;
    return db.getAll('users');
};

export const updateUser = async (user: User) => {
    const db = await dbPromise;
    await db.put('users', user);
};

export const deleteUser = async (userId: string) => {
    const db = await dbPromise;
    await db.delete('users', userId);
};

export const addCourse = async (course: Course) => {
    const db = await dbPromise;
    await db.add('courses', course);
};

export const getCourse = async (courseId: string): Promise<Course | undefined> => {
    const db = await dbPromise;
    return db.get('courses', courseId);
};

// 根据课程ID数组获取多个课程
export const getCourses = async (courseIds: string[]): Promise<Course[]> => {
    const db = await dbPromise;
    const tx = db.transaction('courses', 'readonly');
    const store = tx.objectStore('courses');
    const courses = await Promise.all(courseIds.map(id => store.get(id)));
    return courses.filter((course): course is Course => course !== undefined);
};


export const updateCourse = async (course: Course) => {
    const db = await dbPromise;
    await db.put('courses', course);
    // 教师添加课程
    const teacher = await getUser(course.teacherId);
    if(teacher){
        // 如果教师未添加该课程，则添加
        if(!teacher.selectedCourses.includes(course.courseId)){
            teacher.selectedCourses.push(course.courseId);  
            await updateUser(teacher);
        }
    }
};

export const deleteCourse = async (courseId: string) => {
    const db = await dbPromise;
    // 获取课程
    const course = await getCourse(courseId);
    if(!course) return;
    // 教师删除课程
    const teacher = await getUser(course.teacherId);
    if(teacher){
        teacher.selectedCourses.splice(teacher.selectedCourses.indexOf(courseId), 1);
        await updateUser(teacher);
    }
    await db.delete('courses', courseId);
};

export const addHomework = async (homework: Homework) => {
    const db = await dbPromise;
    await db.add('homeworks', homework);
};

export const getHomework = async (homeworkId: string): Promise<Homework | undefined> => {
    const db = await dbPromise;
    return db.get('homeworks', homeworkId);
};

// 根据课程ID获取作业
export const getHomeworksByCourseId = async (courseId: string): Promise<Homework[]> => {
    const db = await dbPromise;
    const tx = db.transaction('homeworks', 'readonly');
    const store = tx.objectStore('homeworks');
    const index = store.index('by-courseId');
    return index.getAll(courseId);
};

// 提交作业
export const submitHomework = async (hw: {homeworkId: string, content: string, userId: string}) => {
    const db = await dbPromise;
    // 获取对应的作业
    const homework = await getHomework(hw.homeworkId)
    if (!homework) 
        return { success: false, message: '用户已存在' };
    if(homework.isDue)
        return { success: false, message: '作业已截止' };
    if(homework.dueTime>=new Date().toISOString())
    {
        homework.isDue = true;
        await db.put('homeworks', homework);
        return { success: false, message: '作业已截止' };
    }

    // 将作业提交
    homework.submittedHomework.push({ userId: hw.userId, content: hw.content })
    await db.put('homeworks', homework);
    return { success: true, message: '作业提交成功' };
};

// 获取所有作业
export const getAllHomeworks = async (): Promise<Homework[]> => {
    const db = await dbPromise;
    return db.getAll('homeworks');
};

export const updateHomework = async (homework: Homework) => {
    const db = await dbPromise;
    await db.put('homeworks', homework);
};

export const deleteHomework = async (homeworkId: string) => {
    const db = await dbPromise;
    await db.delete('homeworks', homeworkId);
};

export const addResource = async (resource: Resource) => {
    const db = await dbPromise;
    await db.add('resources', resource);
};

export const getResource = async (resourceId: string): Promise<Resource | undefined> => {
    const db = await dbPromise;
    return db.get('resources', resourceId);
};

export const updateResource = async (resource: Resource) => {
    const db = await dbPromise;
    await db.put('resources', resource);
};

export const deleteResource = async (resourceId: string) => {
    const db = await dbPromise;
    await db.delete('resources', resourceId);
};

export const addQuestion = async (question: Question) => {
    const db = await dbPromise;
    await db.add('questions', question);
};

export const getQuestion = async (questionId: string): Promise<Question | undefined> => {
    const db = await dbPromise;
    return db.get('questions', questionId);
};

export const updateQuestion = async (question: Question) => {
    const db = await dbPromise;
    await db.put('questions', question);
};

export const deleteQuestion = async (questionId: string): Promise<void> => {
    const db = await dbPromise;
    await db.delete('questions', questionId);
};

export const addExam = async (exam: Exam) => {
    const db = await dbPromise;
    await db.add('exams', exam);
};

export const getExam = async (examId: string): Promise<Exam | undefined> => {
    const db = await dbPromise;
    return db.get('exams', examId);
};

export const updateExam = async (exam: Exam) => {
    const db = await dbPromise;
    await db.put('exams', exam);
};

export const deleteExam = async (examId: string) => {
    const db = await dbPromise;
    await db.delete('exams', examId);
};

// 登录用户
export const loginUser = async (userId: string, password: string): Promise<{ success: boolean, message: string, avatarUrl?: string, userType?: string, userId?: string }> => {
    const user = await getUser(userId);
    if (!user) {
        return { success: false, message: '用户不存在' };
    }
    if (user.password !== password) {
        user.passwordErrorCount += 1;
        if (user.passwordErrorCount >= 5) {
            user.status = 'frozen';
            await updateUser(user);
            return { success: false, message: '账户已被冻结，请联系管理员' };
        } else {
            await updateUser(user);
            return { success: false, message: '密码错误，当前错误次数：' + user.passwordErrorCount +'还有' + (5 - user.passwordErrorCount) + '次机会' };
        }
    }
    if (user.status === 'frozen') {
        return { success: false, message: '账户已被冻结，请联系管理员' };
    }
    user.passwordErrorCount = 0;
    await updateUser(user);
    return { success: true, message: '登录成功', avatarUrl: user.avatarUrl, userType: user.userType, userId: user.userId };
};

// 注册用户
export const registerUser = async (
    userType: string,
    userId: string,
    password: string
): Promise<{ success: boolean; message: string }> => {
    try {
        // 检查注册状态
        const isRegistrationOpen = await getRegistrationStatus();
        if (!isRegistrationOpen) {
            return { success: false, message: '当前不开放注册' };
        }

        const db = await dbPromise;
        const tx = db.transaction('users', 'readwrite');
        const store = tx.objectStore('users');

        // 检查用户是否已存在
        const existingUser = await store.get(userId);
        if (existingUser) {
            return { success: false, message: '用户已存在' };
        }

        const newUser: User = {
            userType,
            userId,
            password,
            avatarUrl: 'https://s1.locimg.com/2024/12/25/b772c8e171319.jpg',
            nickname: `User${userId}`,
            selectedCourses: [],
            favoriteCourses: [],
            passwordErrorCount: 0,
            status: 'active',
            learningHistory: [],
            description: "A diligent student", // 描述: 一个勤奋的学生
            content: "Detailed student information", // 内容: 详细的学生信息
            note: []
        };

        await store.add(newUser);
        await tx.done;
        return { success: true, message: '注册成功' };
    } catch (error) {
        console.error('注册失败:', error);
        return { success: false, message: '注册失败，请重试。' };
    }
};

// 新增课程发布函数
export const registerCourse = async (
    courseName: string,
    courseCategory: string,
    teacherId: string,
    hasDiscussionArea: boolean,
    hasNoteArea: boolean,
    publishDate: string,
    courseImageUrl: string,
    university: string,
    instructor: string,
    description: string,
    content: string,
): Promise<{ success: boolean; message: string }> => {
    try {
        const db = await dbPromise;
        const tx = db.transaction('courses', 'readwrite');
        const store = tx.objectStore('courses');

        // 生成唯一的课程ID（示例使用时间戳）
        const courseId = `course-${Date.now()}`;

        const newCourse: Course = {
            courseId,
            courseImageUrl,
            numberOfEnrolledStudents: 0, // 初始化为0
            courseCategory,
            courseName,
            publishDate,
            numberOfLikes: 0, // 初始化为0
            discussionArea: [], // 初始化为空数组
            hasDiscussionArea,
            hasNoteArea,
            enrollmentList: [], // 初始化为空数组
            teacherId,
            resourceId: [], // 初始化为空数组
            university, 
            instructor,
            description,
            content,
            isHomepage: false,
        };
        // 教师添加课程
        const teacher = await getUser(teacherId);
        if(teacher){
            teacher.selectedCourses.push(courseId);
            await updateUser(teacher);
        }

        await store.add(newCourse);
        await tx.done;
        return { success: true, message: '课程注册成功' };
    } catch (error) {
        console.error('课程注册失败:', error);
        return { success: false, message: '课程注册失败，请重试。' };
    }
};

// 获取所有课程
export const getAllCourses = async (): Promise<Course[]> => {
    try {
        const db = await dbPromise;
        const tx = db.transaction('courses', 'readonly');
        const store = tx.objectStore('courses');
        const allCourses = await store.getAll(); // 获取所有课程
        return allCourses;
    } catch (error) {
        console.error('获取所有课程失败:', error);
        return [];
    }
};

// 获取首页课程
export const getHomepageCourses = async (): Promise<Course[]> => {
    const db = await dbPromise;
    const tx = db.transaction('courses', 'readonly');
    const store = tx.objectStore('courses');
    const allCourses = await store.getAll(); // 获取所有课程
    return allCourses.filter(course => course.isHomepage); // 过滤出 isHomepage 为 true 的课程
};

// 新增获取推荐课程的函数
export const getTopCourses = async (): Promise<Course[]> => {
    const db = await dbPromise;
    const tx = db.transaction('courses', 'readonly');
    const store = tx.objectStore('courses');
    const index = store.index('by-numberOfLikes'); // 使用点赞数索引

    // 获取所有课程并按点赞数排序，返回前5个
    const allCourses = await index.getAll();
    const topCourses = allCourses
        .sort((a, b) => b.numberOfLikes - a.numberOfLikes) // 按点赞数降序排序
        .slice(0, 5); // 取前5个课程

    return topCourses;
};

// 新增获取推荐课程的函数
export const getRecommendedCourses = async (): Promise<Course[]> => {
    try {
        const db = await dbPromise;
        const tx = db.transaction('courses', 'readonly');
        const store = tx.objectStore('courses');
        const allCourses = await store.getAll();

        // 假设推荐课程是按点赞数排序的前5个课程
        const recommendedCourses = allCourses
            .sort((a, b) => b.numberOfLikes - a.numberOfLikes) // 按点赞数降序排序
            .slice(0, 5); // 取前5个课程

        return recommendedCourses;
    } catch (error) {
        console.error('获取推荐课程失败:', error);
        return [];
    }
}; 

// 新增获取最新课程的函数
export const getLatestCourses = async (): Promise<Course[]> => {
    const db = await dbPromise;
    const tx = db.transaction('courses', 'readonly');
    const store = tx.objectStore('courses');

    // 获取所有课程
    const allCourses = await store.getAll();

    // 按发布日期排序，返回最新的前5个课程
    const latestCourses = allCourses
        .sort((a, b) => new Date(b.publishDate).getTime() - new Date(a.publishDate).getTime()) // 按发布日期降序排序
        .slice(0, 5); // 取前5个课程

    return latestCourses;
};

// 新增获取热门课程的函数
export const getPopularCourses = async (): Promise<Course[]> => {
    const db = await dbPromise;
    const tx = db.transaction('courses', 'readonly');
    const store = tx.objectStore('courses');

    // 获取所有课程
    const allCourses = await store.getAll();

    // 按选课人数排序，返回热门的前5个课程
    const popularCourses = allCourses
        .sort((a, b) => b.numberOfEnrolledStudents - a.numberOfEnrolledStudents) // 按选课人数降序排序
        .slice(0, 5); // 取前5个课程

    return popularCourses;
};

// 新增课程搜索函数
export const searchCourses = async (keyword: string): Promise<Course[]> => {
    const db = await dbPromise;
    const tx = db.transaction('courses', 'readonly');
    const store = tx.objectStore('courses');

    // 获取所有课程
    const allCourses = await store.getAll();

    // 根据关键字匹配课程名称，返回匹配的课���
    const matchedCourses = allCourses.filter(course =>
        course.courseName.includes(keyword) // 直接使用 includes() 方法
    );

    return matchedCourses;
};

// 新增作业发布函数
export const publishHomework = async (
    courseName: string,
    homeworkName: string,
    startTime: string,
    dueTime: string,
    description: string
): Promise<{ success: boolean; message: string }> => {
    try {
        // 查找课程ID
        const db = await dbPromise;
        const tx = db.transaction('courses', 'readonly');
        const store = tx.objectStore('courses');

        // 获取所有课程
        const allCourses = await store.getAll();
        const course = allCourses.find(c => c.courseName === courseName);

        if (!course) {
            return { success: false, message: '课程不存在' };
        }

        // 生成唯一的作业ID（示例使用时间戳）
        const homeworkId = `homework-${Date.now()}`;

        const newHomework: Homework = {
            homeworkId,
            homeworkName,
            courseId: course.courseId, // 使用找到的课程ID
            startTime,
            dueTime,
            description,
            studentList: course.enrollmentList, // 更新作业的学生名单为课程的选课名单
            completedList: [], // 初始化为空数组
            isDue: false, // 初始状态为未截止
                // 评分
            score: [],
            submittedHomework: []
        };

        await addHomework(newHomework);
        return { success: true, message: '作业发布成功' };
    } catch (error) {
        console.error('作业发布失败:', error);
        return { success: false, message: '作业发布失败，请重试。' };
    }
};
// 退选课程
export const unenrollFromCourse = async (userId: string, courseId: string) => {
    const db = await dbPromise;
    const tx = db.transaction('courses', 'readwrite');
    const store = tx.objectStore('courses');
    const course = await store.get(courseId);
    if(course){
        course.enrollmentList = course.enrollmentList.filter(id => id !== userId);
        await store.put(course);
        const user = await getUser(userId);
        if(user){
            user.selectedCourses = user.selectedCourses.filter(id => id !== courseId);
            await updateUser(user);
        }
    }
    return { success: true, message: '退选成功' };
};
// 判断该学生是否已选该课程
export const isEnrolled = async (userId: string, courseId: string): Promise<boolean> => {
    const db = await dbPromise;
    const tx = db.transaction('courses', 'readonly');
    const store = tx.objectStore('courses');
    const course = await store.get(courseId);
    if(course){
        return course.enrollmentList.includes(userId);
    }else{
        return false;
    }
};

// 根据学生id获取作业
export const getHomeworksByStudentId = async (userId: string): Promise<Homework[]> => {
    const db = await dbPromise;
    const tx = db.transaction('homeworks', 'readonly');
    const store = tx.objectStore('homeworks');

    const allHomeworks = await store.getAll();
    return allHomeworks.filter(homework => homework.submittedHomework.filter(hw => hw.userId !== userId));

};

// 新增学生选课函数
export const enrollInCourse = async (userId: string, courseId: string): Promise<{ success: boolean; message: string }> => {
    try {
        const db = await dbPromise;

        // 获取用户信息
        const user = await getUser(userId);
        if (!user) {
            return { success: false, message: '用户不存在' };
        }

        // 获取课程信息
        const course = await getCourse(courseId);
        if (!course) {
            return { success: false, message: '课程不存在' };
        }

        // 更新用户的选课数组
        if (!user.selectedCourses.includes(courseId)) {
            user.selectedCourses.push(courseId);
            user.learningHistory.push(courseId);
            await updateUser(user);
        }else{
            return { success: false, message: '用户已选该课程' };
        }

        // 更新课程的选课名单
        if (!course.enrollmentList.includes(userId)) {
            course.enrollmentList.push(userId);
            course.numberOfEnrolledStudents += 1;
            await updateCourse(course);
        }

        // 更新所有作业的学生名单
        const tx = db.transaction('homeworks', 'readwrite');
        const homeworkStore = tx.objectStore('homeworks');
        const allHomeworks = await homeworkStore.getAll();

        for (const homework of allHomeworks) {
            if (homework.courseId === courseId && !homework.studentList.includes(userId)) {
                homework.studentList.push(userId);
                await homeworkStore.put(homework);
            }
        }
        return { success: true, message: '选课成功' };
    } catch (error) {
        console.error('选课失败:', error);
        return { success: false, message: '选课失败，请重试。' };
    }
};

// 新增收藏课程函数
export const toggleFavoriteCourse = async (userId: string, courseId: string, isFavorite: boolean): Promise<{ success: boolean; message: string }> => {
    try {
        const db = await dbPromise;

        // 获取用户信息
        const user = await getUser(userId);
        if (!user) {
            return { success: false, message: '用户不存在' };
        }

        // 获取课程信息
        const course = await getCourse(courseId);
        if (!course) {
            return { success: false, message: '课程不存在' };
        }

        // 更新用户的收藏课程数组
        if (isFavorite) {
            // 收藏课程
            if (!user.favoriteCourses.includes(courseId)) {
                user.favoriteCourses.push(courseId);
                await updateUser(user);
                // 增加课程的点赞数
                course.numberOfLikes += 1;
                await updateCourse(course);
            } else {
                return { success: false, message: '课程已被收藏' };
            }
        } else {
            // 取消收藏课程
            if (user.favoriteCourses.includes(courseId)) {
                user.favoriteCourses = user.favoriteCourses.filter(id => id !== courseId);
                await updateUser(user);
                // 减少课程的点赞数
                course.numberOfLikes = Math.max(0, course.numberOfLikes - 1); // 确保点赞数不为负
                await updateCourse(course);
            } else {
                return { success: false, message: '课程未被收藏' };
            }
        }

        return { success: true, message: isFavorite ? '课程已收藏' : '课程已取消收藏' };
    } catch (error) {
        console.error('收藏课程失败:', error);
        return { success: false, message: '收藏课程失败，请重试。' };
    }
};


// 获取注册状态
export const getRegistrationStatus = async (): Promise<boolean> => {
    const db = await dbPromise;
    const tx = db.transaction('registrationStatus', 'readonly');
    const store = tx.objectStore('registrationStatus');
    const status = await store.get('status');
    if(status){
        return status.isOpen;
    }else{
        return false;
    }
};

// 更新注册状态
export const setRegistration = async (isOpen: boolean) => {
    const db = await dbPromise;
    const tx = db.transaction('registrationStatus', 'readwrite');
    const store = tx.objectStore('registrationStatus');
    await store.put({ key: 'status', isOpen });
    await tx.done;
};

// 新增公告
export const addAnnouncement = async (announcement: Announcement) => {
    const db = await dbPromise;
    await db.add('announcements', announcement);
};

// 获取所有公告
export const getAnnouncements = async (): Promise<Announcement[]> => {
    const db = await dbPromise;
    const tx = db.transaction('announcements', 'readonly');
    const store = tx.objectStore('announcements');
    return store.getAll();
};

// 根据课程ID获取公告
export const getAnnouncementsByCourseId = async (courseId: string): Promise<Announcement[]> => {
    const db = await dbPromise;
    const tx = db.transaction('announcements', 'readonly');
    const store = tx.objectStore('announcements');
    const index = store.index('by-courseId');
    return index.getAll(courseId);
};

// 根据课程id返回多个公告
export const getAnnouncementsByCourseIds = async (courseIds: string[]): Promise<Announcement[]> => {
    const db = await dbPromise;
    const tx = db.transaction('announcements', 'readonly');
    const store = tx.objectStore('announcements');
    const index = store.index('by-courseId');
    const allAnnouncements = await store.getAll();
    return allAnnouncements.filter(announcement => courseIds.includes(announcement.courseId));
};

// 根据课程ID获取课程
export const getCourseById = async (courseId: string): Promise<Course | undefined> => {
    try {
        const db = await dbPromise;
        const tx = db.transaction('courses', 'readonly');
        const store = tx.objectStore('courses');
        const course = await store.get(courseId);
        return course;
    } catch (error) {
        console.error('获取课程失败:', error);
        return undefined;
    }
};

// 根据课程id获取资源
export const getResourcesByCourseId = async (courseId: string): Promise<Resource[]> => {
    const db = await dbPromise;
    const tx = db.transaction('resources', 'readonly');
    const store = tx.objectStore('resources');
    const index = store.index('by-courseId');
    return index.getAll(courseId);
};


// 根据资源id获取资源
export const getResourceById = async (resourceId: string): Promise<Resource | undefined> => {
    const db = await dbPromise;
    const tx = db.transaction('resources', 'readonly');
    const store = tx.objectStore('resources');
    return store.get(resourceId);
};

// 根据课程id返回多个作业
export const getHomeworksByCourseIds = async (courseId: string[]): Promise<Homework[]> => {
    const db = await dbPromise;
    const tx = db.transaction('homeworks', 'readonly');
    const store = tx.objectStore('homeworks');
    const allHomeworks = await store.getAll();
    return allHomeworks.filter(homework => courseId.includes(homework.courseId));
};

// 收藏课程
export const addFavouriteCourse = async (userId: string, courseId: string) => {
    const db = await dbPromise;
    const user = await getUser(userId);
    if(user){
        // 如果用户已收藏该课程，则取消收藏
        if(!user.favoriteCourses.includes(courseId)){
            user.favoriteCourses.push(courseId);
            await updateUser(user);
        }else{
            toast.error("已收藏该课程！");
        }
    }
    const course = await getCourse(courseId);
    if(course){
        course.numberOfLikes += 1;
        await updateCourse(course);
    }
};
// 取消收藏课程
export const removeFavouriteCourse = async (userId: string, courseId: string) => {
    const db = await dbPromise;
    const user = await getUser(userId);
    if(user){
        user.favoriteCourses = user.favoriteCourses.filter(id => id !== courseId);
        await updateUser(user);
    }
    const course = await getCourse(courseId);
    if(course){
        course.numberOfLikes -= 1;
        course.numberOfLikes = Math.max(0, course.numberOfLikes);
        await updateCourse(course);
    }
};
// 判断用户是否收藏该课程
export const isFavourite = async (userId: string, courseId: string): Promise<boolean> => {
    const user = await getUser(userId);
    if(user){
        return user.favoriteCourses.includes(courseId);
    }else{
        return false;
    }
};
// 新增评论
export const addComment = async (comment: { userId: string; content: string; time: string },courseId: string) => {
    const db = await dbPromise;
    // 获取课程id
    const course = await getCourse(courseId);
    if(course){
        course.discussionArea.push(comment);
        await updateCourse(course);
        return { success: true, message: '评论成功' };
    }else{
        return { success: false, message: '评论失败' };
    }
};

// 新增笔记
export const addNote = async (note: { userId: string; content: string; time: string,courseId:string }) => {
    const db = await dbPromise;
    const user = await getUser(note.userId);
    if(user){
        user.note.push({content:note.content,time:note.time,courseId:note.courseId});
        await updateUser(user);
    }else{
        return { success: false, message: '请先完成登录' };   
    }
};
// 删除评论
export const deleteComment = async (userId: string, courseId: string) => {
    const db = await dbPromise;
    // 获取课程
    const course = await getCourse(courseId);
    if(course){
        course.discussionArea = course.discussionArea.filter(comment => comment.userId !== userId);
        await updateCourse(course);
    }

};
