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
    const [trainEnd, setTrainEnd] = useState(false);

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

    // 区分是否展示预警结果
    const [showWarnRes, setShowWarnRes] = useState(false)
    console.log(showWarnRes)

    const totalTrainingTime = 72005;



    const handleTrainStart = async () => {
        setTraining(true);
        setLoading(true);
        setWaiting(false);
    }
    const handleTrainingComplete = () => {
        Message.success("模型训练完成！");
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
                setElapsedTime((prev) => prev + 1)
            }, 1000)
            try {
                setLoading(true);
                setWaiting(false);
                e.target_file_path = predictFile?.path
                // 开始训练 

                const response = await post("/risk/train", e)
                clearInterval(intervalId)
                handleTrainingComplete()

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
            // get the predict data 

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
                    training={training}
                    setWaiting={setWaiting}
                    waiting={waiting}
                    totalTrainingTime={totalTrainingTime}
                    warningData={warningData}
                    predictData={predictResData}
                    showWarnRes={showWarnRes}
                    setExtraData={setExtraData}
                />
            </Card>
        </div>
    );
}
