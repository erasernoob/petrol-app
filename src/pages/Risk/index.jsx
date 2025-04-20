import { Card, Message } from "@arco-design/web-react";
import { useState } from "react";
import { post } from "../../components/axios";
import ResultPage from "./ResultPage";
import Sider from "./Sider";
export default function DrillPage() {
    const [loading, setLoading] = useState(false);
    // 等待开始计算
    const [waiting, setWaiting] = useState(true);
    const [training, setTraning] = useState(false);
    // 修改为数组类型
    const [historyFile, setHistoryFile] = useState([]);
    // 添加历史数据状态
    const [historyData, setHistoryData] = useState(false);

    const [predictFile, setpredictFile] = useState({ name: "", path: "" });
    const [predictResData, setpredictResData] = useState({});
    const [warningData, setWarningData] = useState({});
    const [extraData, setExtraData] = useState({});
    const [jsonData, setJsonData] = useState({});

    const totalTrainingTime = 10;

    const handleSubmit = async (e) => {
        try {
            if (e) {
                setLoading(true);
                setWaiting(false);
                // 修改：使用第一个历史文件的路径
                if (historyFile.length > 0) {
                    e.file_path = historyFile[0].path;
                    let response = await post("/risk/warning");
                    setWarningData(response);
                    setExtraData({
                        MAE: response.MAE,
                        RMSE: response.RMSE,
                        R: response.R,
                    });
                }

                e.file_path = predictFile.path;
                console.log(predictFile);
                const response = await post("/risk/predict", e);
                let res = response.data;
                // 预测图
                setpredictResData(res);
            } else {
                // 训练
                setTraning(true);
                setLoading(true);
                setWaiting(false);
            }
        } catch (error) {
            Message.error("计算内部出现错误，请检查输入参数！");
            console.log(error);
        } finally {
            setWaiting(false);
            setLoading(false);
        }
    };

    return (
        <div className="main-content">
            <Card
                title="参数"
                style={{
                    width: "30%",
                    height: "100%",
                    padding: "",
                }}
                bodyStyle={{
                    height: "100%",
                    flex: 1,
                }}
            >
                <Sider
                    handleSubmit={handleSubmit}
                    setHistoryFile={setHistoryFile}
                    historyFile={historyFile}
                    historyData={historyData}
                    setHistoryData={setHistoryData}
                    extraData={extraData}
                    setpredictFile={setpredictFile}
                    jsonData={jsonData}
                    setJsonData={setJsonData}
                />
            </Card>
            <Card
                title="计算结果"
                style={{ flex: "1", marginLeft: "5px" }}
                bodyStyle={{ padding: "10px", height: "100%", flex: 1 }}
            >
                <ResultPage
                    loading={loading}
                    training={training}
                    setTraining={setTraning}
                    setWaiting={setWaiting}
                    waiting={waiting}
                    totalTrainingTime={totalTrainingTime}
                    warningData={warningData}
                    predictData={predictResData}
                />
            </Card>
        </div>
    );
}
