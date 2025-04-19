import {
    Button,
    Card,
    Form,
    Grid,
    Input,
    Message,
    Tag
} from "@arco-design/web-react";
import FileUpLoaderBtn from "../components/FileUploadBtn";
import FileUploadDisplay from "./FileDataDisplayer";

export default function ParamsForm({
    data = {},
    handleSubmit,
    extraData = { "RMSE": "", "R": "", "MAE": "" },
    historyData,
    handleUpload,
    predictData,
    handleCancel,
    jsonData,
}) {
    const FormItem = Form.Item;
    const [form] = Form.useForm();
    const Row = Grid.Row;
    const Col = Grid.Col;

    // 文件上传前的检查
    const beforeUpload = (file) => {
        const isExcel =
            file.type ===
            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet" ||
            file.type === "application/vnd.ms-excel" ||
            file.name.endsWith(".csv");
        if (!isExcel) {
            Message.error("只能上传Excel或CSV文件！");
            return false;
        }
        return true;
    };

    // 上传文件改变时的处理函数
    const onChange = (fileList, file) => {
        if (file.status === "done") {
            // 文件上传成功
            handleUpload && handleUpload(file.response || file.originFile);
            Message.success(`${file.name} 上传成功`);
        } else if (file.status === "error") {
            Message.error(`${file.name} 上传失败`);
        }
    };

    // Custom styles for the inputs in this component only
    const inputStyle = {
        width: "80%",
        height: "32px",
    };

    const items =
        Object.keys(data).length !== 0 ? (
            Object.keys(data).map((key, idx) => {
                return (
                    <Col span={12}>
                        <FormItem
                            label={key}
                            field={data[key].field}
                            initialValue={data[key].value}
                        >
                            <Input style={inputStyle} />
                        </FormItem>
                    </Col>
                );
            })
        ) : (
            <></>
        );

    return (
        <>

            <div className="file-uploader">
                <FileUpLoaderBtn
                    uploadStat={historyData}
                    uploadText={"导入历史样本集"}
                    handleCancel={handleCancel}
                    handleUpload={handleUpload}
                    id={0}
                />
                <Button type="primary" disabled={!historyData} onClick={() => handleSubmit()}>模型训练</Button>
            </div>
            <Form
                form={form}
                onSubmit={handleSubmit}
                layout="horizontal"
                labelAlign="right"
                labelCol={{ span: 9 }}
                wrapperCol={{ span: 15 }}
            >
                <div
                    style={{
                        height: "76vh",
                        display: "flex",
                        flexDirection: "column",
                        justifyContent: "space-between",
                        gap: "1px !important",
                        marginTop: "10px",
                    }}
                >


                    <Card
                        title="学习参数"
                        bordered={false}
                        bodyStyle={{
                            height: "36vh",
                            borderBottom: "1px solid #e5e6eb",
                            paddingTop: "10px",
                            paddingBottom: "0px",
                            overflowY: "auto",
                            overflowX: "auto",
                        }}
                    >
                        {!historyData ? (
                            <>
                                <div
                                    style={{
                                        width: "100%",
                                        height: "100%",
                                        display: "flex",
                                        justifyContent: "center",
                                        alignItems: "center",
                                    }}
                                >
                                    请先导入历史样本
                                </div>
                            </>
                        ) : (
                            <>
                                <FileUploadDisplay jsonData={jsonData} />
                            </>
                        )}
                    </Card>

                    <Card
                        title="设置模型超参数"
                        bordered={false}
                        style={{ marginBottom: 16 }}
                        bodyStyle={{
                            borderBottom: "1px solid #e5e6eb",
                            paddingTop: "10px",
                            paddingBottom: "0px",
                        }}
                    >
                        <Row gutter={16}>{items}</Row>
                    </Card>

                    <div
                        style={{
                            border: "1px solid #e5e6eb",
                            margin: "0 3px",
                            paddingTop: "10px",
                            paddingBottom: "15px",
                        }}
                    >
                        <span
                            style={{
                                display: "flex",
                                justifyContent: "center",
                                alignItems: "center",
                                marginBottom: "5px",
                                fontSize: "1rem",
                                fontWeight: "400",
                                color: "",
                            }}
                        >
                            模型误差
                        </span>
                        <Row gutter={16}>
                            <Col span={8}>
                                <span
                                    style={{
                                        display: "flex",
                                        justifyContent: "center",
                                        alignItems: "center",
                                    }}
                                >
                                    <span style={{ marginRight: "10px", textAlign: "center" }}>
                                        MAE：
                                    </span>
                                    <Tag size="large" style={{ width: "100px" }}>
                                        {extraData.MAE}
                                    </Tag>
                                </span>
                            </Col>
                            <Col span={8}>
                                <span
                                    style={{
                                        display: "flex",
                                        justifyContent: "center",
                                        alignItems: "center",
                                    }}
                                >
                                    <span style={{ marginRight: "10px", textAlign: "center" }}>
                                        RMSE：
                                    </span>
                                    <Tag size="large" style={{ width: "100px" }}>
                                        {extraData.RMSE}
                                    </Tag>
                                </span>
                            </Col>
                            <Col span={8}>
                                <span
                                    style={{
                                        display: "flex",
                                        justifyContent: "center",
                                        alignItems: "center",
                                    }}
                                >
                                    <span style={{ marginRight: "10px", textAlign: "center" }}>
                                        R²:
                                    </span>
                                    <Tag size="large" style={{ width: "100px" }}>
                                        {extraData.R}
                                    </Tag>
                                </span>
                            </Col>
                        </Row>
                    </div>
                </div>

                <div>
                    <Row gutter={16} style={{ marginTop: "20px" }}>
                        <Col span={12} style={{ textAlign: "center" }}>
                            <FileUpLoaderBtn
                                uploadStat={predictData}
                                uploadText={"导入预测数据"}
                                handleCancel={handleCancel}
                                handleUpload={handleUpload}
                                style={{
                                    width: "95%",
                                }}
                            />
                        </Col>
                        <Col span={12} style={{ textAlign: "center" }}>
                            <Button
                                type="primary"
                                size="large"
                                style={{ width: "95%" }}
                                htmlType="submit"
                                disabled={!predictData}
                            >
                                输出预测值
                            </Button>
                        </Col>
                    </Row>
                </div>
            </Form>
        </>
    );
}
