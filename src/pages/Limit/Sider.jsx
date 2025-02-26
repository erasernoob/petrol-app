import { Radio, Form, Input, Button, Message } from "@arco-design/web-react";
import { open } from "@tauri-apps/plugin-dialog";
import "../style.css";
import { basename } from "@tauri-apps/api/path";
import { useState } from "react";
import FileUploader from "../components/FileUpLoader";
import { path } from "@tauri-apps/api";
import MSEResult from "./MSEResult";

const RadioGroup = Radio.Group;

export default function Sider({
  form = "default",
  activeRoute,
  subRouteOptions,
  setActiveRoute,
  fileList,
  setFileList,
  handleCalculate,
}) {
  const [orbit, setOrbit] = useState(false);
  const [drillState, setDrillState] = useState(false);
  // FOR MSE
  const [params, setParams] = useState(false);
  const uploaderStyle = {
    width: activeRoute === 1 ? '15%' : '100%',
    marginTop: activeRoute === 1 ? '0' : '100%',
  }



  const Tabs = (
    <RadioGroup
      type="button"
      size="large"
      name="chart"
      defaultValue={1}
      onChange={(value) => {
        setActiveRoute(value);
        // 将filelist重置
        setFileList([])
        setOrbit(false)
        setDrillState(false)
        setParams(false)
      }}
      options={subRouteOptions}
    ></RadioGroup>
  );

  const handleUpload = async (id) => {
    const filePath = await open({ multiple: false });
    if (filePath) {
      const filename = await basename(filePath);
      setFileList((prev) => [...prev, { name: filename, path: filePath }]);
      Message.success(`${filename}导入成功！`);
      if (id === 1) {
        setOrbit(true);
      } else if (id === 2) {
        setDrillState(true);
      } else if (id === 3) {
        setParams(true);
      }
    } else {
      Message.info("文件上传失败,请重新导入");
    }
  };

  return (
    <div className="input-page" style={{ paddingTop: "5px" }}>
      {Tabs}
      {form === "default" ? (
        <>
          <div className="file-uploader" style={uploaderStyle}>
            <FileUploader
              params={params}
              setParams={setParams}
              handleUpload={handleUpload}
            ></FileUploader>
          <Button
            type="primary"
            disabled={
              !params
            }
            onClick={handleCalculate}
          >
            计算
          </Button>
          </div>
          <div className="mse-result-page">
            <MSEResult />
          </div>
        </>
      ) : (
        // to distinct the vibration and the limit page
        <>
          { subRouteOptions.length >= 3 && <div className="file-uploader">
            <FileUploader
              orbit={orbit}
              setOrbit={setOrbit}
              setDrillState={setDrillState}
              drillState={activeRoute >= 3 ? drillState : "default"}
              handleUpload={handleUpload}
            />
          </div>}
          <div className="input-form">
            {form}
          </div>
        </>
      )}
    </div>
  );
}
