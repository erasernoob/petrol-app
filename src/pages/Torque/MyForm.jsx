import { Form, Button, Input, Select, Message } from "@arco-design/web-react";
import { useEffect, useRef, useState } from "react";

const MyForm = ({ datas, handleSubmit, tabs, fileList}) => {
  const FormItem = Form.Item;
  const [form] = Form.useForm();
  const data = datas.work_condition;
  const handleDisabled = () => {
    console.log(`Mechanism: ${fileList.orbit.path === "" || fileList.drill.path === ""}`)
    return fileList.orbit.path === "" || fileList.drill.path === ""
  }
  return (
    <div className="form-wrapper-custom">
      <Form
        labelCol={{ flex: "160px" }}
        wrapperCol={{ flex: "1" }}
        layout="horizontal"
        size="large"
        form={form}
        onSubmit={async (data) => {
          handleSubmit(data);
        }}
      >
        <div className="my-custom-form">
          {data !== undefined
            ? Object.entries(data).map(([key, field]) => {
                return key === "wc" ? (
                  <FormItem
                    field={key}
                    key={key}
                    label={field.name}
                    // TODO: For TEST
                    initialValue={1}
                    rules={[
                      { required: true, message: `${field.name} 不能为空` },
                    ]}
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
                            {
                              required: true,
                              message: `${field.name} 不能为空`,
                            },
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
                              {
                                required: true,
                                message: `${field.name} 不能为空`,
                              },
                            ]}
                          >
                            <Input className="input-component" />
                          </FormItem>
                        );
                      }
                    }}
                  </FormItem>
                );
              })
            : Object.entries(datas).map(([key, field]) => {
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
              })}
        </div>

        <div className=''>
        <FormItem wrapperCol={{ offset: 5 }} >
          <Button
            type="primary"
            className="button submit-button"
            disabled={handleDisabled()}
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
        </div>
          </Form>

   </div>
  );
};

export default MyForm;
