// ------------------ CSRF Helper ------------------
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let cookie of cookies) {
            cookie = cookie.trim();
            if (cookie.startsWith(name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
const csrftoken = getCookie('csrftoken');

// ------------------ Toast Container ------------------
let toastContainer = document.getElementById('toast-container');
if (!toastContainer) {
    toastContainer = document.createElement('div');
    toastContainer.id = 'toast-container';
    toastContainer.className = 'position-fixed top-0 end-0 p-3';
    toastContainer.style.zIndex = 1055;
    document.body.appendChild(toastContainer);
}

// ------------------ Toast Helper ------------------
function showToast(message, type = 'save') {
    const existingToast = Array.from(toastContainer.children).find(toast =>
        toast.querySelector('.toast-body').innerText === message
    );
    if (existingToast) return;

    const toastEl = document.createElement('div');
    const icon = type === 'save' ? '📌' : '❤️';
    const bgClass = type === 'save' ? 'bg-success' : type === 'like' && message.includes('unliked') ? 'bg-secondary' : 'bg-danger';

    toastEl.className = `toast align-items-center text-white ${bgClass} border-0 mb-2`;
    toastEl.setAttribute('role', 'alert');
    toastEl.setAttribute('aria-live', 'assertive');
    toastEl.setAttribute('aria-atomic', 'true');

    toastEl.innerHTML = `
        <div class="d-flex align-items-center">
            <span class="me-2 fs-5">${icon}</span>
            <div class="toast-body fs-5 fw-bold">${message}</div>
            <button type="button" class="btn-close btn-close-white ms-3" data-bs-dismiss="toast" aria-label="Close"></button>
        </div>
    `;

    toastContainer.appendChild(toastEl);
    const bsToast = new bootstrap.Toast(toastEl, { delay: 2500 });
    bsToast.show();
    toastEl.addEventListener('hidden.bs.toast', () => toastEl.remove());
}

// ------------------ Main DOMContentLoaded ------------------
document.addEventListener("DOMContentLoaded", function () {

    // ----------------- Save Button -----------------
    const saveBtn = document.getElementById("save-btn");
    if (saveBtn) {
        const toggleUrl = saveBtn.dataset.toggleUrl;
        const savedCountBadge = document.getElementById("savedCountBadge");
        if (savedCountBadge && savedCountBadge.innerText === '') savedCountBadge.innerText = 0;

        saveBtn.addEventListener("click", function () {
            const postId = this.dataset.id;
            fetch(toggleUrl, {
                method: "POST",
                headers: {
                    "X-CSRFToken": csrftoken,
                    "Content-Type": "application/x-www-form-urlencoded"
                },
                body: `post_id=${postId}`
            })
            .then(res => {
                if (!res.ok) throw new Error('Request failed');
                return res.json();
            })
            .then(data => {
                const saveCount = document.getElementById("save-count");
                if (saveCount) saveCount.innerText = data.total_saves;

                if (data.saved) {
                    saveBtn.classList.remove("btn-outline-success");
                    saveBtn.classList.add("btn-success");
                    saveBtn.innerHTML = `📌 Saved (<span id="save-count">${data.total_saves}</span>)`;
                    showToast("Recipe saved!", "save");
                } else {
                    saveBtn.classList.remove("btn-success");
                    saveBtn.classList.add("btn-outline-success");
                    saveBtn.innerHTML = `Save (<span id="save-count">${data.total_saves}</span>)`;
                    showToast("Recipe removed from saved!", "save");
                }

                const dropdownMenu = document.getElementById("savedDropdownMenu");
                if (dropdownMenu && data.saved_posts) {
                    dropdownMenu.innerHTML = "";
                    if (data.saved_posts.length === 0) {
                        const li = document.createElement("li");
                        li.className = "text-center text-muted p-2";
                        li.innerText = "No saved recipes";
                        dropdownMenu.appendChild(li);
                    } else {
                        data.saved_posts.slice(0, 3).forEach(post => {
                            const li = document.createElement("li");
                            li.className = "dropdown-item d-flex align-items-center";
                            li.innerHTML = `
                                ${post.image_url ? `<img src="${post.get_image_url}" alt="${post.title}" 
                                    style="width:40px; height:40px; object-fit:cover; margin-right:8px; border-radius:4px;">` : ""} 
                                <a href="/post/${post.id}/" class="text-decoration-none text-dark">${post.title}</a>
                            `;
                            dropdownMenu.appendChild(li);
                        });
                        const divider = document.createElement("li");
                        divider.innerHTML = `<hr class="dropdown-divider">`;
                        dropdownMenu.appendChild(divider);
                        const viewAll = document.createElement("li");
                        viewAll.className = "text-center";
                        viewAll.innerHTML = `<a href="/saved-posts/" class="text-decoration-none fw-bold">View All</a>`;
                        dropdownMenu.appendChild(viewAll);
                    }
                }

                if (savedCountBadge) savedCountBadge.innerText = data.total_saves > 0 ? data.total_saves : 0;

            })
            .catch(err => {
                console.error("Error:", err);
                showToast("An error occurred, please try again.", "error");
            });
        });
    }

    // ----------------- Like Button -----------------
    const likeBtn = document.getElementById("like-btn");
    if (likeBtn) {
        function animateHeart(button) {
            button.classList.add('animate-like');
            setTimeout(() => button.classList.remove('animate-like'), 500);
        }
        likeBtn.addEventListener("click", function () {
            const postId = this.dataset.id;
            fetch(`/post/${postId}/like/`, {
                method: "POST",
                headers: {
                    "X-CSRFToken": csrftoken,
                    "Content-Type": "application/json"
                },
                credentials: 'same-origin'
            })
            .then(res => res.json())
            .then(data => {
                const likeCountEl = document.getElementById("like-count");
                if (likeCountEl) likeCountEl.innerText = data.total_likes;
                if (data.liked) {
                    likeBtn.classList.remove("btn-outline-danger");
                    likeBtn.classList.add("btn-danger");
                    likeBtn.innerHTML = `❤️ Like (<span id="like-count">${data.total_likes}</span>)`;
                    showToast("Recipe liked!", "like");
                } else {
                    likeBtn.classList.remove("btn-danger");
                    likeBtn.classList.add("btn-outline-danger");
                    likeBtn.innerHTML = `🤍 Like (<span id="like-count">${data.total_likes}</span>)`;
                    showToast("Recipe unliked!", "like");
                }
                animateHeart(likeBtn);
            })
            .catch(err => console.error("Like error:", err));
        });
    }

// ================= Show More Comments =================
const showMoreBtn = document.getElementById("show-more-btn");
if (showMoreBtn) {

    showMoreBtn.addEventListener("click", function () {
        const postId = this.dataset.postId;
        let nextPage = parseInt(this.dataset.nextPage);

        fetch(`/post/${postId}/load-more-comments/?page=${nextPage}`)
            .then(response => response.json())
            .then(data => {
                const commentsList = document.getElementById("comments-list");
                if (!commentsList) return;

                data.comments.forEach(comment => {
                    if (!document.querySelector(`[data-comment-id="${comment.id}"]`)) {

                        const div = document.createElement("div");
                        div.className = "card mb-3 shadow-sm comment-box rounded-3";
                        div.setAttribute("data-comment-id", comment.id);

                        div.innerHTML = `
                            <div class="card-body p-3">
                                <div class="d-flex align-items-center justify-content-between mb-2">
                                    <div class="d-flex align-items-center">
                                    
                                       <img src="${comment.profile.get_image_url}"
     onerror="this.src='/static/users/default_profile.png';"
     alt="${comment.username}'s profile"
     class="comment-avatar rounded-circle border me-2">

                                        <div class="fw-bold text-primary">${comment.username}</div>
                                    </div>
                                    <small class="text-muted">${comment.date_posted}</small>
                                </div>
                                <p class="mb-0">${comment.content}</p>
                            </div>
                        `;

                        // Add smooth animation
                        div.style.opacity = 0;
                        div.style.transform = "translateY(-20px)";
                        commentsList.appendChild(div);
                        setTimeout(() => {
                            div.style.transition = "all 0.5s ease";
                            div.style.opacity = 1;
                            div.style.transform = "translateY(0)";
                        }, 50);
                    }
                });

                // Update next page or remove button
                if (data.has_next) {
                    showMoreBtn.dataset.nextPage = data.next_page;
                } else {
                    showMoreBtn.remove();
                }
            })
            .catch(error => console.error("Error loading comments:", error));
    });

    // ================= Event delegation for comment images =================
    const commentsContainer = document.getElementById("comments-list");
    commentsContainer.addEventListener("click", function(e) {
        if(e.target.tagName === "IMG" && e.target.classList.contains("account-img")) {
            console.log("Profile image clicked for:", e.target.alt);
            // Optional: open profile modal or perform animation
        }
    });
}


    // ----------------- Back to Top -----------------
    const backToTopBtn = document.getElementById('backToTopBtn');
    if (backToTopBtn) {
        window.addEventListener('scroll', function () {
            if (document.body.scrollTop > 100 || document.documentElement.scrollTop > 100) {
                backToTopBtn.style.display = 'block';
                backToTopBtn.style.opacity = 1;
            } else {
                backToTopBtn.style.opacity = 0;
                setTimeout(() => backToTopBtn.style.display = 'none', 300);
            }
        });
        backToTopBtn.addEventListener('click', function () {
            window.scrollTo({ top: 0, behavior: 'smooth' });
        });
    }

    // ================= Recipe Modal =================
    const recipeModalEl = document.getElementById('recipeModal');
    if (recipeModalEl) {
        const recipeModal = new bootstrap.Modal(recipeModalEl);
        document.querySelectorAll('.open-recipe-btn').forEach(button => {
            button.addEventListener('click', async function () {
                const recipeId = this.dataset.postId;
                try {
                    const response = await fetch(`/post/${recipeId}/json/`);
                    const data = await response.json();
                    if (data.error) throw new Error(data.error);

                    const modalContent = document.getElementById('modal-content');
                    if (modalContent) {
                        modalContent.innerHTML = `
                            <h4>${data.title}</h4>
                            ${data.image_url ? `<img src="${data.get_image_url}" class="img-fluid mb-3" alt="${data.title}">` : ''}
                            <p><strong>Description:</strong> ${data.description}</p>
                            <h6>Ingredients:</h6><p>${data.ingredients}</p>
                            <h6>Instructions:</h6><p>${data.instructions}</p>
                        `;
                    }
                    recipeModal.show();
                } catch (error) {
                    console.error('Error fetching recipe:', error);
                    alert('Could not load recipe details.');
                }
            });
        });
    }

    // ================= Live Recipe Search =================
    const searchInput = document.getElementById('live-search');
    const resultsBox = document.getElementById('live-results');
    if (searchInput && resultsBox) {
        let debounceTimer;
        searchInput.addEventListener('keyup', function () {
            clearTimeout(debounceTimer);
            debounceTimer = setTimeout(() => {
                const query = searchInput.value.trim();
                if (!query.length) { resultsBox.innerHTML = ''; return; }

                fetch(`/live-search/?q=${encodeURIComponent(query)}`)
                    .then(r => r.json())
                    .then(data => {
                        resultsBox.innerHTML = '';
                        if (data.length === 0) {
                            resultsBox.innerHTML = `<div class="list-group-item">No recipes found</div>`;
                            return;
                        }
                        data.forEach(item => {
                            resultsBox.innerHTML += `
                                <a href="/post/${item.id}" class="list-group-item list-group-item-action">
                                    ${item.title}
                                </a>`;
                        });
                    })
                    .catch(error => console.error("Live search error:", error));
            }, 300);
        });

        document.addEventListener('click', e => {
            if (!searchInput.contains(e.target) && !resultsBox.contains(e.target)) resultsBox.innerHTML = '';
        });
    }

    // ----------------- Auto Dismiss Django Alerts -----------------
    const alerts = document.querySelectorAll('.alert.auto-dismiss');
    if (alerts.length > 0) {
        setTimeout(() => {
            alerts.forEach(alert => {
                if (typeof bootstrap !== 'undefined') {
                    new bootstrap.Alert(alert).close();
                } else alert.remove();
            });
        }, 3000);
    }
});

