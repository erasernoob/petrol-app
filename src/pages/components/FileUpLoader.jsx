import { useState } from 'react';
import { Upload, Message, Button } from '@arco-design/web-react';
import { open } from '@tauri-apps/plugin-dialog';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL



const isAcceptFile = (file) => {
  if (!file) return false;
  const fileExtension = file.name.split('.').pop().toLowerCase();
  return fileExtension === 'xlsx';
};



const FileUpLoader = () => {
  const [disabled, setDisabled] = useState(false);
  const [fileList, setFileList] = useState([])
  



  return (
    <Upload
      accept=".xlsx"
      // beforeUpload={() => false}
      action={API_BASE_URL + '/uploadFile'}
      multiple={false} // 只允许单个上传
      disabled={disabled} // 上传一个文件后禁用
      onChange={(fileList) => {
        if (fileList.length > 0) {
          setDisabled(true);
        }
      }}
      onDrop={(e) => {
        let uploadFile = e.dataTransfer.files[0];
        if (!isAcceptFile(uploadFile)) {
          Message.info('只能上传 .xlsx 文件，请重新选择');
        }
      }}
    //   tip="仅允许上传 .xlsx 文件"
    ></Upload>
  );
};

export default FileUpLoader;
