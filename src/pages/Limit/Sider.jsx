import { Button, Message, Radio, Card } from "@arco-design/web-react";
import { basename } from "@tauri-apps/api/path";
import { open } from "@tauri-apps/plugin-dialog";
import { useState } from "react";
import { defaultFileList } from ".";
import FileUploader from "../components/FileUpLoader";
import MSEResult from "../Drill/MSEResult";
import "../style.css";

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
    width: activeRoute === 1 ? "15%" : "100%",
    marginTop: activeRoute === 1 ? "0" : "100%",
  };

  const Tabs = (
    <div
      className={
        subRouteOptions.length != 2 ||
        (subRouteOptions.length == 2 && activeRoute == 2)
          ? "full-width-radio-group"
          : "mse-width-radio-group"
      }
    >
      <RadioGroup
        type="button"
        size="large"
        name="chart"
        defaultValue={activeRoute}
        onChange={(value) => {
          // 在实际更改路由之前，添加一个类来触发过渡动画
          const mainContent = document.querySelector(".main-content");
          if (mainContent) {
            mainContent.classList.add("route-transitioning");
          }

          // 延迟更新状态，给 CSS 过渡一些时间来开始
          setTimeout(() => {
            setActiveRoute(value);
            setOrbit(false);
            setDrillState(false);
            setWaiting(true);
            setLoading(false);
            setChartData([]);
            setFile({ name: "", path: "" });
            setFileList(defaultFileList);
            setParams(false);

            // 动画结束后移除过渡类
            setTimeout(() => {
              if (mainContent) {
                mainContent.classList.remove("route-transitioning");
              }
            }, 2000); // 增加到 1200ms 与 CSS 过渡时间匹配
          }, 50);
        }}
        options={subRouteOptions}
      ></RadioGroup>
    </div>
  );

  const handleUpload = async (id) => {
    console.log(id);
    const filePath = await open({
      name: "导入文件",
      multiple: false,
      filters: [{ extensions: ["xlsx"], name: "" }],
    });

    if (filePath) {
      const filename = await basename(filePath);
      if (id === 1) {
        setFile({ name: filename, path: filePath });
        setFileList((prev) => ({
          ...prev,
          orbit: { name: filename, path: filePath },
        }));
      } else if (id == 2) {
        setFileList((prev) => ({
          ...prev,
          drill: { name: filename, path: filePath },
        }));
      } else if (id == 3) {
        // 上传参数
        // 计算参数
        setFile({ name: filename, path: filePath });
      }
      Message.success(`${filename}导入成功！`);
      if (id === 1) {
        setOrbit(true);
      } else if (id === 2) {
        setDrillState(true);
      } else if (id == 3) {
        setParams(true);
      } else {
        // 重置所有的状态
        setFileList({
          orbit: { name: "", path: "" },
          drill: { name: "", path: "" },
        });
        setFile({ name: "", path: "" });
        Message.info("文件上传失败,请重新导入");
      }
    }
  };
  const handleCancel = (id) => {
    if (id === 1) {
      setOrbit(false);
      setFile({ name: "", path: "" });
      setFileList((prev) => ({ ...prev, orbit: { name: "", path: "" } }));
    } else if (id === 2) {
      setDrillState(false);
      setFileList((prev) => ({ ...prev, drill: { name: "", path: "" } }));
    } else {
      setParams(false);
      setFile({ name: "", path: "" });
    }
  };

  return (
    <div className="input-page" style={{ paddingTop: "5px" }}>
      {form === "default" ? (
        <>
          <div
            className="file-uploader-tabs-container"
            style={{
              display: "flex",
              alignItems: "center",
              gap: "100px",
              justifyContent: "space-between",
              marginTop: "3px",
            }}
          >
            <div className="mse-tabs-container">{Tabs}</div>
            <div
              style={{
                display: "flex",
                alignItems: "center",
                gap: "20px",
                marginRight: "80px",
              }}
            >
              <FileUploader
                params={params}
                setParams={setParams}
                handleCancel={handleCancel}
                handleUpload={handleUpload}
              />
              <Button
                type="primary"
                className="button submit-button"
                disabled={!params}
                onClick={handleCalculate}
              >
                计算
              </Button>
            </div>
          </div>
          <div className="mse-result-page">
          <Card
          title="计算结果"
          className="mse-result-card"
          bodyStyle={{ height: "100%", flex: 1, border: "0px !important" }}
        >
            <MSEResult
              loading={loading}
              waiting={waiting}
              handleExport={handleExport}
              chartData={chartData}
            />
        </Card>


         </div>
        </>
      ) : (
        // to distinct the vibration and the limit page
        <>
          {Tabs}
          {subRouteOptions.length >= 3 && (
            <div className="file-uploader"
            style={{
              paddingTop: "0px",
            }}
            >
              <FileUploader
                orbit={orbit}
                setOrbit={setOrbit}
                handleCancel={handleCancel}
                setDrillState={setDrillState}
                drillState={activeRoute >= 3 ? drillState : "default"}
                handleUpload={handleUpload}
              />
            </div>
          )}
          <div className="input-form">{form}</div>
        </>
      )}
    </div>
  );
}
