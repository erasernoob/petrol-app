import { Button } from "@arco-design/web-react";

export default function FileUpLoaderBtn({
    uploadText,
    uploadStat,
    handleUpload,
    handleCancel,
    style,
    id
}) {
    return (
        !uploadStat ?
            <Button type="primary" style={style} onClick={() => handleUpload(id)} > {uploadText}</Button > :
            <Button type="secondary" onClick={() => handleCancel(id)}>重新上传</Button>
    )
}