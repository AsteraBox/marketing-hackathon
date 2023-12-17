import React, { useState } from "react";

import { api, useGetTextsQuery, useConfirmTextMutation } from "../redux/reducers/api";
import { useDispatch } from "react-redux";

import { Button, Pagination, Table } from "antd";
import { CheckCircleFilled } from '@ant-design/icons';

export default () => {
    const [page, setPage] = useState(1);
    const dispatch = useDispatch();

    // RTK
    const { data, isLoading, isSuccess } = useGetTextsQuery(page);
    const [confirm] = useConfirmTextMutation();

    // Click handler
    const onClick = async (id) => {
        try {
            await confirm(id).unwrap();
            dispatch(api.util.updateQueryData("getTexts", page, (data) => {
                data.records = data.records?.map(el => ({ ...el, confirmed: el.confirmed || el.id === id }));
            }));
        } catch (error) {
            console.log(error);
        }
    }

    // Format data
    const dataSource = isSuccess && data.records?.map((el, index) => ({
        ...el,
        key: index,
        button: !el.confirmed && (
            <Button size="small" onClick={() => onClick(el.id)}>
                Подтвердить
            </Button>
        ) || <CheckCircleFilled style={{ color: "#27AE60", fontSize: "1.4em" }} />,
    })) || [];

    // Columns
    const columns = [
        {
            title: "ID",
            dataIndex: "id",
            key: "id",
        },
        {
            title: "Текст",
            dataIndex: "text",
            key: "text",
        },
        {
            title: "Подвердить",
            dataIndex: "button",
            key: "button",
            align: "center"
        },
    ];

    return (
        <div>
            <Table loading={isLoading} dataSource={dataSource} columns={columns} pagination={false} />
            <Pagination defaultCurrent={page} total={data?.total} pageSize={10} onChange={setPage} style={{ marginTop: 30 }} />
        </div>
    );
};
