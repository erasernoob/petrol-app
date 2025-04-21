import { Card, Message } from "@arco-design/web-react";
import { useState } from "react";
import { post } from "../../components/axios";
import ResultPage from "./ResultPage";
import Sider from "./Sider";
export default function DrillPage() {
    const [loading, setLoading] = useState(false);
    // 等待开始计算
    const [waiting, setWaiting] = useState(true);
    const [training, setTraining] = useState(false);
    const [trainSucceed, setTrainSucceed] = useState(false);

    // 修改为数组类型
    const [historyFile, setHistoryFile] = useState([]);
    // 添加历史数据状态
    const [historyData, setHistoryData] = useState(false);
    const [predictFile, setpredictFile] = useState({ name: "", path: "" });
    const [predictResData, setpredictResData] = useState({});
    const [warningData, setWarningData] = useState({});
    const [extraData, setExtraData] = useState({});
    const [jsonData, setJsonData] = useState({});

    const [elapsedTime, setElapsedTime] = useState(0)

    console.log(trainSucceed)

    // 区分是否展示预警结果
    const [showWarnRes, setShowWarnRes] = useState(false)

    const handleTrainStart = async () => {
        setTraining(true);
        setLoading(true);
        setWaiting(false);
    }
    const handleTrainingComplete = () => {
        Message.success("模型训练完成！点击按钮输出预测结果！");
        setTraining(false);
        setWaiting(true);
        setElapsedTime(0)
    };

    const handleSubmit = async (e) => {
        // warningData 对应的是预测图 
        // predictData 对应的是预警图 
        if (typeof e !== 'number') {
            handleTrainStart()
            const intervalId = setInterval(() => {
                setElapsedTime((prev) => {
                    console.log(prev); // 打印的是最新的值
                    if (prev === 5) {
                        return 72365;
                    } else {
                        return prev + 1;
                    }
                });
            }, 1000);
            try {
                setLoading(true);
                setWaiting(false);
                e.target_file_path = predictFile?.path
                // 开始训练 

                const response = await post("/risk/train", e)
                clearInterval(intervalId)
                handleTrainingComplete()
                setTrainSucceed(true)

                // setShowWarnRes(false)
            } catch (error) {
                clearInterval(intervalId)
                setWaiting(true);
                setTraining(false)
                setLoading(false);
                setElapsedTime(0)
                console.log(error)
                Message.error("计算内部出现错误，请检查输入参数！");
                Message.error(error?.response?.data?.detail)
            } finally {
                clearInterval(intervalId)
                setElapsedTime(0)
                setWaiting(true);
                setTraining(false)
                setLoading(false);
            }
        } else if (e == 1) {
            try {
                setLoading(true);
                setWaiting(false);

                // get the predict data 
                const response = await post("/risk/predict")
                setWarningData(response)
                const { RMSE, R, MAE } = response
                setExtraData({ RMSE, R, MAE })

                // get the warning result
                const res = await post("/risk/warning")
                setpredictResData(res)
                setLoading(false)

            } catch (error) {
                setWaiting(true)
                setLoading(false)
                Message.error(`计算内部出现错误! ${error?.response?.data?.detail}`);
                Message.error("请先训练模型后再计算！");
            }
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
                    setShowWarnRes={setShowWarnRes}
                    trainSucceed={trainSucceed}
                    warningData={warningData}
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
                    elapsedTime={elapsedTime}
                    setElapsedTime={setElapsedTime}
                    loading={loading}
                    trainSucceed={trainSucceed}
                    training={training}
                    setWaiting={setWaiting}
                    waiting={waiting}
                    warningData={warningData}
                    predictData={predictResData}
                    showWarnRes={showWarnRes}
                    setExtraData={setExtraData}
                />
            </Card>
        </div>
    );
}
