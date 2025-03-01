import React, { useState } from 'react';
import { Form, Input, Button, Checkbox, Message } from '@arco-design/web-react';
import { IconUser, IconLock } from '@arco-design/web-react/icon';
import './style.css';

const FormItem = Form.Item;

const LoginPage = () => {
  const [form] = Form.useForm();
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (values) => {
    setLoading(true);
    try {
      console.log('Submit values:', values);
      Message.success('登录成功');
    } finally {
      setLoading(false);
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
          <Form form={form} wrapperCol={{offset: '0.1'}} className='custom-form' onSubmit={handleSubmit} autoComplete="off">
            <FormItem
              field="username"
              rules={[{ required: true, message: '请输入用户名' }]}
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
            >
              <Input.Password
                prefix={<IconLock />}
                placeholder="请输入密码"
                size="large"
              />
            </FormItem>

            <FormItem>
              <Checkbox>记住密码</Checkbox>
            </FormItem>

            <FormItem>
              <Button
                type="primary"
                htmlType="submit"
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