import { Card, Message } from "@arco-design/web-react";
import Papa from "papaparse";
import { useEffect, useState } from "react";
import { useLocation } from "react-router-dom";
import { post } from "../../components/axios";
import { drill_vibration } from "../../data/Params";
import Sider from "../Limit/Sider";
import DynamicForm from "../components/DynamicForm";
import { dealWithTheDataUnit } from "../utils/utils";
import ResultPage from "./ResultPage";

const subRoutesOptions = [
  { label: "MSE", value: 1 },
  { label: "粘滑振动", value: 2 },
];
const tabs = ["基本钻具参数", "钻井液", "计算参数"];

const typeOptions = ["角位移", "角速度", "角加速度", "钻头扭矩", "相轨迹"];

export default function DrillPage() {
  // 从localStorage读取保存的选项
  const storedActiveRoute = localStorage.getItem("drillActiveRoute");
  const [activeRoute, setActiveRoute] = useState(
    storedActiveRoute ? parseInt(storedActiveRoute) : 1
  );

  const [loading, setLoading] = useState(false);
  const [extraData, setExtraData] = useState({});
  const [waiting, setWaiting] = useState(true);
  const [chartData, setChartData] = useState([]);
  const [fileList, setFileList] = useState([{ name: "", path: "" }]);
  const [file, setFile] = useState({ name: "", path: "" });
  const [resultCardVisible, setResultCardVisible] = useState(false);

  const handleCalculate = async () => {
    // 初始化
    setExtraData({})

    if (!file.path) return;
    try {
      setWaiting(false);
      setLoading(true);
      const response = await post(
        "/drill/mse",
        JSON.stringify({ file_path: file.path })
      );
      const res = Papa.parse(response, {
        header: true,
        dynamicTyping: true,
      }).data;
      // 判断是否需要优化 
      if (res[0].UCS) {
        const r = await post("/drill/mse/optimized")
        // 得到优化建议
        setExtraData(r)
      }

      setChartData(res);
      setLoading(false);
    } catch (error) {
      console.log(error);
      setLoading(false);
      setWaiting(true);
      Message.error(error?.response?.data?.detail);
      Message.error("计算内部出现错误，请检查输入参数！");
    }
  };

  const handleExport = () => { };

  const handleSubmit = async (data) => {
    try {
      setWaiting(false);
      setLoading(true);
      dealWithTheDataUnit(data, 4);
      const response = await post("/drill/vibration", JSON.stringify(data));
      const res = Papa.parse(response, {
        header: true,
        dynamicTyping: true,
      }).data;
      setChartData(res);
      setLoading(false);
    } catch (error) {
      console.log(error);
      setLoading(false);
      setWaiting(true);
      Message.error(error?.response?.data?.detail);
      Message.error("计算内部出现错误，请检查输入参数！");
    }
  };

  // 添加一个useEffect检查localStorage中的变化
  useEffect(() => {
    // 初始检查
    const stored = localStorage.getItem("drillActiveRoute");
    console.log(stored);

    const checkStorageValue = () => {
      const stored = localStorage.getItem("drillActiveRoute");

      if (stored && parseInt(stored) !== activeRoute) {
        setActiveRoute(parseInt(stored));
      }
    };

    // 定义storage事件处理函数
    const handleStorageChange = (e) => {
      if (e.key === "drillActiveRoute") {
        checkStorageValue();
      }
    };

    // 添加事件监听
    window.addEventListener("storage", handleStorageChange);

    // 初始检查
    checkStorageValue();

    // 清理函数
    return () => {
      window.removeEventListener("storage", handleStorageChange);
    };
  }, []);

  // 单独的useEffect用于监听URL变化
  const location = useLocation();
  useEffect(() => {
    // 检查URL中是否有类型参数
    const searchParams = new URLSearchParams(location.search);
    const typeParam = searchParams.get("type");

    if (typeParam) {
      const newActiveRoute = parseInt(typeParam);
      if (newActiveRoute !== activeRoute) {
        setActiveRoute(newActiveRoute);
        localStorage.setItem("drillActiveRoute", typeParam);

        // 清除状态，准备重新加载
        setLoading(false);
        setWaiting(true);
        setChartData([]);
      }
    }
  }, [location.search, activeRoute]);

  // 原有的useEffect保持不变
  useEffect(() => {
    setLoading(false);
    setWaiting(true);
    setChartData([]);

    if (activeRoute === 2) {
      setTimeout(() => {
        setResultCardVisible(true);
      }, 100);
    } else {
      setResultCardVisible(false);
    }
  }, [activeRoute]);

  // 处理activeRoute变化的函数
  const handleActiveRouteChange = (value) => {
    // 设置状态
    setActiveRoute(value);
    // 更新localStorage
    localStorage.setItem("drillActiveRoute", value.toString());

    // 使用history对象更新URL
    const newSearch = `?type=${value}&t=${Date.now()}`;
    window.history.pushState({}, "", `${location.pathname}${newSearch}`);

    // 清除状态，准备重新加载
    setLoading(false);
    setWaiting(true);
    setChartData([]);
  };

  return (
    <div className="main-content">
      <Card
        title="参数"
        style={{
          width: activeRoute === 1 ? "100%" : "30%",
          height: "100%",
        }}
        className="parameter-card"
      >
        <Sider
          subRouteOptions={subRoutesOptions}
          loading={loading}
          waiting={waiting}
          handleExport={handleExport}
          chartData={chartData}
          setActiveRoute={handleActiveRouteChange}
          activeRoute={activeRoute}
          extraData={extraData}
          handleCalculate={handleCalculate}
          file={file}
          setFile={setFile}
          fileList={fileList}
          form={
            activeRoute === 2 ? (
              <DynamicForm
                datas={drill_vibration}
                handleSubmit={handleSubmit}
                tabs={tabs}
                file={{ name: "for-vibration", path: "" }}
                drill={true}
              />
            ) : (
              "default"
            )
          }
          setFileList={setFileList}
        />
      </Card>
      {activeRoute === 2 && (
        <Card
          title="计算结果"
          style={{ flex: "1", marginLeft: "5px" }}
          bodyStyle={{ padding: "10px", height: "100%", flex: 1 }}
          className={`result-card ${resultCardVisible ? "result-card-visible" : "result-card-entering"
            }`}
        >
          <ResultPage
            typeOptions={typeOptions}
            loading={loading}
            chartData={chartData}
            waiting={waiting}
          />
        </Card>
      )}
    </div>
  );
}
