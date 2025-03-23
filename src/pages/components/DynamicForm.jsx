import {
  Button,
  Checkbox,
  Form,
  Input,
  Select,
  Tabs,
} from "@arco-design/web-react";
import { useState } from "react";

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
          textAlign: "left",
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
            if (index === datas.length - 1) return
            const [categoryKey, data] = Object.entries(category)[0];
            return (
              <TabPane
                title={tabsName[index]}
                key={categoryKey}
                className="custom-tabsPane"
              >
                <div
                  style={{
                    width: "100%",
                    display: "flex",
                    flexDirection: "column",
                    gap: "2vh",
                    alignItems: "center",
                    paddingTop: "10px",
                    paddingRight: "4vw",
                    boxSizing: "border-box",
                  }}
                >
                  {Object.entries(data).map(([key, field]) => (
                    <FormItem
                      key={key}
                      label={field.name}
                      field={key}
                      initialValue={field.value}
                      rules={[
                        { required: true, message: `${field.name} 不能为空` },
                      ]}
                      className="fixed-position-form-item"
                      labelCol={{ span: 11 }}
                      wrapperCol={{ span: 13 }}
                      style={{
                        marginLeft: "auto",
                        marginRight: "auto",
                        marginBottom: "20px",
                        width: "100%",
                        display: "flex",
                      }}
                    >
                      {key === "lbmx" ? (
                        <Select
                          options={field.option}
                          className="input-component"
                          placeholder={`请选择${field.name}`}
                        />
                      ) : key != "yx" && key != "y" ? (
                        <Input
                          className="input-component"
                          placeholder={`请输入${field.name}`}
                        ></Input>
                      ) : (
                        <Checkbox
                          onChange={(checked) =>
                            form.setFieldValue(key, checked ? 1 : 0)
                          }
                        ></Checkbox>
                      )}
                    </FormItem>
                  ))}
                </div>
              </TabPane>
            );
          })}
        </Tabs>

        <FormItem
          className="button-wrapper"
          style={{
            borderTop: "1px solid #e8e8e8",
            height: datas[datas.length - 1].flag === "1" ? "1%" : "",
            display: "flex",
            justifyContent: "center",
            width: "100%",
          }}
        >
          <div
            style={{ display: "flex", justifyContent: "center", alignItems: "center", gap: "30px", marginTop: "3px"}}
          >
            <Button
              type="primary"
              className="button submit-button"
              disabled={file.name == ""}
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
          </div>
        </FormItem>
      </Form>
    </div>
  );
};

export default DynamicForm;
