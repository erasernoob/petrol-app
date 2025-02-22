import { Tabs } from "@arco-design/web-react";
import { Form, Button, Input } from "@arco-design/web-react";
import MyButton from "../../layouts /BasicLayout/components/MyButton.";
import { post } from "./axios";

const DynamicForm = ({ datas, handleSubmit, tabs }) => {

  const tabsName = tabs
  const  TabPane  = Tabs.TabPane
  const FormItem = Form.Item

  const { form, disabled, isSubmitting } = Form.useFormContext();


  return (
    <div className="form-wrapper">
    <Form 
          layout="horizontal"
          size="large"
          onSubmit={async (data) => {
              handleSubmit(data)
            // console.log(JSON.stringify(data))
            // const response = await post('/hydro', JSON.stringify(data))
            // console.log(response)
           }}
    >
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
                field={key}
                // TODO: 测试用
                initialValue={field.value}
                rules={[{ required: false, message: `${field.name} 不能为空` }]}
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
        <Button type="primary" className='button submit-button'  htmlType="submit" >计算</Button>
        <Button type="primary" className='button reset-button'   >重置</Button>
      </FormItem>
      
        {/* {DemoButton()} */}
   </Form>
    </div>
  );

};

export default DynamicForm;