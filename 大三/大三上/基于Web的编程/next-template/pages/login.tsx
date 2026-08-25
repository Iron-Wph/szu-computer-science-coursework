import { useState } from 'react';
import { loginUser } from '../lib/indexedDB';

const Login = () => {
  const [userId, setUserId] = useState('');
  const [password, setPassword] = useState('');

  const handleLogin = async () => {
    const result = await loginUser(userId, password);

    if (result.success) {
      toast.success(result.message);
      // 处理登录成功逻辑，例如跳转到首页
    } else {
      toast.success(result.message);
      // 处理登录失败逻辑，例如提示错误信息
    }
  };

  return (
    <div>
      <h1>登录</h1>
      {/* 表单输入栏位 */}
      <button onClick={handleLogin}>登录</button>
    </div>
  );
};

export default Login; 