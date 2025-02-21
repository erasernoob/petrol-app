import { Tabs } from "@arco-design/web-react";
import { Form, Button, Input } from "@arco-design/web-react";

const DynamicForm = ({ datas, handleSubmit, tabs }) => {

  const tabsName = tabs
  const  TabPane  = Tabs.TabPane
  const [form] = Form.useForm();
  const FormItem = Form.Item




  return (
    <Form form={form} layout="horizontal">
      <Tabs key="card" tabPosition="left">
        {
          datas.map((category, index) => {
            const [categoryKey, data] = Object.entries(category)[0]
            return (
          <TabPane title={tabsName[index]} key={categoryKey}>
            {Object.entries(data).map(([key, field]) => (
              <FormItem
                key={key}
                label={field.name}
                name={key}
                rules={[{ required: true, message: `${field.name} 不能为空` }]}
              >
                <Input style={{}}/>
              </FormItem>
            ))}

          </TabPane>
          )
        })
      }
      </Tabs>
      
      {/* 提交按钮 */}
      <Button type="primary" onClick={handleSubmit} style={{ marginTop: 16 }}>
        提交
      </Button>
    </Form>

  );
};

export default DynamicForm;