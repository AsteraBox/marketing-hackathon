import React, { useEffect } from "react";

import { setCredentials, setAuthorized } from "../redux/reducers/auth";
import { useDispatch, useSelector } from "react-redux";

import { api, useGetTextsQuery } from "../redux/reducers/api";

import { LockOutlined, UserOutlined } from '@ant-design/icons';
import { Button, Form, Input, Typography } from "antd";

export default () => {
    const { credentials, authorized } = useSelector((state) => state.auth);
    const dispatch = useDispatch();

    // RTK
    const { isSuccess, error } = useGetTextsQuery(1, {
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
            style={{
                width: "100%",
                maxWidth: 240,
                margin: "auto"
            }}
            onFinish={onFinish}
            autoComplete="off"
        >
            <Form.Item
                name="username"
                rules={[{ required: true, message: 'Введите имя пользователя!' }]}
            >
                <Input prefix={<UserOutlined className="site-form-item-icon" />} placeholder="Логин" />
            </Form.Item>

            <Form.Item
                name="password"
                rules={[{ required: true, message: 'Введите пароль!' }]}
            >
                <Input prefix={<LockOutlined className="site-form-item-icon" />} type="password" placeholder="Пароль" />
            </Form.Item>

            {credentials && !authorized && error && (
                <Form.Item>
                    <Typography.Text type="danger" stype={{ margin: 0 }}>Ошибка: {error?.status == 401 ? "неверный логин или пароль" : "неизвестная ошибка"} </Typography.Text>
                </Form.Item>
            )}

            <Form.Item>
                <Button type="primary" htmlType="submit" style={{ width: "100%" }}>
                    Войти
                </Button>
            </Form.Item>
        </Form>
    );
};
