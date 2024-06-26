const categoryCreateForm = document.getElementById("create-category");

function parseJwt (token) {
    const base64Url = token.split('.')[1];
    const base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/');
    const jsonPayload = decodeURIComponent(window.atob(base64).split('').map(function (c) {
        return '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2);
    }).join(''));

    return JSON.parse(jsonPayload);
}


async function refreshTokenPair(callback) {
    const refreshToken = localStorage.getItem("refreshToken");
    if (refreshToken === undefined || refreshToken === null) {
         window.location.href = "/login";
    }

    try {
        const refreshTokenPayload = parseJwt(refreshToken);
        if (Date.now() >= refreshTokenPayload.exp * 1000) {
            localStorage.removeItem("refreshToken");
            window.location.href = "/login";
        }
    } catch (e) {
         window.location.href = "/login";
    }

    const response = await api.auth.refresh({refresh_token: refreshToken});
    if (response === undefined || response === null) {
         window.location.href = "/login";
    } else {
        localStorage.setItem("accessToken", response.data.access_token);
        localStorage.setItem("refreshToken", response.data.refresh_token);
        localStorage.setItem("tokenType", response.data.token_type);

        if (callback !== undefined) {
            await callback()
        }
    }

}

async function getAccessToken() {
    let accessToken = localStorage.getItem("accessToken");
    if (accessToken === undefined || accessToken === null) {
         await refreshTokenPair()
    }

    try {
        const accessTokenPayload = parseJwt(accessToken);
        if (Date.now() >= accessTokenPayload.exp * 1000) {
            localStorage.removeItem("accessToken");
            await refreshTokenPair()
        }
    } catch (e) {
         await refreshTokenPair()
    }

    accessToken = localStorage.getItem("accessToken");
    return accessToken
}


categoryCreateForm.addEventListener("submit", async (e) => {
    e.preventDefault();
    const accessToken = await getAccessToken()
    const tokenType = localStorage.getItem("tokenType");
    const response = await api.v1.categories.create({name: this.categoryName.value}, {Authorization: `${tokenType} ${accessToken}`})
    if (response !== undefined) {
        this.categoryName.value = "";
        await renderCategoryDropdownList();
    }
})


async function renderArticleCards(categoryID) {
    const response = await api.v1.categories.get(categoryID);
    if (response.status === 200) {
        const contentDiv = document.getElementById("content");
        contentDiv.innerHTML = "";
        response.data.articles.map(function (acticle) {
            contentDiv.innerHTML += `<div class="col-md-6 col-lg-3">
                <div class="card">
                  <div class="card-body">
                    <h3 class="card-title"></h3>
                    <p class="text-secondary">${acticle.title}</p>
                  </div>
                </div>
              </div>`
        })
    }
}

async function renderCategoryDropdownList() {
    const response = await api.v1.categories.list();
    if (response.status === 200) {
        let categoryDropdown = document.getElementById("category-dropdown-list");
        categoryDropdown.innerHTML = "";
        response.data.map(function (category) {
            const categoryLink = document.createElement("a");
            categoryLink.className = "dropdown-item";
            categoryLink.setAttribute( "rel", "noopener");
            categoryLink.href = `/${category.id}`
            categoryLink.textContent = category.name;
            categoryDropdown.appendChild(categoryLink);
        })
    }
}


document.addEventListener("DOMContentLoaded", async () => {
    await getAccessToken()
    await renderCategoryDropdownList();
    let categoryID = document.location.pathname.split("/")[1];
    try {
        categoryID = parseInt(categoryID);
        if (!isNaN(categoryID)) {
            await renderArticleCards(categoryID)
        }
    } catch (e) {}
})