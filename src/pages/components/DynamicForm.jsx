import {
  Button,
  Checkbox,
  Form,
  Input,
  Select,
  Tabs,
} from "@arco-design/web-react";
import { useEffect, useState } from "react";
import { useSelector } from "react-redux";

const DynamicForm = ({ datas, handleSubmit, tabs, file, drill = false, limit = false }) => {
  const useTheInitialValue = useSelector((state) => state.data.useTheInitialValue)

  const [tabTime, setTabTime] = useState(0);
  // 默认宾汉流体
  const [selectValue, setSelectValue] = useState(1)
  // 默认不勾选岩屑
  const [checked, setChecked] = useState(false)

  const tabsName = tabs;
  const TabPane = Tabs.TabPane;
  const FormItem = Form.Item;

  const [form] = Form.useForm();
  useEffect(() => {
    form.setFieldValue("y", 0)
    form.setFieldValue("yx", 1)

  }, [])


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
          className={!limit ? (!drill ? "custom-tabs" : "custom-drill") : "custom-tabs-limit"}
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
                    height: "80vh",
                    gap: "2vh",
                    overflowY: "auto",
                    alignItems: "center",
                    paddingTop: "10px",
                    paddingRight: "6vw",
                    boxSizing: "border-box",
                  }}
                >
                  {Object.entries(data).map(([key, field]) => (
                    <FormItem
                      key={key}
                      label={field.name}
                      field={key}
                      initialValue={useTheInitialValue || key === 'lbmx' ? field.value : ""}
                      rules={[
                        {
                          required:
                            !(categoryKey == "fluid" && key != "fluidden" && (
                              selectValue == 1
                              && (key != "miu" && key != "taof")
                              ||
                              selectValue == 2
                              && (key != "n" && key != "K")
                              ||
                              selectValue == 3
                              && (key != "n" && key != "K" && key != "taof"))
                              ||
                              categoryKey == "rock_cuttings" && !checked)

                          , message: `${field.name} 不能为空`
                        },
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
                          value={1}
                          className="input-component"
                          placeholder={`宾汉流体`}
                          onChange={setSelectValue}
                        />
                        // 判断是否是岩屑
                      ) : key != "yx" && key != "y" ? (
                        <Input
                          className="input-component"
                          // placeholder={`请输入${field.name}`}
                          disabled={
                            categoryKey == "fluid" && key != "fluidden" && (
                              selectValue == 1
                              && (key != "miu" && key != "taof")
                              ||
                              selectValue == 2
                              && (key != "n" && key != "K")
                              ||
                              selectValue == 3
                              && (key != "n" && key != "K" && key != "taof"))
                            ||
                            categoryKey == "rock_cuttings" && !checked
                          }
                        ></Input>
                      ) : (
                        <Checkbox
                          checked={checked}
                          onChange={(check) => {
                            form.setFieldValue(key, check ? 1 : 0)
                            console.log(check)
                            setChecked(check)
                          }}
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
            height: datas[datas.length - 1].flag === "1" ? "2%" : "",
            display: "flex",
            justifyContent: "center",
            width: "100%",
          }}
        >
          <div
            style={{
              display: "flex",
              justifyContent: "center",
              alignItems: "center",
              gap: "30px",
              marginTop: !drill ? "14.8px" : "12px"
            }}
          >
            <Button
              type="primary"
              className="button submit-button"
              disabled={file.name == ""}
              onClick={async () => {
                try {
                  console.log(await form.validate())
                } catch (error) {
                  console.log(error.errors)

                }
              }}
              htmlType="submit"
            >
              计算
            </Button>
            <Button
              type="primary"
              className="button reset-button"
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
