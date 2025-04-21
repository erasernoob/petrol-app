import { Table, Typography } from '@arco-design/web-react';
import React from 'react';

const FileUploadDisplay = ({ jsonData }) => {
    // Display component
    return (
        <div style={{ padding: '' }}>
            {jsonData && jsonData.length > 0 ? (
                <Table
                    data={jsonData}
                    columns={Object.keys(jsonData[0]).map((key) => ({
                        title: key,       // Column title based on key
                        dataIndex: key,   // Data mapping to key
                        key: key,         // Unique key for each column
                    }))}
                    pagination={false}
                    scroll={{ x: 'max-content' }} // ✅ 强制横向滚动
                    style={{
                        overflowY: "auto",
                        overflowX: "auto"
                    }}
                />
            ) : (
                <Typography.Text>没有数据展示</Typography.Text>  // Message for no data
            )}
        </div>
    );
};

export default FileUploadDisplay;
