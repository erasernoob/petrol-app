import { Form, Input, Button, Message } from '@arco-design/web-react';
import { open } from '@tauri-apps/plugin-dialog';
import FileUpLoader from '../components/FileUpLoader';
import DynamicForm from '../components/DynamicForm';
import { post } from '../../components/axios';
import '../style.css'
import { useSelector, useDispatch } from 'react-redux';
import { useState } from 'react';
import { basename } from '@tauri-apps/api/path';
import Papa from 'papaparse';
import { setHydro } from '../../store/dataSlice'; 


export default function Sider({form, tabsName, handleSubmit, datas, file={name: ''}, setFile}) {

  const [orbit, setOrbit] = useState(false)

  const handleUpload = async (id) => {
    const filePath = await open({ multiple: false })
    if (filePath) {
      const filename = await basename(filePath)
      setFile(() => ({name: filename, path: filePath}))
      Message.success(`${filename}上传成功！`)
      setOrbit((prev) => !prev)
    } else {
      Message.info('文件上传失败,请重新上传')
    }

  }

  return (
    <div className='input-page'>
      <div className='file-uploader'>
        <FileUpLoader orbit={orbit} setOrbit={setOrbit} handleUpload={handleUpload} />
          </div>
      <div className='input-form'>
        {form}
      </div>
    </div>
  );
}
