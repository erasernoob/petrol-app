import { Radio ,Form, Input, Button, Message } from '@arco-design/web-react';
import { open } from '@tauri-apps/plugin-dialog';
import '../style.css'
import { basename } from '@tauri-apps/api/path';
import { useState } from 'react'
import FileUploader from '../components/FileUpLoader';

const RadioGroup = Radio.Group
const subRoutesOptions = [
  { label: '裸眼延伸极限', value: 1 },
  { label: '水力延伸极限', value: 2 },
  { label: '机械延伸极限', value: 3 },
  { label: '屈曲临界载荷', value: 4 }
];
export default function Sider({ form, activeRoute, setActiveRoute, fileList}) {
    const [orbit, setOrbit] = useState(false)
    const [drillState, setDrillState] = useState(false)
const Tabs = (
    <RadioGroup
        type='button'
        size='large'
        name='chart'
        defaultValue={1}
        onChange={(value) => {
            setActiveRoute(value)
        }}
        options={subRoutesOptions}
      >
      </RadioGroup>
    )

    return (

    <div className='input-page' style={{paddingTop: '5px'}}>
        {Tabs}
      <div className='file-uploader'>
        <FileUploader orbit={orbit} drillState={activeRoute >= 3 ? drillState : 'default'}  />
     </div>
      <div className='input-form'>
        {form}
      </div>
    </div>
  );

}