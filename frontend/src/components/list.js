import React, { useState } from "react";

import { api, useGetTextsQuery, useConfirmTextMutation } from "../redux/reducers/api";
import { useDispatch } from "react-redux";

import { Pagination, Table, Switch } from "antd";

export default () => {
    const [page, setPage] = useState(1);
    const dispatch = useDispatch();

    // RTK
    const { data, isLoading, isSuccess } = useGetTextsQuery(page);
    const [confirm] = useConfirmTextMutation();

    // Click handler
    const onChange = async (id) => {
        try {
            await confirm(id).unwrap();
            dispatch(api.util.updateQueryData("getTexts", page, (data) => {
                data.records = data.records?.map(el => ({ ...el, confirmed: el.id === id ? !el.confirmed : el.confirmed }));
            }));
        } catch (error) {
            console.log(error);
        }
    }

    // Format data
    const dataSource = isSuccess && data.records?.map((el, index) => ({
        ...el,
        key: index,
        confirm: <Switch checked={el.confirmed} onChange={() => onChange(el.id)} />,
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
            title: "Подтвердить",
            dataIndex: "confirm",
            key: "confirm",
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
