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
      console.log(field.name)
    }
  })


  return (
    <div className="form-wrapper">
      <Form
        style={{
          height: "100%",
        }}
        layout="vertical"
        size="large"
        form={form}
        onSubmit={async (data) => {
          handleSubmit(data);
        }}
      >
        {
          Object.entries(data).map(([key, field]) => {
            return (
            key === 'wc' ?
            <FormItem
            field={key}
            key={key}
            label={field.name}
            >
              <Select option={field.option}></Select>
            </FormItem>
              :
              <FormItem
              field={key}
              
              
              >

              </FormItem>
            )
           
          })
        }

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
