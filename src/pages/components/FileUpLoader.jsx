import { useState } from "react";
import { Upload, Message, Button } from "@arco-design/web-react";
import { open } from "@tauri-apps/plugin-dialog";

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL;

export default function FileUploader({
  orbit = "default",
  drillState = "default",
  params = "default",
  handleUpload,
  handleCancel,
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
        <Button type="secondary" onClick={() => handleCancel(1)}>
          重新导入
        </Button>
      ))}
      {drillState != "default" &&
        (!drillState ? (
          <Button type="primary" onClick={() => handleUpload(2)}>
            导入钻具组合
          </Button>
        ) : (
          <Button type="secondary" onClick={() => handleCancel(2)}>
            重新导入
          </Button>
        ))}
    {params !== "default" && 
      (!params ? (
        <Button 
        type="primary" 
        onClick={() => handleUpload(3)}
        style={{width:"150px"}}
        >
          导入计算参数
        </Button>
      ) : (
        <Button type="secondary" onClick={() => handleCancel(3)}>
          重新导入
        </Button>
      ))}
    </>
  );
}
