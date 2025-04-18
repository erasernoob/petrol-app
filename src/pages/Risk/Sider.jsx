import { Button, Message } from "@arco-design/web-react";
import { basename } from "@tauri-apps/api/path";
import { open } from "@tauri-apps/plugin-dialog";
import { readFile } from "@tauri-apps/plugin-fs";
import { useState } from "react";
import * as XLSX from "xlsx";
import { modelHyperParams } from "../../data/Params";
import FileUpLoaderBtn from "../components/FileUploadBtn";
import "../style.css";
import ParamsForm from "./ParamsForm";

export default function Sider({
  form,
  tabsName,
  datas,
  file = { name: "" },
  setFile,
}) {
  const [historyData, setHistoryData] = useState(false);
  const [predictData, setpredictData] = useState(false);
  const [historyFile, setHistoryFile] = useState({ name: "", filePath: "" });
  const [predictFile, setpredictFile] = useState({ name: "", filePath: "" });
  const [jsonData, setJsonData] = useState({})

  const handleUpload = async (id) => {
    const filePath = await open({
      name: "导入文件",
      multiple: false,
      filters: [{ extensions: ["xlsx", "csv"], name: "" }],
    });

    if (filePath) {
      const filename = await basename(filePath);

      if (id == 0) {
        setHistoryFile(() => ({ name: filename, path: filePath }));
        setHistoryData(true);

        // 读取文件为字节数据
        const fileBytes = await readFile(filePath);

        // 用 xlsx 解析
        const workbook = XLSX.read(fileBytes, { type: "buffer" });
        const sheet = workbook.Sheets[workbook.SheetNames[0]];
        const jsonData = XLSX.utils.sheet_to_json(sheet);
        setJsonData(jsonData.length >= 500 ? jsonData.slice(0, 500) : jsonData)
      }
      else {
        setpredictFile(() => ({ name: filename, path: filePath }));
        setpredictData(true);
      }

      Message.success(`${filename}上传成功！`);
    } else {
      Message.info("文件上传失败,请重新上传");
    }
  };

  const handleSubmit = async (e) => {
    // 输出预测值
    if (e) {

    } else {
      // 开始训练

    }


  }


  const handleCancel = (id) => {
    if (id === 0) {
      setHistoryData(false);
      setHistoryFile({ name: "", path: "" });
    } else {
      setpredictData(false);
      setpredictFile({ name: "", path: "" });
    }
  };

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
      <ParamsForm
        data={modelHyperParams}
        predictData={predictData}
        historyData={historyData}
        handleUpload={handleUpload}
        handleCancel={handleCancel}
        handleSubmit={handleSubmit}
        jsonData={jsonData}
      />
    </>
  );
}
