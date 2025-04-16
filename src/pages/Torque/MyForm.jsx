import { Button, Checkbox, Form, Input, Select } from "@arco-design/web-react";
import { useState } from "react";
import { useSelector } from "react-redux";

const MyForm = ({ datas, handleSubmit, tabs, fileList, limit = false }) => {
  const FormItem = Form.Item;
  const [form] = Form.useForm();
  const data = datas.work_condition;
  const handleDisabled = () => {
    return fileList.orbit.path === "" || fileList.drill.path === ""
  }

  const useTheInitialValue = useSelector((state) => state.data.useTheInitialValue)
  // 是否勾选计算屈曲
  const [checked, setChecked] = useState(false)

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
        <div className={!limit ? "my-custom-form" : "my-custom-form-limit"}>
          {data !== undefined
            ? Object.entries(data).map(([key, field]) => {
              return key === "wc" ? (
                <FormItem
                  field={key}
                  key={key}
                  label={field.name}
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
                        disabled={
                          !checked && key === "ml"
                        }
                        label={field.name}
                        initialValue={useTheInitialValue ? field.value : ""}

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

                    // 删掉后三个工况的钻压 以及除了下钻工况的屈曲
                    if (values.wc !== 1 && values.wc !== 2 && key === "T0"
                      ||
                      values.wc !== 4 && key === "calcCurve" || values.wc !== 4 && key === "ml"
                    ) {
                      return <></>
                    }

                    if (values.wc === 4 && key === "calcCurve") {
                      return (<>
                        <hr style={{
                          display: 'block',
                          marginTop: '2px',
                          height: '1px',
                          backgroundColor: '#000',
                          width: 'calc(100% + 58px)', // 通过 calc() 来覆盖掉 padding
                          marginLeft: '-60px' // 向左偏移 60px，覆盖 padding
                        }}></hr>


                        <FormItem
                          key={key}
                          label={field.name}
                          field={key}
                        >
                          {/* 添加一条线作为额外的标签 */}
                          <Checkbox
                            checked={checked}
                            onChange={(check) => {
                              form.setFieldValue(key, check ? 1 : 0)
                              setChecked(check)
                              console.log(check)
                            }}
                          ></Checkbox>
                        </FormItem >
                      </>)
                    }

                    if (values.wc !== 1 && values.wc !== 5) {
                      return key === "v" || key === "omega" ? <></> : res;
                    } else {
                      if (values.wc === 5 && key === "v") {
                        field.name = "上提速度(m/h)";
                      } else if (values.wc === 1 && key === "v") {
                        field.name = "钻进速度(m/h)";
                      }
                      return (
                        <FormItem
                          field={key}
                          key={key}
                          label={field.name}
                          initialValue={useTheInitialValue ? field.value : ""}
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
                  initialValue={useTheInitialValue ? field.value : ""}
                  rules={[
                    { required: true, message: `${field.name} 不能为空` },
                  ]}
                >
                  <Input className="input-component" />
                </FormItem>
              );
            })}
        </div>

        {/* <div className=''>
        <FormItem >
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
        </div> */}
        <FormItem
          className="button-wrapper"
          style={{
            // borderTop: "1px solid #e8e8e8",
            display: "flex",
            justifyContent: "center",
            width: "100%",
          }}
        >
          <div
            style={{ display: "flex", justifyContent: "center", alignItems: "center", gap: "30px", marginTop: datas.work_condition && (datas.work_condition.hasOwnProperty("js")) && Object.keys(datas.work_condition).length > 4 ? "16px" : "13px", paddingLeft: "0px !important" }}
          >
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
              onClick={() => {
                form.resetFields();
              }}
            >
              重置
            </Button>
          </div>
        </FormItem>

      </Form >

    </div >
  );
};

export default MyForm;
