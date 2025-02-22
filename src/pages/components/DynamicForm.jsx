import { Tabs } from "@arco-design/web-react";
import { Message } from "@arco-design/web-react";
import { useEffect, useRef } from "react";
import { Form, Button, Input } from "@arco-design/web-react";
import MyButton from "../../layouts /BasicLayout/components/MyButton.";

const DynamicForm = ({ datas, handleSubmit, tabs }) => {

  const tabsName = tabs
  const  TabPane  = Tabs.TabPane
  const { form, disabled, isSubmitting } = Form.useFormContext();

  const FormItem = Form.Item

  function DemoButton() {
  const { form, disabled, isSubmitting } = Form.useFormContext();
  const messageRef = useRef(null)

  useEffect(() => {
    if (isSubmitting) {
      messageRef.current = 'id-' + Date.now()
      Message.loading({
        id: messageRef.current,
        content: 'submitting',
        duration: 0
      });
    } else {
      if (messageRef.current) {
        const isError = Object.keys(form.getFieldsError()).length > 0;

        Message[isError ? 'error' : 'success']({
          id: messageRef.current,
          content: isError ? 'validate failed' : 'submitted',
          duration: 3000
        });
      }
      messageRef.current = null
    }
  }, [isSubmitting])
    return (
    <>
      <Button
        type='primary'
        htmlType='submit'
        disabled={disabled}
        loading={isSubmitting}
        style={{ marginRight: 24 }}
      >
        Submit
      </Button>
      <Button
        disabled={disabled}
        style={{ marginRight: 24 }}
        onClick={() => {
          form.resetFields();
        }}
      >
        Reset
      </Button>
    </>
  );

}

  return (
    <div className="form-wrapper">
    <Form 
          layout="horizontal"
          size="large"
          onSubmit={async (data) => {
            console.log(JSON.stringify(data))
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