import React, { useState } from "react";

import { api, useGetTextsQuery, useConfirmTextMutation } from "../redux/reducers/api";

import { Button, Pagination, Table } from "antd";
import { useDispatch } from "react-redux";

export default () => {
    const [page, setPage] = useState(1);
    const dispatch = useDispatch();

    // RTK
    const { data, isLoading, isSuccess } = useGetTextsQuery(page);
    const [confirm] = useConfirmTextMutation();

    // Click handler
    const onClick = async (id) => {
        const { data: { success } } = await confirm(id);
        if (success) {
            dispatch(api.util.updateQueryData("getTexts", page, (data) => {
                data.results = data.results.map(el => ({ ...el, confirmed: el.confirmed || el.id === id }));
            }));
        }
    }

    // Fromat data
    const dataSource = data?.results.map((el, index) => ({
        ...el,
        key: index,
        button: !el.confirmed && (
            <Button size="small" onClick={() => onClick(el.id)}>
                Подтвердить
            </Button>
        ),
    }));

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
        },
    ];

    return (
        <div>
            <Table loading={isLoading} dataSource={dataSource} columns={columns} pagination={false} />
            <Pagination defaultCurrent={page} total={data?.total} pageSize={10} onChange={setPage} style={{ marginTop: 30 }} />
        </div>
    );
};
