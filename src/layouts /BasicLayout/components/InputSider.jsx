import { Card, Tabs, Layout } from "@arco-design/web-react"
import { Link } from "@arco-design/web-react";


export default function InputSider (props) {
  const TabPane = Tabs.TabPane
  const Sider = Layout.Sider
  return(
    <Card
      title='参数列表'
      style={{
        width: '100%',
        height: '100%',
        overflow: "hidden",
        fontSize: '100px',
        maxHeight: 'calc(100% - 40px)'
      }}
    >
    </Card>
   )
   
}