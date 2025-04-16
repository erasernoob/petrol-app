import { Button, Checkbox, Form, Input, Message } from '@arco-design/web-react';
import { IconLock, IconUser } from '@arco-design/web-react/icon';
import React, { useState } from 'react';

import userInfo from './data';
import './style.css';

const FormItem = Form.Item;
const LoginPage = ({ status, setStatus, setTest }) => {
  const [form] = Form.useForm();
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (values) => {
    setLoading(true);
    try {
      if (userInfo[0].username === values.username
        && userInfo[0].password === values.password) {
        setTimeout(() => {
          setStatus(true)
          Message.success('登录成功！欢迎进入系统!')
          location.replace("/#/hydro")
          setLoading(false);
        }, 0)
      } else if (userInfo[1].username === values.username
        && userInfo[1].password === values.password) {
        setTimeout(() => {
          setStatus(true)
          setTest(true)

          Message.success('欢迎进入测试环境')
          location.replace("/#/hydro")
          setLoading(false);
        }, 800)

      } else {
        setTimeout(() => {
          Message.success('认证失败!')
          setLoading(false);
        }, 800)
      }
    } finally {
    }
  };

  return (
    <div className="login-container">
      {/* 系统标题 */}
      <div className="system-title">
        <h1>大位移井钻井关键参数联动分析系统</h1>
        <p>Drilling Parameters Optimization Platform</p>
      </div>

      {/* 登录表单容器 */}
      <div className="form-container">
        <div className="form-box">
          <h2 className="form-title">系统登录</h2>
          <Form form={form} wrapperCol={{ offset: '0.1' }} className='custom-form' onSubmit={handleSubmit} autoComplete="off">
            <FormItem
              field="username"
              rules={[{ required: true, message: '请输入用户名' }]}
              initialValue={userInfo[0].username}
            >
              <Input
                prefix={<IconUser />}
                placeholder="请输入用户名"
                size="large"
              />
            </FormItem>

            <FormItem
              field="password"
              rules={[{ required: true, message: '请输入密码' }]}
              initialValue={userInfo[0].password}
            >
              <Input.Password
                prefix={<IconLock />}
                placeholder="请输入密码"
                size="large"
              />
            </FormItem>

            <FormItem>
              <Checkbox
                defaultChecked={true}
              >记住密码</Checkbox>
            </FormItem>

            <FormItem>
              <Button
                type="primary"
                htmlType="submit"
                className='login-button'
                long
                size="large"
                loading={loading}
                shape="round"
              >
                登录系统
              </Button>
            </FormItem>
          </Form>
        </div>
      </div>
    </div>
  );
};

export default LoginPage;