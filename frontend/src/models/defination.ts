
export interface UserInfo {
    id: number
    username: string
    name: string
    role: 'student' | 'admin'
    status: 0 | 1
    phone: string | null
    email: string | null
}

export interface AccountSessionData {
    token: string
    user: UserInfo
}

export interface LoginData{
    username: string
    password: string
}

export interface LoginResult{
    code: number
    message: string
    data: AccountSessionData | null
}
