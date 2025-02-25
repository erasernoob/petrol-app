import { Radio ,Form, Input, Button, Message } from '@arco-design/web-react';
import { open } from '@tauri-apps/plugin-dialog';
import '../style.css'
import { basename } from '@tauri-apps/api/path';
import { useState } from 'react'
import FileUploader from '../components/FileUpLoader';

const RadioGroup = Radio.Group
const subRoutesOptions = ['裸眼延伸极限', '水力延伸极限', '机械延伸极限', '屈曲临界载荷']

export default function Sider({ form }) {
    const [orbit, setOrbit] = useState(false)
    const [drillState, setDrillState] = useState(false)
    const [subRoute, setSubRoute] =  useState([])



const Tabs = (
    <RadioGroup
        type='button'
        size='large'
        name='chart'
        defaultValue='裸眼延伸极限'
        onChange={(value) => {
        }}
        options={subRoutesOptions}
        noStyle
      >
      </RadioGroup>
    )

    return (

    <div className='input-page' style={{paddingTop: '5px'}}>
        {Tabs}
      <div className='file-uploader'>
        <FileUploader orbit={orbit} drillState={drillState}  />
     </div>
      <div className='input-form'>
        {form}
      </div>
    </div>
  );

}