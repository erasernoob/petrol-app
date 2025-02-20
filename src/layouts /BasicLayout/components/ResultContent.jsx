import { Card } from '@arco-design/web-react'

export default function ResultContent() {
    return (
    <Card
      title='计算结果'
      style={{
        width: '100%',
        height: '100%',
        overflow: "hidden",
        fontSize: '100px',
        maxHeight: 'calc(100% - 40px)',
        borderTop: '0px'
      }}
    >
    </Card>

    )

}