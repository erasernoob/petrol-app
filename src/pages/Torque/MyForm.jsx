import { Form, Button, Input, Select } from "@arco-design/web-react";
import { useEffect, useRef, useState } from "react";
import { torque } from "../../data/Params";

const MyForm = ({ datas, handleSubmit, tabs, fileList=[] }) => {
  const [tabTime, setTabTime] = useState(0);
  const FormItem = Form.Item;
  const [form] = Form.useForm();
  const data = torque.work_condition;

  Object.entries(data).map(([key, field]) => {
    if (key === "wc") {
      console.log(field.option);
    }
  });

  return (
    <div className="form-wrapper-custom">
      <Form
        labelCol={{ flex: "160px" }}
        wrapperCol={{ flex: "1" }}
        className="my-custom-form"
        layout="horizontal"
        size="large"
        form={form}
        onSubmit={async (data) => {
          handleSubmit(data);
        }}
      >
        <div className="my-custom-form">
          {Object.entries(data).map(([key, field]) => {
            return key === "wc" ? (
              <FormItem
                field={key}
                key={key}
                label={field.name}
                // TODO: For TEST
                initialValue={1}
                rules={[{ required: true, message: `${field.name} 不能为空` }]}
              >
                <Select
                  options={field.option}
                  className="input-component"
                ></Select>
              </FormItem>
            ) : (
              <FormItem noStyle shouldUpdate>
                {(values) => {
                  const res = (
                    <FormItem
                      field={key}
                      key={key}
                      label={field.name}
                      initialValue={field.value}
                      rules={[
                        { required: true, message: `${field.name} 不能为空` },
                      ]}
                    >
                      <Input className="input-component" />
                    </FormItem>
                  );
                  if (values.wc !== 1 && values.wc !== 5) {
                    return key === "v" || key === "omega" ? <></> : res;
                  } else {
                    if (values.wc === 5 && key === "v") {
                      field.name = "上提速度(m/s)";
                    } else if (values.wc === 1 && key === "v") {
                      field.name = "钻进速度(m/s)";
                    }
                    return (
                    <FormItem
                      field={key}
                      key={key}
                      label={field.name}
                      initialValue={field.value}
                      rules={[
                        { required: true, message: `${field.name} 不能为空` },
                      ]}
                    >
                      <Input className="input-component" />
                    </FormItem>
                    );
                  }
                }}
              </FormItem>
              //  <FormItem field={key} key={key} label={field.name}>
              // <Input className="input-component" />
              // </FormItem>
              //
            );
          })}
        </div>
        <FormItem wrapperCol={{ offset: 6 }}>
          <Button
            type="primary"
            className="button submit-button"
            disabled={
              fileList.length <= 2
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
