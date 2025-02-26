import { useState } from "react";
import { Upload, Message, Button } from "@arco-design/web-react";
import { open } from "@tauri-apps/plugin-dialog";

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL;

export default function FileUploader({
  orbit = "default",
  drillState = "default",
  params = "default",
  handleUpload,
  setOrbit,
  setDrillState,
  setParams,
}) {
  return (
    <>
    {orbit !== "default" &&
      (!orbit ? (
        <Button type="primary" onClick={() => handleUpload(1)}>
          导入井眼轨迹
        </Button>
      ) : (
        <Button type="secondary" onClick={() => setOrbit(1)}>
          重新导入
        </Button>
      ))}
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
    {params !== "default" && 
      (!params ? (
        <Button type="primary" onClick={() => handleUpload(3)}>
          导入计算参数
        </Button>
      ) : (
        <Button type="secondary" onClick={() => setParams(false)}>
          重新导入
        </Button>
      ))}
    </>
  );
}
