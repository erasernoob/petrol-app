import { Form, Input, Button, Message } from '@arco-design/web-react';
import FileUpLoader from '../components/FileUpLoader';
import { hydro } from '../../data/Params'
import DynamicForm from '../components/DynamicForm';
import { post } from '../components/axios';
import '../style.css'
import { useSelector } from 'react-redux';
import { useDispatch } from 'react-redux';
import { increment } from '../../features/counterSlice';

const tabsName = ['基本参数', '钻井液', '钻头', '钻杆接头', '地面管汇', '岩屑床']

const handleSubmit = async (data) => {
  try {
    const response = post('/hydro', JSON.stringify(data))
  } catch (error) {
    console.log(error)
  }
  
}

export default function HydroPage() {

const counter = useSelector(state => state.counter.value)
const dispatch = useDispatch()


  return (
    <div className='input-page'>
      <div className='fileup-loader'>
        <FileUpLoader />
      </div>
      <div className='input-form'>
        <DynamicForm handleSubmit={handleSubmit} datas={hydro} tabs={tabsName} />
      </div>
    </div>
  );
}
