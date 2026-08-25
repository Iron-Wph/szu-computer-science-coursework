import { useState } from 'react';
import { registerCourse } from '../lib/indexedDB';

const CreateCourse = () => {
  const [courseName, setCourseName] = useState('');
  const [courseCategory, setCourseCategory] = useState('');
  const [teacherId, setTeacherId] = useState('');
  const [hasDiscussionArea, setHasDiscussionArea] = useState(false);
  const [hasNoteArea, setHasNoteArea] = useState(false);
  const [startTime, setStartTime] = useState('');
  const [courseImageUrl, setCourseImageUrl] = useState('');

  const handleCreateCourse = async () => {
    const result = await registerCourse(
      courseName,
      courseCategory,
      teacherId,
      hasDiscussionArea,
      hasNoteArea,
      startTime,
      courseImageUrl
    );

    if (result.success) {
      toast.success(result.message);
      // 处理注册成功逻辑，例如跳转到课程列表页
    } else {
      toast.success(result.message);
      // 处理注册失败逻辑，例如提示错误信息
    }
  };

  return (
    <div>
      <h1>创建课程</h1>
      {/* 表单输入栏位 */}
      <input
        type="text"
        placeholder="课程名称"
        value={courseName}
        onChange={(e) => setCourseName(e.target.value)}
      />
      <input
        type="text"
        placeholder="课程类别"
        value={courseCategory}
        onChange={(e) => setCourseCategory(e.target.value)}
      />
      <input
        type="text"
        placeholder="授课教师ID"
        value={teacherId}
        onChange={(e) => setTeacherId(e.target.value)}
      />
      <label>
        <input
          type="checkbox"
          checked={hasDiscussionArea}
          onChange={(e) => setHasDiscussionArea(e.target.checked)}
        />
        设置讨论区
      </label>
      <label>
        <input
          type="checkbox"
          checked={hasNoteArea}
          onChange={(e) => setHasNoteArea(e.target.checked)}
        />
        设置笔记区
      </label>
      <input
        type="datetime-local"
        placeholder="开课时间"
        value={startTime}
        onChange={(e) => setStartTime(e.target.value)}
      />
      <input
        type="text"
        placeholder="课程图片URL"
        value={courseImageUrl}
        onChange={(e) => setCourseImageUrl(e.target.value)}
      />
      <button onClick={handleCreateCourse}>创建课程</button>
    </div>
  );
};

export default CreateCourse; 