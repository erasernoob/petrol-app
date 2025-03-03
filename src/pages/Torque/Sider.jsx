import { Form, Input, Button, Message } from '@arco-design/web-react';
import { open } from '@tauri-apps/plugin-dialog';
import '../style.css'
import { basename } from '@tauri-apps/api/path';
import { useState } from 'react'
import FileUploader from '../components/FileUpLoader';


export default function Sider({form, tabsName, handleSubmit, datas, fileList, setFileList}) {
  const [orbit, setOrbit] = useState(false)
  const [drillState, setDrillState] = useState(false)

  const handleUpload = async (id) => {
    const filePath = await open({ multiple: false })
    if (filePath) {
      const filename = await basename(filePath)
      setFileList((prev) => ([ ...prev ,{name: filename, path: filePath}]))
      console.log(fileList)
      Message.success(`${filename}导入成功！`)
      if (id === 1) {
        setOrbit(true)
      } else if (id === 2) (setDrillState(true))
    } else {
      Message.info('文件上传失败,请重新导入')
    }
  }

  return (
    <div className='input-page'>
      <div className='file-uploader'>
        <FileUploader orbit={orbit} setDrillState={setDrillState} setOrbit={setOrbit} drillState={drillState} handleUpload={handleUpload} />
     </div>
      <div className='input-form'>
        {form}
      </div>
    </div>
  );
}
