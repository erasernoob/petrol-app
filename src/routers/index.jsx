import { createHashRouter } from "react-router-dom"
import DrillPage from "../pages/Drill"
import HydroPage from "../pages/Hydro"
import LimitPage from "../pages/Limit"
import LoginPage from "../pages/Login/LoginPage"
import RiskPage from "../pages/Risk"
import TorquePage from "../pages/Torque"

export const routeList = [
    {
        name: '数据管理系统',
        // TODO: change to the database system url
        path: 'http://47.108.223.152:5173/petroleum-data-storage/',
        element: <></>
    },
    {
        name: 'login',
        path: '/',
        element: <LoginPage />
    },
    {
        name: '水力学计算',
        path: '/hydro',
        element: <HydroPage />
    },
    {
        name: '摩阻扭矩计算',
        path: '/torque',
        element: <TorquePage />
    },
    {
        name: '延伸极限预测',
        path: '/limit',
        element: <LimitPage />
    },
    {
        name: '钻头状态监测',
        path: '/drill',
        element: <DrillPage />,
    },
    {
        name: '井漏风险预警',
        path: '/risk',
        element: <RiskPage />
    },
]

const routerList = createHashRouter(routeList)

export default routerList



