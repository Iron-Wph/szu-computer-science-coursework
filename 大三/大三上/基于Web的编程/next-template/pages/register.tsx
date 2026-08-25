import { useState } from 'react';
import { registerUser } from '../lib/indexedDB';

const Register = () => {
  const [userType, setUserType] = useState('');
  const [userId, setUserId] = useState('');
  const [password, setPassword] = useState('');

  const handleRegister = async () => {
    const result = await registerUser(userType, userId, password);

    if (result.success) {
      toast.success(result.message);
      // 处理注册成功逻辑，例如跳转到登录页
    } else {
      toast.success(result.message);
      // 处理注册失败逻辑，例如提示错误信息
    }
  };

  return (
    <div>
      <h1>注册</h1>
      {/* 表单输入栏位 */}
      <button onClick={handleRegister}>注册</button>
    </div>
  );
};

export default Register; 