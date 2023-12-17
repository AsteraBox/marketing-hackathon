import React, { useEffect } from "react";

import { setCredentials, setAuthorized } from "../redux/reducers/auth";
import { useDispatch, useSelector } from "react-redux";

import { api, useGetTextsQuery } from "../redux/reducers/api";

import { Button, Form, Input, Typography } from "antd";

export default () => {
    const { credentials, authorized } = useSelector((state) => state.auth);
    const dispatch = useDispatch();

    // RTK
    const { isLoading, isSuccess, error } = useGetTextsQuery(1, {
        skip: !credentials,
    });

    const onFinish = (values) => {
        dispatch(api.util.resetApiState());
        dispatch(setCredentials(values));
    };

    useEffect(() => {
        dispatch(setAuthorized(isSuccess));
    }, [isSuccess]);

    return (
        <Form
            name="basic"
            labelCol={{
                span: 8,
            }}
            wrapperCol={{
                span: 16,
            }}
            style={{
                width: "100%",
                maxWidth: 320,
                margin: "auto"
            }}
            onFinish={onFinish}
            autoComplete="off"
        >
            <Form.Item
                label="Логин"
                name="username"
                rules={[
                    {
                        required: true,
                    },
                ]}
            >
                <Input />
            </Form.Item>

            <Form.Item
                label="Пароль"
                name="password"
                rules={[
                    {
                        required: true,
                    },
                ]}
            >
                <Input.Password />
            </Form.Item>

            {credentials && !authorized && error && (
                <Form.Item
                    wrapperCol={{
                        offset: 8,
                        span: 16,
                    }}
                >
                    <Typography.Text type="danger">Ошибка: {error?.status == 401 ? "неверный логин или пароль" : "неизвестная ошибка"} </Typography.Text>
                </Form.Item>
            )}

            <Form.Item
                wrapperCol={{
                    offset: 8,
                    span: 16,
                }}
            >
                <Button type="primary" htmlType="submit">
                    Войти
                </Button>
            </Form.Item>
        </Form>
    );
};
