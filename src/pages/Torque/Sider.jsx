import { Form, Input, Button, Message } from '@arco-design/web-react';
import { open } from '@tauri-apps/plugin-dialog';
import '../style.css'
import { basename } from '@tauri-apps/api/path';
import { useState } from 'react'
import FileUploader from '../components/FileUpLoader';


export default function Sider({form, tabsName, handleSubmit, datas, fileList, setFileList}) {
  const [orbit, setOrbit] = useState(false)
  const [drillState, setDrillState] = useState(false)

  const handleCancel = (id) => {
    if (id === 1) {
      setOrbit(false)
      setFileList(prev => ({...prev, orbit: {name: '', path: ''}}))
    } else if(id === 2) {
      setDrillState(false)
      setFileList(prev => ({...prev, drill: {name: '', path: ''}}))
    } else {

    }
  }

  const handleUpload = async (id) => {
    const filePath = await open({
      name: "导入文件",
       multiple: false, 
       filters: [{extensions: ['xlsx'], name: ''}],
    })
    if (filePath) {
      const filename = await basename(filePath)
      if (id === 1) {
        setFileList(prev => ({...prev, orbit: {name: filename, path: filePath}}))
      } else if (id == 2) {
        setFileList((prev) => ({...prev, drill: {name: filename, path: filePath}}))
      } else {
        // 上传参数
      }
      Message.success(`${filename}导入成功！`)
      if (id === 1) {
        setOrbit(true)
      } else if (id === 2) (setDrillState(true))
    } else {
      setFileList({orbit: {name: '', path: ''}, drill: {name: '', path: ''}})
      Message.info('文件上传失败,请重新导入')
    }
  }

  return (
    <div className='input-page'>
      <div className='file-uploader'>
        <FileUploader orbit={orbit} handleCancel={handleCancel} setDrillState={setDrillState} setOrbit={setOrbit} drillState={drillState} handleUpload={handleUpload} />
     </div>
      <div className='input-form'>
        {form}
      </div>
    </div>
  );
}

