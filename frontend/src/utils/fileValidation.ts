export const validateFiles = (files: File[]) => {
    const MAX_FILE_SIZE = 10 * 1024 * 1024; // 10MB
    const MAX_TOTAL_SIZE = 100 * 1024 * 1024; // 100MB
    const ALLOWED_TYPES = ['image/jpeg', 'image/png', 'image/jpg', 'image/webp'];
    
    const validFiles: File[] = [];
    const errors: string[] = [];
    let totalSize = 0;

    files.forEach((file, index) => {
        // Check file type
        if (!ALLOWED_TYPES.includes(file.type)) {
            errors.push(`File ${index + 1} (${file.name}): Invalid file type. Only JPEG, PNG, and WebP are allowed.`);
            return;
        }

        // Check individual file size
        if (file.size > MAX_FILE_SIZE) {
            errors.push(`File ${index + 1} (${file.name}): Too large (${(file.size / (1024 * 1024)).toFixed(2)}MB). Maximum size is 10MB.`);
            return;
        }

        // Check total size
        if (totalSize + file.size > MAX_TOTAL_SIZE) {
            errors.push(`File ${index + 1} (${file.name}): Would exceed total size limit of 100MB.`);
            return;
        }

        validFiles.push(file);
        totalSize += file.size;
    });

    return { validFiles, errors };
};

export const formatFileSize = (bytes: number): string => {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
};
