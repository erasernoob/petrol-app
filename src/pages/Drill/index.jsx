import { Button } from "@arco-design/web-react"
import { Form, Input } from "@arco-design/web-react"
export default function DrillPage() {
    return (
        <>
    <Form
        onchange={() => console.log('first')}
        onSubmit={(data) => {
            console.log(data)
        }}
    >
        <Form.Item
            field={'h'}
            label='hy'
        >
            <Input />
        </Form.Item>
        <Button htmlType="submit" ></Button>
        </Form>
    </>
   )
}