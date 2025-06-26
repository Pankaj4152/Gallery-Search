import axiosInstance from './axiosInstance';

export const getImages = async () => {
    return axiosInstance.get('gallery/image-list/')
}

export const uploadImages = async (formData: FormData) => {
    const response = await axiosInstance.post(
        '/gallery/upload/',
        formData
    );
    return response.data;
};

export const deleteImage = async (imageId: number) => {
    return axiosInstance.delete(`/gallery/delete/${imageId}/`);
};

export const searchImages = async (query: string) => {
    return axiosInstance.get(`gallery/search/?q=${encodeURIComponent(query)}`);
};