const apiBaseURL = "https://coherent-super-snapper.ngrok-free.app";
const apiClient = axios.create({baseURL: apiBaseURL})


const api = {
    v1: {
        categories: {
            list: async function(){
                try {
                    return await apiClient.get("/api/v1/categories")
                } catch (e) {}
            },
            get: async function(categoryID) {
                try {
                    return await apiClient.get(`/api/v1/categories/${categoryID}`)
                } catch (e) {}
            },
            create: async function(data, headers) {
                try {
                    return await apiClient.request({
                        url: "/api/v1/categories",
                        method: "post",
                        data: data,
                        headers: headers
                    })
                } catch (e) {}
            }
        }
    },
    auth: {
        register: async function(data) {
            try {
                return await apiClient.post("/api/auth/register", data)
            } catch (e) {}
        },
        login: async function(data) {
            try {
                return await apiClient.post("/api/auth/login", data)
            } catch (e) {}
        },
        refresh: async function(data) {
            try {
                return await apiClient.post("/api/auth/refresh", data)
            } catch (e) {}
        },
        google: async function(params) {
            try {
                return await apiClient.get("/api/auth/google" + params)
            } catch (e) {}
        }
    }
}
