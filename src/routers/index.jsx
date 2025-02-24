import { createHashRouter, createBrowserRouter } from "react-router-dom"
import HydroPage from "../pages/Hydro"
import DrillPage from "../pages/Drill"
import TorquePage from "../pages/Torque"
import RiskPage from "../pages/Risk"
import LimitPage from "../pages/Limit"

export const routeList = [
    {
        name: '数据管理系统',
        // TODO: change to the database system url
        path: 'http://www.baidu.com',
        element: <></>
    },
    {
        name: '水力学',
        path: '/',
        element: <HydroPage />
    },
    {
        name: '摩阻扭矩',
        path: '/torque',
        element: <TorquePage />
    },
    {
        name: '延伸极限',
        path: '/limit',
        element: <LimitPage />
    },
    {
        name: '钻头状态',
        path: '/drill',
        element: <DrillPage />
    },
    {
        name: '风险预警',
        path: '/risk',
        element: <RiskPage />
    },
]

const routerList = createHashRouter(routeList)

export default routerList



