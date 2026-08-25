import { useState } from 'react';
import { toggleFavoriteCourse } from '../lib/indexedDB';

const FavoriteCourse = () => {
    const [userId, setUserId] = useState('');
    const [courseId, setCourseId] = useState('');
    const [isFavorite, setIsFavorite] = useState(false);

    const handleToggleFavorite = async () => {
        const result = await toggleFavoriteCourse(userId, courseId, isFavorite);

        if (result.success) {
            toast.success(result.message);
            // 处理收藏成功逻辑，例如更新UI
        } else {
            toast.success(result.message);
            // 处理收藏失败逻辑，例如提示错误信息
        }
    };

    return (
        <div>
            <h1>收藏课程</h1>
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
            <label>
                <input
                    type="checkbox"
                    checked={isFavorite}
                    onChange={(e) => setIsFavorite(e.target.checked)}
                />
                收藏课程
            </label>
            <button onClick={handleToggleFavorite}>提交</button>
        </div>
    );
};

export default FavoriteCourse; 