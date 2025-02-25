import { Form, Button, Input, Select } from "@arco-design/web-react";
import { useEffect, useRef, useState } from "react";
import { torque } from "../../data/Params";

const MyForm = ({ datas, handleSubmit, tabs, fileList }) => {
  const [tabTime, setTabTime] = useState(0);
  const FormItem = Form.Item;
  const [form] = Form.useForm();
  const data = torque.work_condition

  Object.entries(data).map(([key, field]) => {
    if (key === 'wc') {
      console.log(field.option)
    }
  })


  return (
    <div className="form-wrapper-custom">
      <Form
        labelCol={{ flex: '160px' }}
        wrapperCol={{ flex: '1' }}
        className='my-custom-form'
        style={{
          height: "100%",
        }}
        layout="horizontal"
        size="large"
        form={form}
        // labelCol={{offset: '0'}}
        onSubmit={async (data) => {
          handleSubmit(data);
        }}
      >
        <div className="my-custom-form">
        {
          Object.entries(data).map(([key, field]) => {
            return (
            key === 'wc' ?
            <FormItem
            field={key}
            key={key}
            label={field.name}
            initialValue={1}
            >
              <Select options={field.option} className='input-component'></Select>
            </FormItem>
              :
              <FormItem
                field={key}
                key={key}
                label={field.name}
              >
                <Input  className='input-component'/>
              </FormItem>
            )
          })
        }
        </div>
        <FormItem wrapperCol={{ offset: 6 }}>
          <Button
            type="primary"
            className="button submit-button"
            disabled={
              fileList.length != 0 || (tabTime < tabs.length - 1 && !form.validate())
            }
            htmlType="submit"
          >
            计算
          </Button>
          <Button
            type="primary"
            className="button reset-button"
            disabled={!form.validate()}
            onClick={() => {
              form.resetFields();
            }}
          >
            重置
          </Button>
        </FormItem>
      </Form>
    </div>
  );
};

export default MyForm;
