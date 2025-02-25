import { Form, Input, Button, Message } from '@arco-design/web-react';
import { open } from '@tauri-apps/plugin-dialog';
import '../style.css'
import { basename } from '@tauri-apps/api/path';
import { useState } from 'react'


export default function Sider() {
    const handleUpload = () => {

    }

    return (
    <div className='input-page'>
      <div className='file-uploader'>
        {
          !orbit ?  <Button type="primary" 
            onClick={() => handleUpload(1)}
        >导入井眼轨迹</Button> :
          <Button type="secondary"  
            onClick={() => setOrbit(false)}
        >重新导入</Button>
        }
        {
          !drillState ?  <Button type="primary" 
            onClick={() => handleUpload(2)}
        >导入钻具状态</Button> :
          <Button type="secondary"  
            onClick={() => setDrillState(false)}
        >重新导入</Button>
        }
      </div>
      <div className='input-form'>
        {form}
      </div>
    </div>
  );

    return(<></>)
    

}