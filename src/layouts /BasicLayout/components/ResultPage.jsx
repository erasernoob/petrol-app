import { Card } from '@arco-design/web-react'
import { RouterProvider } from 'react-router-dom'
import routerList from '../../../routers'

export default function ResultContent() {
    return (
    <Card
      title='计算结果'
      style={{
        width: '100%',
        height: '100%',
        overflow: "hidden",
        maxHeight: 'calc(100% - 1px)',
        borderTop: '0px'
      }}
    >
      {/* <RouterProvider router={routerList} /> */}
    </Card>

    )

}