// script.js

document.addEventListener('DOMContentLoaded', () => {
    const formTitle = document.getElementById('form-title');
    const authForm = document.getElementById('auth-form');
    const submitButton = document.getElementById('submit-button');
    const toggleButton = document.getElementById('toggle-button');
    const toggleText = document.getElementById('toggle-text');
    const usernameGroup = document.getElementById('username-group');
    const togglePasswordButton = document.getElementById('toggle-password');
    const passwordInput = document.getElementById('password');
    const usernameInput = document.getElementById('username');
    const resetPasswordForm = document.getElementById('reset-password-form');
    const forgotPasswordLink = document.getElementById('forgot-password-link');
    const backToLoginLink = document.getElementById('back-to-login');
    const toggleNewPasswordButton = document.getElementById('toggle-new-password');
    const newPasswordInput = document.getElementById('new-password');
    const resetUsernameInput = document.getElementById('reset-username');
    const strengthIndicator = document.getElementById('strength-indicator');
    const newStrengthIndicator = document.getElementById('new-strength-indicator'); // 新密码强度指示器

    let isLogin = true;

    // 初始化 IndexedDB
    let db;
    const request = indexedDB.open('UserDB', 1);

    request.onerror = function (event) {
        console.error('数据库打开失败');
    };

    request.onsuccess = function (event) {
        db = event.target.result;
        console.log('数据库已打开');
    };

    request.onupgradeneeded = function (event) {
        db = event.target.result;
        const objectStore = db.createObjectStore('users', { keyPath: 'username' });
        objectStore.createIndex('username', 'username', { unique: true });
    };

    toggleButton.addEventListener('click', () => {
        isLogin = !isLogin;
        if (isLogin) {
            formTitle.textContent = '登录';
            submitButton.textContent = '登录';
            toggleText.textContent = '没有账户？';
            toggleButton.textContent = '注册';
            usernameGroup.style.display = 'block';
            clearStrengthIndicator(); // 清除强度指示器
        } else {
            formTitle.textContent = '注册';
            submitButton.textContent = '注册';
            toggleText.textContent = '已有账户？';
            toggleButton.textContent = '登录';
            usernameGroup.style.display = 'block';
            clearStrengthIndicator(); // 清除强度指示器
        }
        clearErrors();
        authForm.reset();
    });

    togglePasswordButton.addEventListener('click', () => {
        const type = passwordInput.getAttribute('type') === 'password' ? 'text' : 'password';
        passwordInput.setAttribute('type', type);
        const passwordIcon = document.getElementById('password-icon');
        passwordIcon.classList.toggle('fa-eye-slash'); // 切换图标
        passwordIcon.classList.toggle('fa-eye'); // 切换图标
    });

    // 处理密码输入时的强度指示
    passwordInput.addEventListener('input', () => {
        const password = passwordInput.value;
        updateStrengthIndicator(password, strengthIndicator);
    });

    // 处理新密码输入时的强度指示
    newPasswordInput.addEventListener('input', () => {
        const newPassword = newPasswordInput.value;
        updateStrengthIndicator(newPassword, newStrengthIndicator);
    });

    // 更新密码强度指示器
    function updateStrengthIndicator(password, indicator) {
        let strength = 0;
        const hasUpperCase = /[A-Z]/.test(password);
        const hasLowerCase = /[a-z]/.test(password);
        const hasNumbers = /\d/.test(password);
        if (hasUpperCase) strength++;
        if (hasLowerCase) strength++;
        if (hasNumbers) strength++;
        indicator.className = 'strength-indicator'; // 重置类名

        if (strength === 1) {
            indicator.classList.add('strength-weak');
        } else if (strength === 2) {
            indicator.classList.add('strength-medium');
        } else if (strength === 3) {
            indicator.classList.add('strength-strong');
        }
    }

    // 清除强度指示器样式
    function clearStrengthIndicator() {
        strengthIndicator.className = 'strength-indicator'; // 重置类名
        newStrengthIndicator.className = 'strength-indicator'; // 重置类名
    }

    // 处理忘记密码链接点击事件
    forgotPasswordLink.addEventListener('click', (e) => {
        e.preventDefault(); // 阻止默认链接行为
        formTitle.style.display = 'none'; // 隐藏标题
        authForm.classList.add('hidden'); // 隐藏登录表单
        resetPasswordForm.classList.remove('hidden'); // 显示重置密码表单
    });

    // 处理返回登录链接点击事件
    backToLoginLink.addEventListener('click', (e) => {
        e.preventDefault(); // 阻止默认链接行为
        resetPasswordForm.classList.add('hidden'); // 隐藏重置密码表单
        authForm.classList.remove('hidden'); // 显示登录表单
        formTitle.style.display = 'block'; // 显示标题
    });

    // 定义清除错误信息的函数
    function clearErrors() {
        const errorElements = document.querySelectorAll('.error');
        errorElements.forEach(el => el.textContent = '');
    }

    // 显示错误信息的函数
    function showError(elementId, message) {
        const errorElement = document.getElementById(elementId);
        if (errorElement) {
            errorElement.textContent = message;
        }
    }

    // 哈希密码的函数
    async function hashPassword(password, salt) {
        const encoder = new TextEncoder();
        const data = encoder.encode(password + salt); // 将盐添加到密码后
        const hash = await crypto.subtle.digest('SHA-256', data);
        return Array.from(new Uint8Array(hash)).map(b => b.toString(16).padStart(2, '0')).join('');
    }

    // 定义生成盐的函数
    function generateSalt() {
        // 生成一个随机盐
        const array = new Uint8Array(16);
        window.crypto.getRandomValues(array);
        return Array.from(array).map(b => b.toString(16).padStart(2, '0')).join('');
    }

    // 处理新密码输入框的图标点击事件
    toggleNewPasswordButton.addEventListener('click', () => {
        const type = newPasswordInput.getAttribute('type') === 'password' ? 'text' : 'password';
        newPasswordInput.setAttribute('type', type);
        const newPasswordIcon = document.getElementById('new-password-icon');
        newPasswordIcon.classList.toggle('fa-eye-slash'); // 切换图标
        newPasswordIcon.classList.toggle('fa-eye'); // 切换图标
    });

    authForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        clearErrors();
        const username = document.getElementById('username').value.trim();
        const password = document.getElementById('password').value.trim();
        let valid = true;
        if (username === '') {
            showError('username-error', '用户名不能为空');
            valid = false;
        }
        if (password === '') {
            showError('password-error', '密码不能为空');
            valid = false;
        } else if (password.length < 6) {
            showError('password-error', '密码长度至少为6个字符');
            valid = false;
        }
        if (db) {
            if (isLogin) {
                // 登录逻辑：验证用户
                const getRequest = db.transaction(['users'], 'readonly').objectStore('users').get(username);

                getRequest.onsuccess = async function (event) {
                    const user = event.target.result;
                    if (user) {
                        const hashedPassword = await hashPassword(password, user.salt); // 使用存储的盐
                        if (user.password === hashedPassword) {
                            alert('登录成功！');
                        } else {
                            alert('密码错误');
                        }
                    } else {
                        alert('用户未注册');
                    }
                };
            } else {
                // 注册逻辑：存储新用户
                const salt = generateSalt(); // 生成盐
                const hashedPassword = await hashPassword(password, salt); // 使用盐哈希密码
                const newUser = { username, password: hashedPassword, salt }; // 存储盐
                const transaction = db.transaction(['users'], 'readwrite');
                const objectStore = transaction.objectStore('users');
                // 先检查用户名是否存在
                const getUsernameRequest = objectStore.get(username);
                getUsernameRequest.onsuccess = async function (event) {
                    const existingUser = event.target.result;
                    if (existingUser) {
                        alert('用户名已存在！');
                    } else {
                        // 添加新用户
                        const addRequest = objectStore.add(newUser);
                        addRequest.onsuccess = function () {
                            alert('注册成功！');
                            authForm.reset();
                        };
                        addRequest.onerror = function () {
                            alert('注册失败，请稍后再试。');
                        };
                    }
                };
            }
        } else {
            alert('数据库未初始化，请稍后再试。');
        }
    });

    // 处理重置密码表单提交事件
    resetPasswordForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        clearErrors();
        const resetUsername = resetUsernameInput.value.trim();
        const newPassword = newPasswordInput.value.trim();
        let valid = true;
        if (resetUsername === '') {
            showError('reset-username-error', '用户名不能为空');
            valid = false;
        }
        if (newPassword === '') {
            showError('new-password-error', '新密码不能为空');
            valid = false;
        } else if (newPassword.length < 6) {
            showError('new-password-error', '新密码长度至少为6个字符');
            valid = false;
        }

        if (db && valid) {
            // 检查用户是否存在
            const getRequest = db.transaction(['users'], 'readonly').objectStore('users').get(resetUsername);
            getRequest.onsuccess = async function (event) {
                const user = event.target.result;
                if (user) {
                    const salt = user.salt; // 获取用户的盐
                    const hashedPassword = await hashPassword(newPassword, salt); // 使用盐哈希新密码
                    // 更新用户密码
                    const transaction = db.transaction(['users'], 'readwrite');
                    const objectStore = transaction.objectStore('users');
                    user.password = hashedPassword; // 更新密码
                    const updateRequest = objectStore.put(user);
                    updateRequest.onsuccess = function () {
                        alert('密码重置成功！'); // 弹出提示
                        resetPasswordForm.reset(); // 重置表单
                        clearStrengthIndicator(); // 清除强度指示器
                    };
                    updateRequest.onerror = function () {
                        alert('密码重置失败，请稍后再试。');
                    };
                } else {
                    alert('用户未注册');
                }
            };
        } else {
            alert('数据库未初始化，请稍后再试。');
        }
    });
});