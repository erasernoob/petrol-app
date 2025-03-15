import { Radio,Button, Message } from "@arco-design/web-react";
import { open } from "@tauri-apps/plugin-dialog";
import "../style.css";
import { basename } from "@tauri-apps/api/path";
import { useState } from "react";
import FileUploader from "../components/FileUpLoader";
import MSEResult from "../Drill/MSEResult";
import { defaultFileList } from ".";

const RadioGroup = Radio.Group;

export default function Sider({
  form = "default",
  activeRoute,
  subRouteOptions,
  setActiveRoute,
  setWaiting,
  setLoading,
  setChartData,
  loading,
  waiting,
  handleCalculate,
  handleExport,
  chartData,
  setFile,
  setFileList,
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
        // file重置
        setOrbit(false)
        setDrillState(false)
        setWaiting(true)
        setLoading(false)
        setChartData([])
        setFile({name: '', path: ''})
        setFileList(defaultFileList)

        setParams(false)
      }}
      options={subRouteOptions}
    ></RadioGroup>
  );

    const handleUpload = async (id) => {
    console.log(id)
    const filePath = await open({
      name: "导入文件",
       multiple: false, 
       filters: [{extensions: ['xlsx'], name: ''}],
    })
 
    if (filePath) {
      const filename = await basename(filePath)
      if (id === 1) {
        setFile({name: filename, path: filePath})
        setFileList(prev => ({...prev, orbit: {name: filename, path: filePath}}))
      } else if (id == 2) {
        setFileList((prev) => ({...prev, drill: {name: filename, path: filePath}}))
      } else if (id == 3) {
        // 上传参数
        // 计算参数
        setFile({name: filename, path: filePath})
      }
      Message.success(`${filename}导入成功！`)
      if (id === 1) {
        setOrbit(true)
      } else if (id === 2) {
        (setDrillState(true))
      } else if (id == 3) {
        setParams(true)
      } else {
        // 重置所有的状态
      setFileList({orbit: {name: '', path: ''}, drill: {name: '', path: ''}})
      setFile({name: '', path: ''})
      Message.info('文件上传失败,请重新导入')
    }
  }
}
  const handleCancel = (id) => {
    if (id === 1) {
      setOrbit(false)
      setFile({name: '', path: ''})
      setFileList(prev => ({...prev, orbit: {name: '', path: ''}}))
    } else if(id === 2) {
      setDrillState(false)
      setFileList(prev => ({...prev, drill: {name: '', path: ''}}))
    } else {
      setParams(false)
      setFile({name: '', path: ''})
    }
  }



  return (
    <div className="input-page" style={{ paddingTop: "5px" }}>
      {Tabs}
      {form === "default" ? (
        <>
          <div className="file-uploader" style={uploaderStyle}>
            <FileUploader
              params={params}
              setParams={setParams}
              handleCancel={handleCancel}
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
            <MSEResult loading={loading} waiting={waiting} handleExport={handleExport} chartData={chartData} />
          </div>
        </>
      ) : (
        // to distinct the vibration and the limit page
        <>
          { subRouteOptions.length >= 3 && <div className="file-uploader">
            <FileUploader
              orbit={orbit}
              setOrbit={setOrbit}
              handleCancel={handleCancel}
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
