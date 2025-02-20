import { Card, Tabs, Layout } from "@arco-design/web-react"
import { Link } from "@arco-design/web-react";
import { RouterProvider } from "react-router-dom";
import routerList from "../../../routers";


export default function InputSider (props) {
  return(
    <Card
      title='参数列表'
      style={{
        width: '100%',
        height: '100%',
        maxWidth: 'calc(100% - 1.7px)',
        // fontSize: '10px',
        maxHeight: 'calc(100% - 2px)'
      }}
    >
      <RouterProvider router={routerList} />
    </Card>
   )
   
}