import { Message } from "@arco-design/web-react";
import { basename } from "@tauri-apps/api/path";
import { open } from "@tauri-apps/plugin-dialog";
import { useState } from "react";
import { modelHyperParams } from "../../data/Params";
import "../style.css";
import ParamsForm from "./ParamsForm";

export default function Sider({
  handleSubmit,
  setHistoryFile,
  historyFile,
  extraData,
  setpredictFile,
  historyData,
  setHistoryData,
  jsonData,
  setJsonData,
}) {
  const [predictData, setpredictData] = useState(false);

  const handleUpload = async (filePaths) => {
    // 对 id=0 的历史文件上传处理
    if (Array.isArray(filePaths)) {
      try {
        // 保存所有文件的信息
        const fileInfos = await Promise.all(
          filePaths.map(async (filePath) => {
            const filename = await basename(filePath);
            return { name: filename, path: filePath };
          })
        );

        // 更新历史文件列表
        setHistoryFile(fileInfos);
        setHistoryData(true);


        Message.success(`已成功上传 ${fileInfos.length} 个文件`);
      } catch (error) {
        console.log(error)
      }
      return;
    }

    // 兼容旧代码逻辑 - 处理单文件上传
    if (typeof filePaths === "number") {
      const id = filePaths
      const filePath = await open({
        name: "导入文件",
        multiple: false,
        filters: [{ extensions: ["xlsx", "csv"], name: "" }],
      });

      if (filePath) {
        const filename = await basename(filePath);

        if (id == 0) {
          setHistoryFile([{ name: filename, path: filePath }]);
          setHistoryData(true);

        } else {
          setpredictFile({ name: filename, path: filePath });
          setpredictData(true);
        }

        Message.success(`${filename}上传成功！`);
      } else {
        Message.info("文件上传失败,请重新上传");
      }
    }
  };

  const handleCancel = (id) => {
    if (id === 0) {
      setHistoryData(false);
      setHistoryFile([]);
    } else {
      setpredictData(false);
      setpredictFile({ name: "", path: "" });
    }
  };

  return (
    <>
      <ParamsForm
        data={modelHyperParams}
        predictData={predictData}
        historyData={historyData}
        setHistoryData={setHistoryData}
        historyFile={historyFile}
        handleUpload={handleUpload}
        handleCancel={handleCancel}
        handleSubmit={handleSubmit}
        extraData={extraData}
        jsonData={jsonData}
      />
    </>
  );
}
