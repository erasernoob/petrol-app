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
import { handleUpload } from '../utils/utils';


export default function Sider({form, tabsName, handleSubmit, datas, file={name: ''}, setFile}) {

  const [orbit, setOrbit] = useState(false)

  const handleCancel = (id) => {
    if (id === 1) {
      setOrbit(false)
      setFile({name: '', path: ''})
    }
  }

  return (
    <div className='input-page'>
      <div className='file-uploader'>
        <FileUpLoader handleCancel={handleCancel} orbit={orbit} setOrbit={setOrbit} handleUpload={handleUpload} />
          </div>
      <div className='input-form'>
        {form}
      </div>
    </div>
  );
}
