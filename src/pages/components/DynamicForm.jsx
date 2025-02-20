import { Form, InputNumber, Button } from "@arco-design/web-react";

const { FormItem } = Form.Item
const DynamicForm = ({ data, onSubmit }) => {

    const [form] = Form.useForm();

    const formItemList = data.entries()
    console.log(formItemList)


  return (
    <Form
      form={form}
      style={{ width: 600 }}
      initialValues={{ }}
      autoComplete='off'
      onValuesChange={(v, vs) => {
        console.log(v, vs);
      }}
      onSubmit={(v) => {
        console.log(v);
      }}
    >
      <FormItem label='Username' field='name' rules={[{ required: true }]}>
        <Input placeholder='please enter your username' />
      </FormItem>
      <FormItem
        label='Age'
        field='age'
        rules={[{ required: true, type: 'number', min: 0, max: 99 }]}
      >
        <InputNumber placeholder='please enter your age' />
      </FormItem>
      <FormItem wrapperCol={{ offset: 5 }}>
        <Button type='primary' htmlType='submit' style={{ marginRight: 24 }}>
          Submit
        </Button>
        <Button
          style={{ marginRight: 24 }}
          onClick={() => {
            form.resetFields();
          }}
        >
          Reset
        </Button>
        <Button
          type='text'
          onClick={() => {
            form.setFieldsValue({
              name: 'admin',
              age: 11,
            });
          }}
        >
          Fill Form
        </Button>


        <Button
          type='text'
          onClick={() => {
            // 仅校验值，不会有 UI 表现
            form.validate({validateOnly: true}).then(() => {
              console.log('pass');
            }).catch(e => {

              console.log(e.errors)
            });

          }}
        >
          validateOnly
        </Button>
      </FormItem>
    </Form>
  );
};

export default DynamicForm;