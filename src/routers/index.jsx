import { createHashRouter, createBrowserRouter } from "react-router-dom"
import HydroPage from "../pages/Hydro"
import DrillPage from "../pages/Drill"
import TorquePage from "../pages/Torque"
import RiskPage from "../pages/Risk"
import LimitPage from "../pages/Limit"

export const routeList = [
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
        name: '钻头状态',
        path: '/drill',
        element: <DrillPage />
    },
    {
        name: '延伸极限',
        path: '/limit',
        element: <LimitPage />
    },
    {
        name: '风险预警',
        path: '/risk',
        element: <RiskPage />
    },
]

const routerList = createHashRouter(routeList)

export default routerList



