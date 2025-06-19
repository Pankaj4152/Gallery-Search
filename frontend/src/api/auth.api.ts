import axios from 'axios';

export const loginUser = async (username: string, password: string) => {
    const res = await axios.post("http://localhost:8000/api/token/", {
        username,
        password,
    });

    const { access, refresh } = res.data;
    localStorage.setItem("access", access);
    localStorage.setItem("refresh", refresh);
};