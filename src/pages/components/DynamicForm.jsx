import { Tabs } from "@arco-design/web-react";
import { Form, Button, Input } from "@arco-design/web-react";
import MyButton from "../../layouts /BasicLayout/components/MyButton.";

const DynamicForm = ({ datas, handleSubmit, tabs }) => {

  const tabsName = tabs
  const  TabPane  = Tabs.TabPane
  const [form] = Form.useForm();
  const FormItem = Form.Item
  console.log('')




  return (
    <div className="form-wrapper">
    <Form form={form} layout="horizontal">
      <Tabs type="card" tabPosition="left" className='custom-tabs' size="large">
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
                name={key}
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
      
      {/* 提交按钮 */}
      <div className="button-wrapper">
      <Button type="primary" className='button submit-button'  onClick={() => handleSubmit()} >计算</Button>
      <Button type="primary" className='button reset-button'  onClick={() => handleReset()} >重置</Button>
      </div>
   </Form>

    </div>
  );

};

export default DynamicForm;