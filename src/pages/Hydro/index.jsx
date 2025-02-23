import { Form, Input, Button, Message } from '@arco-design/web-react';
import { open } from '@tauri-apps/plugin-dialog';
import FileUpLoader from '../components/FileUpLoader';
import { hydro } from '../../data/Params'
import DynamicForm from '../components/DynamicForm';
import { post } from '../components/axios';
import '../style.css'
import { useSelector, useDispatch } from 'react-redux';
import { useState } from 'react';
import { basename } from '@tauri-apps/api/path';
import Papa from 'papaparse';

const tabsName = ['基本参数', '钻井液', '钻头', '钻杆接头', '地面管汇', '岩屑床']

export default function HydroPage() {

  const [file, setFile] = useState({name: '', path: ''})
  const counter = useSelector(state => state.counter.value)
  const dispatch = useDispatch()

  const handleSubmit = async (data) => {
    // TODO: 
    // if (!file.path) return
    try {
      data.file_path = file.path ? file.path : ''
      const response = await post('/hydro', JSON.stringify(data))
      const e = Papa.parse(response, {header: true})
      const d = JSON.stringify(e.data)
      console.log(d)

    } catch (error) {
      Message.error('计算内部出现错误，请检查')
    }
  }

  const handleUpload = async () => {
    const filePath = await open({ multiple: false })
    if (filePath) {
      const filename = await basename(filePath)
      setFile(() => ({name: filename, path: filePath}))
      Message.success(`${filename}上传成功！`)
    } else {
      Message.info('文件上传失败,请重新上传')
    }
  }


  return (
    <div className='input-page'>
      <div className='file-uploader'>
        {/* <FileUpLoader /> */}
        <Button type="primary" className='' 
            onClick={() => handleUpload()}
            disabled={file.name}
        >导入井眼轨迹</Button>

        {(file.name && <Button size="small" type="secondary" className='' 
            onClick={() => setFile(() => ({name: '', path: ''}))}
        >重新上传</Button>)}
        {/* {<span>{file.name} 上传成功</span> && file.name} */}
      </div>

      <div className='input-form'>
        <DynamicForm handleSubmit={handleSubmit} datas={hydro} tabs={tabsName} />
      </div>
    </div>
  );
}
