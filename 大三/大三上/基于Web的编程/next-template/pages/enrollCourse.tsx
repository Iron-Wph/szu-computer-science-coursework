import { useState } from 'react';
import { enrollInCourse } from '../lib/indexedDB';

const EnrollCourse = () => {
    const [userId, setUserId] = useState('');
    const [courseId, setCourseId] = useState('');

    const handleEnroll = async () => {
        const result = await enrollInCourse(userId, courseId);

        if (result.success) {
            toast.success(result.message);
            // 处理选课成功逻辑，例如跳转到课程列表页
        } else {
            toast.success(result.message);
            // 处理选课失败逻辑，例如提示错误信息
        }
    };

    return (
        <div>
            <h1>选课</h1>
            <input
                type="text"
                placeholder="用户ID"
                value={userId}
                onChange={(e) => setUserId(e.target.value)}
            />
            <input
                type="text"
                placeholder="课程ID"
                value={courseId}
                onChange={(e) => setCourseId(e.target.value)}
            />
            <button onClick={handleEnroll}>选课</button>
        </div>
    );
};

export default EnrollCourse; 