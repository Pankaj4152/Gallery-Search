import axios from 'axios'

export const getImages = () => {
    return axios.get('http://localhost:8000/gallery/image-list/')
}