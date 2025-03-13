import { Checkbox, Tabs } from "@arco-design/web-react";
import { Form, Button, Input, Select } from "@arco-design/web-react";
import { useEffect, useRef, useState } from "react";

const DynamicForm = ({ datas, handleSubmit, tabs, file }) => {
  const [tabTime, setTabTime] = useState(0);

  const tabsName = tabs;
  const TabPane = Tabs.TabPane;
  const FormItem = Form.Item;

  const [form] = Form.useForm();

  return (
    <div className="form-wrapper">
      <Form
        style={{
          height: "100%",
          textAlign: 'left'
        }}
        layout="horizontal"
        size="large"
        form={form}
        onSubmit={async (data) => {
          handleSubmit(data);
        }}
        >
        <Tabs
          type="card"
          tabPosition="left"
          className="custom-tabs"
          size="large"
          lazyload={false}
          onChange={() => setTabTime(() => tabTime + 1)}
          >
          {datas.map((category, index) => {
            const [categoryKey, data] = Object.entries(category)[0];
            return (
              <TabPane
              title={tabsName[index]}
              key={categoryKey}
              className="custom-tabsPane"
              >
                {Object.entries(data).map(([key, field]) => (
                  <FormItem
                  key={key}
                  label={field.name}
                  labelCol={ tabsName[index] === '钻井液' || tabsName[index] === '地面管汇' ? {span: '11', offset: ''} : {span: '9'}}
                  wrapperCol={{span: '10',}}
                  field={key}
                  // TODO: 测试用
                  // labelCol={{flex: "1" ,offset: ""}}
                  initialValue={field.value}
                  rules={[
                    { required: true, message: `${field.name} 不能为空` },
                  ]}
                  >
                    {key === "lbmx" ? (
                      <Select
                        options={field.option}
                        className="input-component"
                      />
                    ) : key != "yx" && key != "y" ? (
                      <Input className="input-component"></Input>
                    ) : (
                      <Checkbox
                        // checked={field.value === "1"} // 控制选中状态
                        onChange={(checked) =>
                          form.setFieldValue(key, checked ? 1 : 0)
                        }
                      ></Checkbox>
                    )}
                  </FormItem>
                ))}
              </TabPane>
            );
          })}
        </Tabs>

        <FormItem className='button-wrapper' wrapperCol={{ offset: 6 }} style={{borderTop: "1px solid #e8e8e8"}}>
          <Button
            type="primary"
            className="button submit-button"
            disabled={
              file.name == "" 
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

export default DynamicForm;
