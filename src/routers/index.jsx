import { createHashRouter, createBrowserRouter } from "react-router-dom"
import HydroPage from "../pages/Hydro"
import DrillPage from "../pages/Drill"

export const routeList = [
    {
        name: '水力学',
        path: '/',
        element: <HydroPage />
    },
    {
        name: '摩阻扭矩',
        path: '/torque',
        element: <></>
    },
    {
        name: '钻头状态',
        path: '/drill',
        element: <DrillPage />
    },
    {
        name: '延伸极限',
        path: '/limit',
        element: <></>
    },
    {
        name: '风险预警',
        path: '/risk',
        element: <></>
    },
]

const routerList = createHashRouter(routeList)

export default routerList



