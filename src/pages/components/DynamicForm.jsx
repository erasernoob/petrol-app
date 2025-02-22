import { Tabs } from "@arco-design/web-react";
import { Form, Button, Input } from "@arco-design/web-react";
import { useEffect, useRef, useState } from "react";

const DynamicForm = ({ datas, handleSubmit, tabs }) => {

  const [tabTime, setTabTime] = useState(0) 

  const tabsName = tabs
  const  TabPane  = Tabs.TabPane
  const FormItem = Form.Item

  const [form] = Form.useForm()

  return (
    <div className="form-wrapper">
    <Form 
          layout="horizontal"
          size="large"
          form={form}
          onSubmit={async (data) => {
              handleSubmit(data)
           }}
    >
      <Tabs type="card" tabPosition="left" className='custom-tabs' size="large" onChange={() => setTabTime(() => tabTime + 1)}>
        {
          datas.map((category, index) => {
            const [categoryKey, data] = Object.entries(category)[0]
            return (
          <TabPane title={tabsName[index]} key={categoryKey} className='custom-tabsPane'>
            {Object.entries(data).map(([key, field]) => (
              field.name.length <= 1000 ? 
              <FormItem
                key={key}
                label={field.name}
                field={key}
                // TODO: 测试用
                initialValue={field.value}
                rules={[{ required: true, message: `${field.name} 不能为空` }]}
              >
                <Input className='input-component'/>
              </FormItem> : <></>
            ))}
          </TabPane>
          )
        })
      }
      </Tabs>
      
      <FormItem wrapperCol={{offset: 6}}>
        <Button type="primary" className='button submit-button' disabled={tabTime < tabs.length - 1}  htmlType="submit" >计算</Button>
        <Button type="primary" className='button reset-button'>重置</Button>
      </FormItem>
      
   </Form>
    </div>
  );

};

export default DynamicForm;