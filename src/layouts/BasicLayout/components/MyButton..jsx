import { Button } from "@arco-design/web-react"

export default function MyButton({children})  {
    return (
        <Button type="dashed">{children}</Button>
    )
}