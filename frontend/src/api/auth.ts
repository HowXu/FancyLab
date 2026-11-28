import type { LoginData, LoginResult, RegisterData, RegisterResult } from "@/models/defination";
import request from "@/utils/request";

export function loginApi(data: LoginData) {
    return request<LoginResult, LoginResult, LoginData>({
        url: '/api/auth/login',
        method: 'POST',
        data: data
    })
}

export function registerApi(data: RegisterData) {
    return request<RegisterResult, RegisterResult, RegisterData>({
        url: '/api/auth/register',
        method: 'POST',
        data: data
    })
}
