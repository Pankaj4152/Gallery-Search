import axiosInstance from './axiosInstance';

export const getImages = async () => {
    return axiosInstance.get('http://localhost:8000/gallery/image-list/')
}

export const uploadImages = async (formData: FormData) => {
    const response = await axiosInstance.post(
        '/gallery/upload/',
        formData,
        {
            headers: {
                "Content-Type": "multipart/form-data",
                Authorization: `Bearer ${localStorage.getItem("access")}`
            },
        }
    );
    return response.data;
};