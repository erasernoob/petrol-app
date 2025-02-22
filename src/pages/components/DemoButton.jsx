import { Form, Message } from "@arco-design/web-react";
import { useEffect, useRef } from "react";

export default function DemoButton() {
  const { form, disabled, isSubmitting } = Form.useFormContext();
  const messageRef = useRef(null)

  useEffect(() => {
    if (isSubmitting) {
      messageRef.current = 'id-' + Date.now()
      Message.loading({
        id: messageRef.current,
        content: 'submitting',
        duration: 0
      });
    } else {
      if (messageRef.current) {
        const isError = Object.keys(form.getFieldsError()).length > 0;

        Message[isError ? 'error' : 'success']({
          id: messageRef.current,
          content: isError ? 'validate failed' : 'submitted',
          duration: 3000
        });
      }
      messageRef.current = null
    }
  }, [isSubmitting])
    return (
    <>
      <Button
        type='primary'
        htmlType='submit'
        disabled={disabled}
        loading={isSubmitting}
        style={{ marginRight: 24 }}
      >
        Submit
      </Button>
      <Button
        disabled={disabled}
        style={{ marginRight: 24 }}
        onClick={() => {
          form.resetFields();
        }}
      >
        Reset
      </Button>
    </>
  );

}