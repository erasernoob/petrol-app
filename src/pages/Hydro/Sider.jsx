import { Button, Message } from "@arco-design/web-react";
import { basename } from "@tauri-apps/api/path";
import { open } from "@tauri-apps/plugin-dialog";
import { useState } from "react";
import FileUpLoader from "../components/FileUpLoader";
import "../style.css";

export default function Sider({
  form,
  tabsName,
  handleSubmit,
  datas,
  file = { name: "" },
  setFile,
}) {
  const [orbit, setOrbit] = useState(false);

  const handleUpload = async (id) => {
    const filePath = await open({
      name: "导入文件",
      multiple: false,
      filters: [{ extensions: ["xlsx"], name: "" }],
    });
    if (filePath) {
      const filename = await basename(filePath);
      setFile(() => ({ name: filename, path: filePath }));
      Message.success(`${filename}上传成功！`);
      setOrbit((prev) => !prev);
    } else {
      Message.info("文件上传失败,请重新上传");
    }
  };

  const handleCancel = (id) => {
    if (id === 1) {
      setOrbit(false);
      setFile({ name: "", path: "" });
    }
  };

  return (
    <div className="input-page">
      <div className="file-uploader">
        <FileUpLoader
          handleCancel={handleCancel}
          orbit={orbit}
          setOrbit={setOrbit}
          handleUpload={handleUpload}
        />
      </div>
      <div className="input-form">{form}</div>
      <div
        style={{
          display: "flex",
          justifyContent: "center",
          gap: "30px",
          marginTop: "15px",
        }}
      >
        <Button
          type="primary"
          className="button submit-button"
          disabled={file.name === ""}
          onClick={() => handleSubmit(form)}
        >
          计算
        </Button>
        <Button
          type="primary"
          className="button reset-button"
          onClick={() => form.resetFields()}
        >
          重置
        </Button>
      </div>
    </div>
  );
}
