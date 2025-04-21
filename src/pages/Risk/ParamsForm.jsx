import {
  Button,
  Card,
  Form,
  Grid,
  Input,
  Message,
  Tag,
  Upload
} from "@arco-design/web-react";
import { useEffect, useState } from "react";
import { post } from "../../components/axios";
import FileUpLoaderBtn from "../components/FileUploadBtn";

export default function ParamsForm({
  data = {},
  handleSubmit,
  extraData = { RMSE: "", R: "", MAE: "" },
  historyData = true,
  setHistoryData,
  historyFile,
  setShowWarnRes,
  warningData,
  trainSucceed,
  handleRiskResult,
  handleUpload,
  predictData,
  handleCancel,
  jsonData,
}) {
  const FormItem = Form.Item;
  const [form] = Form.useForm();
  const Row = Grid.Row;
  const Col = Grid.Col;

  // 创建转换文件格式的函数
  const createFileList = (files) => {
    if (!files || files.length === 0) return [];
    return files.map((file, index) => ({
      uid: `file-${index}`,
      name: file.name, // 确保使用原始文件名
      status: "done",
      url: file.path, // 保存实际文件路径
    }));
  };

  // 初始化文件列表
  const [uploadFileList, setUploadFileList] = useState([]);

  // 当 historyFile 变化时更新文件列表
  useEffect(() => {
    if (historyFile && Array.isArray(historyFile) && historyFile.length > 0) {
      const newFileList = createFileList(historyFile);
      setUploadFileList(newFileList);
    } else {
      setUploadFileList([]);
    }
  }, [historyFile]);

  // 自定义上传请求
  const customRequest = async (options) => {
    const { onSuccess, file, onError } = options;

    try {
      const formData = new FormData()
      formData.append('file', file)
      const res = await post("/risk/upload", formData, {
        headers: {
          'Content-Type': 'multipart/form-data',  // 让 Axios 知道上传的是表单数据
        }
      })
      onSuccess({
        url: URL.createObjectURL(file),
        name: file.name
      })

    } catch (error) {
      Message.error(error?.response?.data?.detail)
      onError()
    }
  };

  // 处理上传文件变化
  const handleFileChange = (fileList) => {
    const files = fileList.map((file) => {
      return file;
    });

    setUploadFileList(files);

    // 如果有文件，就更新 historyData 状态
    if (files && files.length > 0) {
      setHistoryData(true);
      // 将上传的文件转换为符合 handleUpload 需要的格式
      const paths = files.map((file) => file.url);
      // handleUpload(paths);
    } else {
      // 如果没有文件，设置 historyData 为 false 并调用 handleCancel
      setHistoryData(false);
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
          <Col span={12} key={idx}>
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
      <Form
        form={form}
        onSubmit={handleSubmit}
        layout="horizontal"
        labelAlign="right"
        labelCol={{ span: 9 }}
        wrapperCol={{ span: 15 }}
      >
        <div className="file-uploader">
          <Upload
            multiple
            customRequest={customRequest}
            onChange={handleFileChange}
            fileList={uploadFileList}
            showUploadList={false}
            accept=".xlsx,.xls,.csv"
          >
            <Button type="primary">导入历史样本集</Button>
          </Upload>
          <FileUpLoaderBtn
            uploadStat={predictData}
            uploadText={"导入预测井"}
            handleCancel={handleCancel}
            handleUpload={handleUpload}
            id={1}
          />
          <Button
            disabled={!historyData || !predictData}
            htmlType="submit"
            type="primary"
          // onClick={() => handleSubmit()}
          >
            模型训练
          </Button>
        </div>

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
              paddingBottom: "0px",
              overflowY: "auto",
              overflowX: "hidden",
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
                {/* 文件列表显示部分 - 删除上传按钮 */}
                {uploadFileList.length > 0 && (
                  <div style={{ marginBottom: "15px" }}>
                    <Upload
                      fileList={uploadFileList}
                      onChange={handleFileChange}
                      showUploadList={{
                        showRemoveIcon: true,
                        showPreviewIcon: false,
                      }}
                      onError={(file) => {
                        // 自定义处理上传错误
                        console.error('上传失败', file);
                      }}
                      customRequest={customRequest}
                      listType="text"
                      // 完全隐藏上传按钮
                      action=""
                      autoUpload={false}
                      // 使用一个空的 children 来替代默认的上传按钮
                      children={null}
                      style={{ marginBottom: "15px" }}
                    />
                  </div>
                )}
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
              <Button
                type="primary"
                size="large"
                style={{ width: "95%" }}
                disabled={!trainSucceed}
                onClick={() => handleSubmit(1)}
              >
                输出预测结果
              </Button>
            </Col>
            <Col span={12} style={{ textAlign: "center" }}>
              <Button
                type="primary"
                size="large"
                style={{ width: "95%" }}
                onClick={() => setShowWarnRes(true)}
                disabled={!trainSucceed}
              >
                输出预警结果
              </Button>
            </Col>

          </Row>
        </div>
      </Form>
    </>
  );
}
