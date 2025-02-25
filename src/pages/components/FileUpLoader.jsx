import { useState } from "react";
import { Upload, Message, Button } from "@arco-design/web-react";
import { open } from "@tauri-apps/plugin-dialog";

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL;

export default function FileUploader({
  orbit,
  drillState = "default",
  handleUpload,
  setOrbit,
  setDrillState,
}) {
  return (
    <>
      {!orbit ? (
        <Button type="primary" onClick={() => handleUpload(1)}>
          导入井眼轨迹
        </Button>
      ) : (
        <Button type="secondary" onClick={() => setOrbit(false)}>
          重新导入
        </Button>
      )}
      {drillState != "default" &&
        (!drillState ? (
          <Button type="primary" onClick={() => handleUpload(2)}>
            导入钻具状态
          </Button>
        ) : (
          <Button type="secondary" onClick={() => setDrillState(false)}>
            重新导入
          </Button>
        ))}
    </>
  );
}
