import type { LoginData, LoginResult } from "@/models/defination";
import request from "@/utils/request";

export function loginApi(data: LoginData) {
    return request<LoginResult, LoginResult, LoginData>({
        url: '/api/auth/login',
        method: 'POST',
        data: data
    })
}
